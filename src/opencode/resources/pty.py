"""PTY resource for pseudo-terminal session management.

This module provides the PtyResource class for managing PTY (pseudo-terminal)
sessions through the OpenCode API. PTY sessions allow interactive command-line
access to the server environment.
"""
from __future__ import annotations

from typing import Any

from opencode._base import BaseResource
from opencode.models.pty import Pty


class PtyResource(BaseResource):
    """Manage PTY (pseudo-terminal) sessions.

    This resource provides methods for creating, listing, updating, and
    managing pseudo-terminal sessions. PTY sessions enable interactive
    shell access and command execution within the OpenCode environment.

    Example:
        ```python
        async with OpenCodeClient() as client:
            # Create a new PTY session
            pty = await client.pty.create(command="/bin/bash", title="My Shell")

            # List all sessions
            sessions = await client.pty.list()

            # Update session dimensions
            await client.pty.update(pty.id, rows=24, cols=80)

            # Remove session when done
            await client.pty.remove(pty.id)
        ```
    """

    async def list(self, *, directory: str | None = None) -> list[Pty]:
        """List all PTY sessions.

        Retrieves a list of all active pseudo-terminal sessions.

        Args:
            directory: Optional project directory context for the request.

        Returns:
            A list of Pty objects representing all active PTY sessions.

        Raises:
            OpenCodeError: If the API request fails.

        Example:
            ```python
            sessions = await client.pty.list()
            for session in sessions:
                print(f"Session {session.id}: {session.title}")
            ```
        """
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/pty", params=params)
        return [Pty.model_validate(item) for item in data]

    async def create(
        self,
        *,
        command: str | None = None,
        args: list[str] | None = None,
        cwd: str | None = None,
        title: str | None = None,
        env: dict[str, str] | None = None,
        directory: str | None = None,
    ) -> Pty:
        """Create a new PTY session.

        Creates a new pseudo-terminal session with the specified configuration.
        If no command is provided, a default shell will be started.

        Args:
            command: The command to execute in the PTY (e.g., "/bin/bash").
                If not provided, the system default shell is used.
            args: Optional list of arguments to pass to the command.
            cwd: The working directory for the PTY session.
            title: A human-readable title for the session.
            env: Additional environment variables to set in the PTY.
            directory: Optional project directory context for the request.

        Returns:
            A Pty object representing the newly created session.

        Raises:
            OpenCodeError: If the PTY session cannot be created.

        Example:
            ```python
            # Create a bash session
            pty = await client.pty.create(
                command="/bin/bash",
                title="Development Shell",
                cwd="/home/user/project",
                env={"NODE_ENV": "development"}
            )
            ```
        """
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {}
        if command:
            body["command"] = command
        if args:
            body["args"] = args
        if cwd:
            body["cwd"] = cwd
        if title:
            body["title"] = title
        if env:
            body["env"] = env
        data = await self._request("POST", "/pty", params=params, json_data=body)
        return Pty.model_validate(data)

    async def get(self, pty_id: str, *, directory: str | None = None) -> Pty:
        """Get PTY session info.

        Retrieves detailed information about a specific PTY session.

        Args:
            pty_id: The unique identifier of the PTY session.
            directory: Optional project directory context for the request.

        Returns:
            A Pty object containing the session details.

        Raises:
            OpenCodeError: If the session is not found or the request fails.

        Example:
            ```python
            pty = await client.pty.get("pty-abc123")
            print(f"Title: {pty.title}, Status: {pty.status}")
            ```
        """
        params = self._build_params(directory=directory)
        data = await self._request("GET", f"/pty/{pty_id}", params=params)
        return Pty.model_validate(data)

    async def update(
        self,
        pty_id: str,
        *,
        title: str | None = None,
        rows: int | None = None,
        cols: int | None = None,
        directory: str | None = None,
    ) -> Pty:
        """Update PTY session.

        Updates the properties of an existing PTY session, such as its
        title or terminal dimensions.

        Args:
            pty_id: The unique identifier of the PTY session to update.
            title: New title for the session.
            rows: Number of rows for terminal dimensions. Must be provided
                together with cols.
            cols: Number of columns for terminal dimensions. Must be provided
                together with rows.
            directory: Optional project directory context for the request.

        Returns:
            The updated Pty object.

        Raises:
            OpenCodeError: If the session is not found or the update fails.

        Example:
            ```python
            # Resize the terminal
            pty = await client.pty.update("pty-abc123", rows=24, cols=80)

            # Update the title
            pty = await client.pty.update("pty-abc123", title="Renamed Shell")
            ```
        """
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {}
        if title:
            body["title"] = title
        if rows is not None and cols is not None:
            body["size"] = {"rows": rows, "cols": cols}
        data = await self._request("PUT", f"/pty/{pty_id}", params=params, json_data=body)
        return Pty.model_validate(data)

    async def remove(self, pty_id: str, *, directory: str | None = None) -> bool:
        """Remove a PTY session.

        Terminates and removes an existing PTY session. This will close
        any running processes in the session.

        Args:
            pty_id: The unique identifier of the PTY session to remove.
            directory: Optional project directory context for the request.

        Returns:
            True if the session was successfully removed.

        Raises:
            OpenCodeError: If the session is not found or cannot be removed.

        Example:
            ```python
            success = await client.pty.remove("pty-abc123")
            if success:
                print("Session terminated")
            ```
        """
        params = self._build_params(directory=directory)
        return await self._request("DELETE", f"/pty/{pty_id}", params=params)

    async def connect(self, pty_id: str, *, directory: str | None = None) -> bool:
        """Connect to a PTY session.

        Establishes a connection to an existing PTY session for interactive
        communication. This is typically used to attach to a running session.

        Args:
            pty_id: The unique identifier of the PTY session to connect to.
            directory: Optional project directory context for the request.

        Returns:
            True if the connection was successfully established.

        Raises:
            OpenCodeError: If the session is not found or connection fails.

        Example:
            ```python
            connected = await client.pty.connect("pty-abc123")
            if connected:
                print("Connected to PTY session")
            ```
        """
        params = self._build_params(directory=directory)
        return await self._request("GET", f"/pty/{pty_id}/connect", params=params)
