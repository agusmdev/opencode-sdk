"""Server-Sent Events (SSE) streaming support."""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import suppress
from typing import TYPE_CHECKING, Any, TypeVar

import httpx
from httpx_sse import aconnect_sse

from opencode._constants import (
    DEFAULT_STREAMING_TIMEOUT,
    SSE_BACKOFF_FACTOR,
    SSE_INITIAL_DELAY,
    SSE_MAX_DELAY,
    SSE_MAX_RETRIES,
)
from opencode._exceptions import StreamingError
from opencode._logging import get_logger

if TYPE_CHECKING:
    from opencode.models.event import Event

T = TypeVar("T")


class EventStream(AsyncIterator["Event"]):
    """
    Async iterator for SSE events with automatic reconnection.

    Features:
    - Automatic reconnection with exponential backoff
    - Configurable retry limits
    - Graceful shutdown via close()
    - Context manager support

    Example:
        async with client.events.subscribe() as stream:
            async for event in stream:
                match event:
                    case MessagePartUpdatedEvent(properties=p):
                        print(p.delta, end="")
                    case SessionIdleEvent():
                        break
    """

    def __init__(
        self,
        http_client: httpx.AsyncClient,
        url: str,
        params: dict[str, Any] | None = None,
        *,
        max_retries: int = SSE_MAX_RETRIES,
        initial_delay: float = SSE_INITIAL_DELAY,
        max_delay: float = SSE_MAX_DELAY,
        backoff_factor: float = SSE_BACKOFF_FACTOR,
        timeout: float = DEFAULT_STREAMING_TIMEOUT,
    ) -> None:
        """
        Initialize the event stream.

        Args:
            http_client: The httpx async client to use
            url: The SSE endpoint URL
            params: Query parameters for the request
            max_retries: Maximum reconnection attempts before giving up
            initial_delay: Initial delay between retries (seconds)
            max_delay: Maximum delay between retries (seconds)
            backoff_factor: Multiplier for exponential backoff
            timeout: Timeout for the SSE connection
        """
        self._http = http_client
        self._url = url
        self._params = params or {}
        self._max_retries = max_retries
        self._initial_delay = initial_delay
        self._max_delay = max_delay
        self._backoff_factor = backoff_factor
        self._timeout = timeout
        self._retry_count = 0
        self._closed = False
        self._log = get_logger("opencode.streaming")
        # Maintain connection state across __anext__ calls
        self._event_iterator: AsyncIterator[Any] | None = None
        # Track the async generator for proper cleanup
        self._current_generator: AsyncGenerator[Any, None] | None = None
        # Track the current response for cancellation
        self._current_response: httpx.Response | None = None

    def __aiter__(self) -> "EventStream":
        """Return self as async iterator."""
        return self

    async def __anext__(self) -> "Event":
        """
        Get the next event from the stream.

        Handles reconnection on connection errors.

        Returns:
            The next Event

        Raises:
            StopAsyncIteration: When the stream is closed
            StreamingError: When max retries exceeded or unrecoverable error
        """
        from opencode.models.event import parse_event

        while not self._closed:
            try:
                # Reuse existing connection or establish a new one
                if self._event_iterator is None:
                    self._current_generator = self._iter_events()
                    self._event_iterator = self._current_generator.__aiter__()

                while True:
                    try:
                        event = await self._event_iterator.__anext__()
                    except StopAsyncIteration:
                        # Iterator exhausted, need to reconnect
                        self._event_iterator = None
                        self._current_generator = None
                        break

                    # Skip empty events or comments
                    if not event.data:
                        continue

                    try:
                        parsed = parse_event(event.data)
                        self._retry_count = 0  # Reset on successful event
                        return parsed
                    except (json.JSONDecodeError, ValueError) as e:
                        self._log.warning(
                            "event_parse_error",
                            error=str(e),
                            data=event.data[:100] if event.data else None,
                        )
                        continue

            except (httpx.ReadError, httpx.ConnectError, httpx.RemoteProtocolError) as e:
                # Reset iterator on connection error
                self._event_iterator = None
                self._current_generator = None

                if self._closed:
                    raise StopAsyncIteration

                if self._retry_count >= self._max_retries:
                    self._log.error(
                        "max_retries_exceeded",
                        retries=self._retry_count,
                        error=str(e),
                    )
                    raise StreamingError(
                        f"Connection lost after {self._retry_count} retries: {e}",
                        retry_count=self._retry_count,
                        cause=e,
                    ) from e

                delay = min(
                    self._initial_delay * (self._backoff_factor**self._retry_count),
                    self._max_delay,
                )
                self._retry_count += 1

                self._log.warning(
                    "reconnecting",
                    retry=self._retry_count,
                    max_retries=self._max_retries,
                    delay=delay,
                    error=str(e),
                )

                await asyncio.sleep(delay)
                continue

            except httpx.TimeoutException as e:
                # Reset iterator on timeout
                self._event_iterator = None
                self._current_generator = None

                if self._closed:
                    raise StopAsyncIteration

                # Timeout during streaming, attempt reconnect
                self._log.warning("stream_timeout", error=str(e))
                continue

        raise StopAsyncIteration

    async def _iter_events(self) -> AsyncIterator[Any]:
        """
        Establish SSE connection and yield events.

        Uses httpx-sse for proper SSE handling.
        Maintains the connection context for the lifetime of iteration.
        """
        self._log.debug(
            "connecting",
            url=self._url,
            params=self._params,
        )

        event_source_ctx = aconnect_sse(
            self._http,
            "GET",
            self._url,
            params=self._params,
            timeout=self._timeout,
        )
        event_source = await event_source_ctx.__aenter__()
        # Store the response for potential cancellation
        self._current_response = event_source.response
        try:
            self._log.info("connected", url=self._url)

            async for event in event_source.aiter_sse():
                if self._closed:
                    break
                yield event
        except GeneratorExit:
            # Handle graceful shutdown when consumer stops iterating
            pass
        finally:
            self._current_response = None
            # Manually close the context manager to avoid issues with
            # generator cleanup during athrow()
            try:
                await event_source_ctx.__aexit__(None, None, None)
            except Exception:
                # Suppress any errors during cleanup
                pass

    async def close(self) -> None:
        """
        Close the event stream.

        Signals the iterator to stop and cleans up resources.
        Safe to call multiple times.
        """
        if self._closed:
            return

        self._closed = True
        
        # Close the underlying response to unblock the generator
        if self._current_response is not None:
            with suppress(Exception):
                await self._current_response.aclose()
            self._current_response = None
        
        # Close the async generator if it exists
        if self._current_generator is not None:
            with suppress(GeneratorExit, RuntimeError):
                await self._current_generator.aclose()
            self._current_generator = None
            self._event_iterator = None
        
        self._log.debug("stream_closed")

    async def __aenter__(self) -> "EventStream":
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit async context manager and close stream."""
        await self.close()

    @property
    def is_closed(self) -> bool:
        """Check if the stream is closed."""
        return self._closed

    @property
    def retry_count(self) -> int:
        """Get the current retry count."""
        return self._retry_count
