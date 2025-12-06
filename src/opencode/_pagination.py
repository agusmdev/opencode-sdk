"""Async pagination helpers for the SDK."""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Generic, TypeVar

from opencode._constants import DEFAULT_PAGE_SIZE
from opencode._logging import get_logger

T = TypeVar("T")


class AsyncPaginator(Generic[T], AsyncIterator[T]):
    """
    Async iterator for paginated API resources.
    
    Automatically fetches pages as needed and yields items one by one.
    Supports memory-efficient iteration over large collections.
    
    Example:
        async for session in client.sessions.list_iter():
            print(session.id)
    """

    def __init__(
        self,
        fetch_page: Callable[[int], Awaitable[list[T]]],
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> None:
        """
        Initialize the paginator.
        
        Args:
            fetch_page: Async function that takes an offset and returns a page of items
            page_size: Number of items to fetch per page
        """
        self._fetch_page = fetch_page
        self._page_size = page_size
        self._buffer: list[T] = []
        self._offset = 0
        self._exhausted = False
        self._log = get_logger("opencode.pagination")

    def __aiter__(self) -> "AsyncPaginator[T]":
        """Return self as async iterator."""
        return self

    async def __anext__(self) -> T:
        """
        Get the next item.
        
        Fetches a new page when the buffer is empty.
        
        Returns:
            The next item
            
        Raises:
            StopAsyncIteration: When all items have been yielded
        """
        # Fetch more items if buffer is empty and not exhausted
        if not self._buffer and not self._exhausted:
            self._log.debug(
                "fetching_page",
                offset=self._offset,
                page_size=self._page_size,
            )
            
            page = await self._fetch_page(self._offset)
            
            self._log.debug(
                "page_fetched",
                offset=self._offset,
                items_count=len(page),
            )
            
            # If we got fewer items than page_size, we've reached the end
            if len(page) < self._page_size:
                self._exhausted = True
                
            self._buffer.extend(page)
            self._offset += len(page)

        # If buffer is still empty, we're done
        if not self._buffer:
            raise StopAsyncIteration

        return self._buffer.pop(0)

    async def collect(self) -> list[T]:
        """
        Collect all items into a list.
        
        Useful when you need all items at once.
        
        Returns:
            List of all items
            
        Warning:
            This loads all items into memory. For large collections,
            prefer iterating directly.
        """
        items: list[T] = []
        async for item in self:
            items.append(item)
        return items

    async def first(self) -> T | None:
        """
        Get the first item or None.
        
        Returns:
            The first item, or None if empty
        """
        try:
            return await self.__anext__()
        except StopAsyncIteration:
            return None

    async def take(self, n: int) -> list[T]:
        """
        Take up to n items.
        
        Args:
            n: Maximum number of items to take
            
        Returns:
            List of up to n items
        """
        items: list[T] = []
        count = 0
        async for item in self:
            items.append(item)
            count += 1
            if count >= n:
                break
        return items


class CursorPaginator(Generic[T], AsyncIterator[T]):
    """
    Async iterator for cursor-based pagination.
    
    Some APIs use cursor tokens instead of offsets.
    This paginator handles that pattern.
    """

    def __init__(
        self,
        fetch_page: Callable[[str | None], Awaitable[tuple[list[T], str | None]]],
    ) -> None:
        """
        Initialize the cursor paginator.
        
        Args:
            fetch_page: Async function that takes a cursor and returns 
                        (items, next_cursor). next_cursor is None when done.
        """
        self._fetch_page = fetch_page
        self._buffer: list[T] = []
        self._cursor: str | None = None
        self._started = False
        self._exhausted = False
        self._log = get_logger("opencode.pagination")

    def __aiter__(self) -> "CursorPaginator[T]":
        """Return self as async iterator."""
        return self

    async def __anext__(self) -> T:
        """Get the next item."""
        if not self._buffer and not self._exhausted:
            # Only pass cursor after first request
            cursor = self._cursor if self._started else None
            self._started = True
            
            self._log.debug("fetching_page", cursor=cursor)
            
            items, next_cursor = await self._fetch_page(cursor)
            
            self._log.debug(
                "page_fetched",
                items_count=len(items),
                has_next=next_cursor is not None,
            )
            
            self._cursor = next_cursor
            if next_cursor is None:
                self._exhausted = True
                
            self._buffer.extend(items)

        if not self._buffer:
            raise StopAsyncIteration

        return self._buffer.pop(0)

    async def collect(self) -> list[T]:
        """Collect all items into a list."""
        items: list[T] = []
        async for item in self:
            items.append(item)
        return items
