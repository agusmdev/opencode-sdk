"""TUI resource for terminal UI control."""

from __future__ import annotations

from typing import Any, Literal

from opencode._base import BaseResource


class TuiResource(BaseResource):
    """
    Control the OpenCode TUI (Terminal User Interface).

    This resource provides programmatic control over the OpenCode terminal
    user interface, enabling integrations and automation workflows. Use these
    methods to manipulate the prompt, open dialogs, show notifications,
    and interact with the TUI event system.

    Example:
        # Append text to the prompt and submit
        await client.tui.append_prompt("Fix the bug in main.py")
        await client.tui.submit_prompt()

        # Show a notification
        await client.tui.show_toast(
            "Build completed",
            "success",
            title="Build Status",
            duration=3000
        )

        # Open a dialog
        await client.tui.open_models()
    """

    async def append_prompt(self, text: str, *, directory: str | None = None) -> bool:
        """
        Append text to the current prompt input.

        Adds the specified text to the end of whatever is currently
        in the prompt input field without clearing existing content.

        Args:
            text: The text to append to the current prompt.
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the operation was successful, False otherwise.

        Example:
            await client.tui.append_prompt("Explain this function")
            await client.tui.append_prompt(" in detail")  # Appends more text
        """
        params = self._build_params(directory=directory)
        return await self._request(
            "POST", "/tui/append-prompt", params=params, json_data={"text": text}
        )

    async def clear_prompt(self, *, directory: str | None = None) -> bool:
        """
        Clear the current prompt input.

        Removes all text from the prompt input field, resetting it
        to an empty state.

        Args:
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the operation was successful, False otherwise.

        Example:
            await client.tui.clear_prompt()  # Start fresh
            await client.tui.append_prompt("New prompt text")
        """
        params = self._build_params(directory=directory)
        return await self._request("POST", "/tui/clear-prompt", params=params)

    async def submit_prompt(self, *, directory: str | None = None) -> bool:
        """
        Submit the current prompt for processing.

        Triggers the submission of whatever text is currently in the
        prompt input field, as if the user pressed Enter. The prompt
        will be sent to the active session for processing.

        Args:
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the operation was successful, False otherwise.

        Example:
            await client.tui.append_prompt("What does this code do?")
            await client.tui.submit_prompt()  # Send to the LLM
        """
        params = self._build_params(directory=directory)
        return await self._request("POST", "/tui/submit-prompt", params=params)

    async def open_help(self, *, directory: str | None = None) -> bool:
        """
        Open the help dialog in the TUI.

        Displays the help dialog showing available keyboard shortcuts,
        commands, and usage information.

        Args:
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the operation was successful, False otherwise.

        Example:
            await client.tui.open_help()  # Show help information
        """
        params = self._build_params(directory=directory)
        return await self._request("POST", "/tui/open-help", params=params)

    async def open_sessions(self, *, directory: str | None = None) -> bool:
        """
        Open the sessions dialog in the TUI.

        Displays the sessions picker dialog, allowing selection between
        existing sessions or creation of new ones.

        Args:
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the operation was successful, False otherwise.

        Example:
            await client.tui.open_sessions()  # Show session picker
        """
        params = self._build_params(directory=directory)
        return await self._request("POST", "/tui/open-sessions", params=params)

    async def open_themes(self, *, directory: str | None = None) -> bool:
        """
        Open the themes dialog in the TUI.

        Displays the theme picker dialog for changing the TUI's
        color scheme and visual appearance.

        Args:
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the operation was successful, False otherwise.

        Example:
            await client.tui.open_themes()  # Show theme picker
        """
        params = self._build_params(directory=directory)
        return await self._request("POST", "/tui/open-themes", params=params)

    async def open_models(self, *, directory: str | None = None) -> bool:
        """
        Open the models dialog in the TUI.

        Displays the model picker dialog for selecting which AI model
        to use for generating responses.

        Args:
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the operation was successful, False otherwise.

        Example:
            await client.tui.open_models()  # Show model picker
        """
        params = self._build_params(directory=directory)
        return await self._request("POST", "/tui/open-models", params=params)

    async def execute_command(
        self, command: str, *, directory: str | None = None
    ) -> bool:
        """
        Execute a TUI command.

        Runs a slash command or internal TUI command as if it were
        typed by the user. This allows programmatic execution of
        any command supported by the TUI.

        Args:
            command: The command to execute (e.g., "/clear", "/compact").
                Should include the leading slash for slash commands.
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the operation was successful, False otherwise.

        Example:
            await client.tui.execute_command("/clear")  # Clear conversation
            await client.tui.execute_command("/compact")  # Toggle compact mode
        """
        params = self._build_params(directory=directory)
        return await self._request(
            "POST", "/tui/execute-command", params=params, json_data={"command": command}
        )

    async def show_toast(
        self,
        message: str,
        variant: Literal["info", "success", "warning", "error"],
        *,
        title: str | None = None,
        duration: int | None = None,
        directory: str | None = None,
    ) -> bool:
        """
        Show a toast notification in the TUI.

        Displays a temporary notification message to the user with
        the specified styling and optional title.

        Args:
            message: The main notification message to display.
            variant: The type of notification, which affects styling:
                - "info": Neutral informational message
                - "success": Positive confirmation (e.g., green styling)
                - "warning": Caution message (e.g., yellow styling)
                - "error": Error or failure message (e.g., red styling)
            title: Optional title displayed above the message.
            duration: Optional display duration in milliseconds.
                If not specified, uses the default duration.
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the operation was successful, False otherwise.

        Example:
            # Simple notification
            await client.tui.show_toast("File saved", "success")

            # Detailed notification with title and duration
            await client.tui.show_toast(
                "Check the logs for details",
                "warning",
                title="Build Warning",
                duration=5000  # 5 seconds
            )
        """
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {"message": message, "variant": variant}
        if title:
            body["title"] = title
        if duration:
            body["duration"] = duration
        return await self._request(
            "POST", "/tui/show-toast", params=params, json_data=body
        )

    async def publish(
        self, event: dict[str, Any], *, directory: str | None = None
    ) -> bool:
        """
        Publish a custom event to the TUI event bus.

        Sends a custom event that can be received by TUI components
        or other integrations listening on the event bus. This enables
        custom inter-component communication.

        Args:
            event: The event payload as a dictionary. The structure
                depends on the event type being published.
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the event was published successfully, False otherwise.

        Example:
            await client.tui.publish({
                "type": "custom.notification",
                "data": {"message": "Task completed"}
            })
        """
        params = self._build_params(directory=directory)
        return await self._request(
            "POST", "/tui/publish", params=params, json_data=event
        )

    async def get_next_request(
        self, *, directory: str | None = None
    ) -> dict[str, Any] | None:
        """
        Get the next pending TUI control request from the queue.

        Retrieves the next request that requires a response from the
        control queue. This is used by external controllers to receive
        requests that need processing.

        This is typically used in a polling loop by external processes
        that need to respond to TUI requests.

        Args:
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            A dictionary containing the request details, or None if
            no requests are pending in the queue.

        Example:
            # Poll for requests and process them
            while True:
                request = await client.tui.get_next_request()
                if request:
                    # Process the request
                    result = process_request(request)
                    await client.tui.submit_response(result)
                await asyncio.sleep(0.1)  # Brief pause between polls
        """
        params = self._build_params(directory=directory)
        return await self._request("GET", "/tui/control/next", params=params)

    async def submit_response(
        self, response: Any, *, directory: str | None = None
    ) -> bool:
        """
        Submit a response to a TUI control request.

        Sends a response back to the TUI for a previously received
        control request. This completes the request-response cycle
        for external TUI controllers.

        Args:
            response: The response payload. The structure should match
                what the original request expects.
            directory: Project directory override. If not specified,
                uses the client's default directory.

        Returns:
            True if the response was submitted successfully, False otherwise.

        Example:
            # Get a request and submit a response
            request = await client.tui.get_next_request()
            if request:
                result = {"status": "completed", "data": process(request)}
                await client.tui.submit_response(result)
        """
        params = self._build_params(directory=directory)
        return await self._request(
            "POST", "/tui/control/response", params=params, json_data=response
        )
