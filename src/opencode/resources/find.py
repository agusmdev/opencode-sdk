"""Find resource for search operations.

This module provides the FindResource class for performing various search
operations through the OpenCode API, including text search, file search,
and symbol search across the project.
"""
from __future__ import annotations

from typing import Any

from opencode._base import BaseResource
from opencode.models.file import Symbol


class FindResource(BaseResource):
    """Search for text, files, and symbols.

    This resource provides methods for searching across the project,
    including full-text search within files, fuzzy file name matching,
    and symbol search for code navigation.

    Example:
        ```python
        async with OpenCodeClient() as client:
            # Search for text in files
            matches = await client.find.text("TODO")

            # Find files by name
            files = await client.find.files("main")

            # Search for symbols
            symbols = await client.find.symbols("MyClass")
        ```
    """

    async def text(
        self, pattern: str, *, directory: str | None = None
    ) -> list[dict[str, Any]]:
        """Search for text pattern in files.

        Performs a full-text search across all files in the project,
        returning matches for the specified pattern. Supports regular
        expression patterns for advanced searching.

        Args:
            pattern: The text pattern to search for. Can be a plain string
                or a regular expression pattern.
            directory: Optional project directory context for the request.

        Returns:
            A list of dictionaries containing match information, including
            file paths, line numbers, and matched content.

        Raises:
            OpenCodeError: If the search fails or the pattern is invalid.

        Example:
            ```python
            # Search for TODO comments
            matches = await client.find.text("TODO:")
            for match in matches:
                print(f"{match['file']}:{match['line']}: {match['content']}")

            # Search with regex
            matches = await client.find.text(r"def \\w+\\(self")
            ```
        """
        params = self._build_params(directory=directory, pattern=pattern)
        return await self._request("GET", "/find", params=params)

    async def files(
        self,
        query: str,
        *,
        include_dirs: bool = False,
        directory: str | None = None,
    ) -> list[str]:
        """Find files matching a query.

        Searches for files whose names match the specified query. Uses
        fuzzy matching to find files even with partial or approximate
        name matches.

        Args:
            query: The search query for file names. Supports fuzzy matching
                for flexible searching.
            include_dirs: If True, include directories in the results.
                Defaults to False (files only).
            directory: Optional project directory context for the request.

        Returns:
            A list of file paths that match the query.

        Raises:
            OpenCodeError: If the search fails.

        Example:
            ```python
            # Find Python files containing "test" in the name
            files = await client.find.files("test.py")
            for path in files:
                print(path)

            # Include directories in search
            paths = await client.find.files("src", include_dirs=True)
            ```
        """
        params = self._build_params(
            directory=directory, query=query, dirs="true" if include_dirs else "false"
        )
        return await self._request("GET", "/find/file", params=params)

    async def symbols(
        self, query: str, *, directory: str | None = None
    ) -> list[Symbol]:
        """Find workspace symbols.

        Searches for code symbols (classes, functions, variables, etc.)
        across the project. This is useful for code navigation and
        understanding project structure.

        Args:
            query: The search query for symbol names. Supports fuzzy matching
                for flexible searching.
            directory: Optional project directory context for the request.

        Returns:
            A list of Symbol objects representing matching symbols, including
            their names, types, locations, and container information.

        Raises:
            OpenCodeError: If the search fails.

        Example:
            ```python
            # Find all symbols matching "Handler"
            symbols = await client.find.symbols("Handler")
            for symbol in symbols:
                print(f"{symbol.kind}: {symbol.name} in {symbol.location}")

            # Find class definitions
            classes = await client.find.symbols("class")
            ```
        """
        params = self._build_params(directory=directory, query=query)
        data = await self._request("GET", "/find/symbol", params=params)
        return [Symbol.model_validate(item) for item in data]
