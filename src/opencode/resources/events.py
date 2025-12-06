"""Events resource for real-time event streaming."""

from __future__ import annotations

from typing import TYPE_CHECKING

from opencode._base import BaseResource
from opencode._streaming import EventStream

if TYPE_CHECKING:
    from opencode._client import OpenCode
    from opencode.models.event import Event, GlobalEvent


class EventsResource(BaseResource):
    """
    Subscribe to real-time events via Server-Sent Events (SSE).
    
    Events are streamed as they occur, enabling real-time updates
    for session status changes, message updates, file edits, and more.
    
    Example:
        async for event in client.events.subscribe():
            match event:
                case MessagePartUpdatedEvent(properties=p):
                    if p.delta:
                        print(p.delta, end="", flush=True)
                case SessionIdleEvent():
                    print("\\n--- Complete ---")
                    break
    """

    def subscribe(
        self,
        *,
        directory: str | None = None,
        max_retries: int = 5,
        reconnect: bool = True,
    ) -> EventStream:
        """
        Subscribe to project events.
        
        Returns an async iterator that yields Event objects.
        Automatically reconnects on connection loss.
        
        Args:
            directory: Project directory (uses client default if not set)
            max_retries: Maximum reconnection attempts
            reconnect: Whether to automatically reconnect on errors
            
        Returns:
            EventStream: Async iterator of events
            
        Example:
            async with client.events.subscribe() as stream:
                async for event in stream:
                    print(event.type)
        """
        params = self._build_params(directory=directory)
        
        self._log.info(
            "subscribing_to_events",
            url="/event",
            directory=params.get("directory"),
            max_retries=max_retries if reconnect else 0,
        )
        
        return EventStream(
            http_client=self._http,
            url="/event",
            params=params,
            max_retries=max_retries if reconnect else 0,
        )

    def subscribe_global(
        self,
        *,
        max_retries: int = 5,
        reconnect: bool = True,
    ) -> EventStream:
        """
        Subscribe to global events across all projects.
        
        Global events include the project directory in each event,
        allowing you to track activity across multiple projects.
        
        Args:
            max_retries: Maximum reconnection attempts
            reconnect: Whether to automatically reconnect on errors
            
        Returns:
            EventStream: Async iterator of GlobalEvent objects
        """
        self._log.info(
            "subscribing_to_global_events",
            url="/global/event",
            max_retries=max_retries if reconnect else 0,
        )
        
        return EventStream(
            http_client=self._http,
            url="/global/event",
            params={},
            max_retries=max_retries if reconnect else 0,
        )
