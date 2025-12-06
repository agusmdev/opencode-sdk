"""
OpenCode Python SDK

Official Python SDK for the OpenCode API. Provides a fully typed,
async-first interface with streaming support.

Example:
    >>> import asyncio
    >>> from opencode import OpenCode
    >>> from opencode.models import TextPartInput
    >>>
    >>> async def main():
    ...     async with OpenCode() as client:
    ...         session = await client.sessions.create(title="My Session")
    ...         response = await client.sessions.prompt(
    ...             session.id,
    ...             parts=[TextPartInput(type="text", text="Hello!")]
    ...         )
    ...         print(response)
    >>>
    >>> asyncio.run(main())
"""

from opencode._client import OpenCode
from opencode._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConnectionError,
    NotFoundError,
    OpenCodeError,
    RateLimitError,
    ServerError,
    StreamingError,
    ValidationError,
)
from opencode._logging import configure_logging, get_logger
from opencode._pagination import AsyncPaginator, CursorPaginator
from opencode._streaming import EventStream

__version__ = "0.1.0"

__all__ = [
    # Main client
    "OpenCode",
    # Streaming
    "EventStream",
    # Pagination
    "AsyncPaginator",
    "CursorPaginator",
    # Exceptions
    "OpenCodeError",
    "APIError",
    "BadRequestError",
    "NotFoundError",
    "AuthenticationError",
    "RateLimitError",
    "ServerError",
    "StreamingError",
    "ConnectionError",
    "ValidationError",
    # Logging
    "configure_logging",
    "get_logger",
    # Version
    "__version__",
]
