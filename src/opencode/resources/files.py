"""Files resource for file operations.

This module provides the FilesResource class for performing file system
operations through the OpenCode API, including listing directories,
reading file contents, and checking file modification status.
"""
from __future__ import annotations

from opencode._base import BaseResource
from opencode.models.file import File, FileContent, FileNode


class FilesResource(BaseResource):
    """Access file system operations.

    This resource provides methods for interacting with the file system,
    including listing directory contents, reading files, and checking
    the status of modified files in the project.

    Example:
        ```python
        async with OpenCodeClient() as client:
            # List files in a directory
            nodes = await client.files.list("/src")

            # Read a specific file
            content = await client.files.read("/src/main.py")

            # Check modified files
            modified = await client.files.status()
        ```
    """

    async def list(self, path: str, *, directory: str | None = None) -> list[FileNode]:
        """List files and directories at a path.

        Retrieves a list of all files and subdirectories at the specified
        path. Each node includes metadata such as name, type, and size.

        Args:
            path: The path to list contents from (relative to project root
                or absolute path).
            directory: Optional project directory context for the request.

        Returns:
            A list of FileNode objects representing files and directories
            at the specified path.

        Raises:
            OpenCodeError: If the path is not found or the request fails.

        Example:
            ```python
            # List contents of the src directory
            nodes = await client.files.list("/src")
            for node in nodes:
                if node.is_directory:
                    print(f"[DIR]  {node.name}")
                else:
                    print(f"[FILE] {node.name} ({node.size} bytes)")
            ```
        """
        params = self._build_params(directory=directory, path=path)
        data = await self._request("GET", "/file", params=params)
        return [FileNode.model_validate(item) for item in data]

    async def read(self, path: str, *, directory: str | None = None) -> FileContent:
        """Read file content.

        Retrieves the contents of a file at the specified path. This method
        is suitable for reading text files and returns the content along
        with file metadata.

        Args:
            path: The path to the file to read (relative to project root
                or absolute path).
            directory: Optional project directory context for the request.

        Returns:
            A FileContent object containing the file's content and metadata.

        Raises:
            OpenCodeError: If the file is not found, is not readable,
                or the request fails.

        Example:
            ```python
            # Read a Python file
            file_content = await client.files.read("/src/main.py")
            print(f"File: {file_content.path}")
            print(f"Content:\\n{file_content.content}")
            ```
        """
        params = self._build_params(directory=directory, path=path)
        data = await self._request("GET", "/file/content", params=params)
        return FileContent.model_validate(data)

    async def status(self, *, directory: str | None = None) -> list[File]:
        """Get status of modified files.

        Retrieves a list of files that have been modified in the project.
        This is useful for tracking changes and identifying uncommitted
        modifications.

        Args:
            directory: Optional project directory context for the request.

        Returns:
            A list of File objects representing modified files, including
            their modification status.

        Raises:
            OpenCodeError: If the request fails.

        Example:
            ```python
            # Get all modified files
            modified_files = await client.files.status()
            for file in modified_files:
                print(f"{file.status}: {file.path}")
            ```
        """
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/file/status", params=params)
        return [File.model_validate(item) for item in data]
