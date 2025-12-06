"""Sessions resource for managing chat sessions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from opencode._base import BaseResource
from opencode._pagination import AsyncPaginator
from opencode.models.common import FileDiff, ModelConfig
from opencode.models.message import MessageWithParts
from opencode.models.part import PartInput
from opencode.models.session import Permission, Session, SessionStatus, Todo

if TYPE_CHECKING:
    from opencode._client import OpenCode
    from opencode.resources.messages import MessagesResource


class SessionsResource(BaseResource):
    """
    Manage chat sessions.

    Sessions are the main container for conversations with the AI.
    Each session maintains its own context and message history.
    """

    async def list(self, *, directory: str | None = None) -> list[Session]:
        """
        List all sessions.

        Args:
            directory: Optional working directory override.

        Returns:
            List of all sessions.
        """
        self._log.debug("listing_sessions")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/session", params=params)
        sessions = [Session.model_validate(item) for item in data]
        self._log.info("sessions_listed", count=len(sessions))
        return sessions

    def list_iter(
        self,
        *,
        page_size: int = 50,
        directory: str | None = None,
    ) -> AsyncPaginator[Session]:
        """
        Iterate over all sessions with pagination.

        Args:
            page_size: Number of sessions to fetch per page.
            directory: Optional working directory override.

        Returns:
            Async paginator for iterating over sessions.
        """
        self._log.debug("creating_session_paginator", page_size=page_size)

        async def fetch_page(offset: int) -> list[Session]:
            params = self._build_params(
                directory=directory,
                offset=offset,
                limit=page_size,
            )
            data = await self._request("GET", "/session", params=params)
            return [Session.model_validate(item) for item in data]

        return AsyncPaginator(fetch_page, page_size=page_size)

    async def create(
        self,
        *,
        parent_id: str | None = None,
        title: str | None = None,
        directory: str | None = None,
    ) -> Session:
        """
        Create a new session.

        Args:
            parent_id: Optional parent session ID for creating child sessions.
            title: Optional title for the session.
            directory: Optional working directory override.

        Returns:
            The newly created session.
        """
        self._log.debug("creating_session", parent_id=parent_id, title=title)
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {}
        if parent_id is not None:
            body["parentID"] = parent_id
        if title is not None:
            body["title"] = title
        data = await self._request("POST", "/session", params=params, json_data=body)
        session = Session.model_validate(data)
        self._log.info("session_created", session_id=session.id)
        return session

    async def get(self, session_id: str, *, directory: str | None = None) -> Session:
        """
        Get a session by ID.

        Args:
            session_id: The session ID to retrieve.
            directory: Optional working directory override.

        Returns:
            The requested session.

        Raises:
            NotFoundError: If the session does not exist.
        """
        self._log.debug("getting_session", session_id=session_id)
        params = self._build_params(directory=directory)
        data = await self._request("GET", f"/session/{session_id}", params=params)
        session = Session.model_validate(data)
        self._log.debug("session_retrieved", session_id=session.id)
        return session

    async def update(
        self,
        session_id: str,
        *,
        title: str | None = None,
        directory: str | None = None,
    ) -> Session:
        """
        Update session properties.

        Args:
            session_id: The session ID to update.
            title: New title for the session.
            directory: Optional working directory override.

        Returns:
            The updated session.

        Raises:
            NotFoundError: If the session does not exist.
        """
        self._log.debug("updating_session", session_id=session_id, title=title)
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {}
        if title is not None:
            body["title"] = title
        data = await self._request(
            "PATCH", f"/session/{session_id}", params=params, json_data=body
        )
        session = Session.model_validate(data)
        self._log.info("session_updated", session_id=session.id)
        return session

    async def delete(self, session_id: str, *, directory: str | None = None) -> bool:
        """
        Delete a session.

        Args:
            session_id: The session ID to delete.
            directory: Optional working directory override.

        Returns:
            True if the session was deleted successfully.

        Raises:
            NotFoundError: If the session does not exist.
        """
        self._log.debug("deleting_session", session_id=session_id)
        params = self._build_params(directory=directory)
        await self._request("DELETE", f"/session/{session_id}", params=params)
        self._log.info("session_deleted", session_id=session_id)
        return True

    async def status(
        self, *, directory: str | None = None
    ) -> dict[str, SessionStatus]:
        """
        Get status of all sessions.

        Args:
            directory: Optional working directory override.

        Returns:
            Dictionary mapping session IDs to their status.
        """
        self._log.debug("getting_session_status")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/session/status", params=params)
        # The response is a dict of session_id -> status
        from opencode.models.session import (
            SessionStatusBusy,
            SessionStatusIdle,
            SessionStatusRetry,
        )

        result: dict[str, SessionStatus] = {}
        for session_id, status_data in data.items():
            status_type = status_data.get("type")
            if status_type == "idle":
                result[session_id] = SessionStatusIdle.model_validate(status_data)
            elif status_type == "busy":
                result[session_id] = SessionStatusBusy.model_validate(status_data)
            elif status_type == "retry":
                result[session_id] = SessionStatusRetry.model_validate(status_data)
        self._log.debug("session_status_retrieved", count=len(result))
        return result

    async def get_children(
        self, session_id: str, *, directory: str | None = None
    ) -> list[Session]:
        """
        Get child sessions.

        Args:
            session_id: The parent session ID.
            directory: Optional working directory override.

        Returns:
            List of child sessions.
        """
        self._log.debug("getting_session_children", session_id=session_id)
        params = self._build_params(directory=directory)
        data = await self._request(
            "GET", f"/session/{session_id}/children", params=params
        )
        children = [Session.model_validate(item) for item in data]
        self._log.debug(
            "session_children_retrieved", session_id=session_id, count=len(children)
        )
        return children

    async def get_todos(
        self, session_id: str, *, directory: str | None = None
    ) -> list[Todo]:
        """
        Get todo list for a session.

        Args:
            session_id: The session ID.
            directory: Optional working directory override.

        Returns:
            List of todo items for the session.
        """
        self._log.debug("getting_session_todos", session_id=session_id)
        params = self._build_params(directory=directory)
        data = await self._request("GET", f"/session/{session_id}/todo", params=params)
        todos = [Todo.model_validate(item) for item in data]
        self._log.debug(
            "session_todos_retrieved", session_id=session_id, count=len(todos)
        )
        return todos

    async def init(
        self,
        session_id: str,
        *,
        provider_id: str,
        model_id: str,
        message_id: str,
        directory: str | None = None,
    ) -> bool:
        """
        Initialize a session with AGENTS.md analysis.

        Args:
            session_id: The session ID to initialize.
            provider_id: The provider ID to use.
            model_id: The model ID to use.
            message_id: The message ID for initialization context.
            directory: Optional working directory override.

        Returns:
            True if initialization was successful.
        """
        self._log.debug(
            "initializing_session",
            session_id=session_id,
            provider_id=provider_id,
            model_id=model_id,
        )
        params = self._build_params(directory=directory)
        body = {
            "providerID": provider_id,
            "modelID": model_id,
            "messageID": message_id,
        }
        await self._request(
            "POST", f"/session/{session_id}/init", params=params, json_data=body
        )
        self._log.info("session_initialized", session_id=session_id)
        return True

    async def fork(
        self,
        session_id: str,
        *,
        message_id: str | None = None,
        directory: str | None = None,
    ) -> Session:
        """
        Fork a session at a specific message.

        Creates a new session that branches from the specified message,
        allowing exploration of alternative conversation paths.

        Args:
            session_id: The session ID to fork.
            message_id: Optional message ID to fork from. If not provided,
                       forks from the latest message.
            directory: Optional working directory override.

        Returns:
            The newly created forked session.
        """
        self._log.debug(
            "forking_session", session_id=session_id, message_id=message_id
        )
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {}
        if message_id is not None:
            body["messageID"] = message_id
        data = await self._request(
            "POST", f"/session/{session_id}/fork", params=params, json_data=body
        )
        session = Session.model_validate(data)
        self._log.info(
            "session_forked", session_id=session_id, forked_session_id=session.id
        )
        return session

    async def abort(self, session_id: str, *, directory: str | None = None) -> bool:
        """
        Abort a running session.

        Cancels any ongoing operations in the session.

        Args:
            session_id: The session ID to abort.
            directory: Optional working directory override.

        Returns:
            True if the session was aborted successfully.
        """
        self._log.debug("aborting_session", session_id=session_id)
        params = self._build_params(directory=directory)
        await self._request("POST", f"/session/{session_id}/abort", params=params)
        self._log.info("session_aborted", session_id=session_id)
        return True

    async def share(self, session_id: str, *, directory: str | None = None) -> Session:
        """
        Share a session publicly.

        Makes the session accessible via a public URL.

        Args:
            session_id: The session ID to share.
            directory: Optional working directory override.

        Returns:
            The updated session with share information.
        """
        self._log.debug("sharing_session", session_id=session_id)
        params = self._build_params(directory=directory)
        data = await self._request(
            "POST", f"/session/{session_id}/share", params=params
        )
        session = Session.model_validate(data)
        self._log.info("session_shared", session_id=session_id, url=session.share)
        return session

    async def unshare(
        self, session_id: str, *, directory: str | None = None
    ) -> Session:
        """
        Unshare a session.

        Removes public access to the session.

        Args:
            session_id: The session ID to unshare.
            directory: Optional working directory override.

        Returns:
            The updated session.
        """
        self._log.debug("unsharing_session", session_id=session_id)
        params = self._build_params(directory=directory)
        data = await self._request(
            "DELETE", f"/session/{session_id}/share", params=params
        )
        session = Session.model_validate(data)
        self._log.info("session_unshared", session_id=session_id)
        return session

    async def get_diff(
        self,
        session_id: str,
        *,
        message_id: str | None = None,
        directory: str | None = None,
    ) -> list[FileDiff]:
        """
        Get file diffs for the session.

        Returns all file changes made during the session or up to
        a specific message.

        Args:
            session_id: The session ID.
            message_id: Optional message ID to get diffs up to.
            directory: Optional working directory override.

        Returns:
            List of file diffs.
        """
        self._log.debug(
            "getting_session_diff", session_id=session_id, message_id=message_id
        )
        params = self._build_params(directory=directory, messageID=message_id)
        data = await self._request("GET", f"/session/{session_id}/diff", params=params)
        diffs = [FileDiff.model_validate(item) for item in data]
        self._log.debug(
            "session_diff_retrieved", session_id=session_id, count=len(diffs)
        )
        return diffs

    async def summarize(
        self,
        session_id: str,
        *,
        provider_id: str,
        model_id: str,
        directory: str | None = None,
    ) -> bool:
        """
        Summarize the session.

        Generates a summary of the session conversation.

        Args:
            session_id: The session ID to summarize.
            provider_id: The provider ID to use for summarization.
            model_id: The model ID to use for summarization.
            directory: Optional working directory override.

        Returns:
            True if summarization was successful.
        """
        self._log.debug(
            "summarizing_session",
            session_id=session_id,
            provider_id=provider_id,
            model_id=model_id,
        )
        params = self._build_params(directory=directory)
        body = {
            "providerID": provider_id,
            "modelID": model_id,
        }
        await self._request(
            "POST", f"/session/{session_id}/summarize", params=params, json_data=body
        )
        self._log.info("session_summarized", session_id=session_id)
        return True

    # =========================================================================
    # Message operations (convenience methods that call messages resource)
    # =========================================================================

    async def get_messages(
        self,
        session_id: str,
        *,
        limit: int | None = None,
        directory: str | None = None,
    ) -> list[MessageWithParts]:
        """
        Get messages for a session.

        Args:
            session_id: The session ID.
            limit: Maximum number of messages to return.
            directory: Optional working directory override.

        Returns:
            List of messages with their parts.
        """
        self._log.debug("getting_session_messages", session_id=session_id, limit=limit)
        params = self._build_params(directory=directory, limit=limit)
        data = await self._request(
            "GET", f"/session/{session_id}/message", params=params
        )
        messages = [MessageWithParts.model_validate(item) for item in data]
        self._log.debug(
            "session_messages_retrieved", session_id=session_id, count=len(messages)
        )
        return messages

    async def get_message(
        self,
        session_id: str,
        message_id: str,
        *,
        directory: str | None = None,
    ) -> MessageWithParts:
        """
        Get a specific message.

        Args:
            session_id: The session ID.
            message_id: The message ID to retrieve.
            directory: Optional working directory override.

        Returns:
            The requested message with its parts.

        Raises:
            NotFoundError: If the message does not exist.
        """
        self._log.debug(
            "getting_message", session_id=session_id, message_id=message_id
        )
        params = self._build_params(directory=directory)
        data = await self._request(
            "GET", f"/session/{session_id}/message/{message_id}", params=params
        )
        message = MessageWithParts.model_validate(data)
        self._log.debug("message_retrieved", message_id=message_id)
        return message

    async def prompt(
        self,
        session_id: str,
        *,
        parts: list[PartInput],
        model: ModelConfig | None = None,
        agent: str | None = None,
        system: str | None = None,
        tools: dict[str, bool] | None = None,
        message_id: str | None = None,
        no_reply: bool | None = None,
        directory: str | None = None,
    ) -> MessageWithParts:
        """
        Send a prompt and wait for response.

        This is the main method for interacting with the AI in a session.

        Args:
            session_id: The session ID.
            parts: The message parts to send.
            model: Optional model configuration override.
            agent: Optional agent name to use.
            system: Optional system prompt override.
            tools: Optional tools configuration (tool name -> enabled).
            message_id: Optional message ID (for retries or specific context).
            no_reply: If True, don't wait for AI response.
            directory: Optional working directory override.

        Returns:
            The assistant's response message with parts.
        """
        self._log.debug("sending_prompt", session_id=session_id, agent=agent)
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {
            "parts": [part.model_dump(by_alias=True, exclude_none=True) for part in parts]
        }
        if model is not None:
            body["model"] = model.model_dump(by_alias=True)
        if agent is not None:
            body["agent"] = agent
        if system is not None:
            body["system"] = system
        if tools is not None:
            body["tools"] = tools
        if message_id is not None:
            body["messageID"] = message_id
        if no_reply is not None:
            body["noReply"] = no_reply
        data = await self._request(
            "POST", f"/session/{session_id}/message", params=params, json_data=body
        )
        message = MessageWithParts.model_validate(data)
        self._log.info(
            "prompt_completed", session_id=session_id, message_id=message.info.id
        )
        return message

    async def prompt_async(
        self,
        session_id: str,
        *,
        parts: list[PartInput],
        model: ModelConfig | None = None,
        agent: str | None = None,
        message_id: str | None = None,
        no_reply: bool | None = None,
        system: str | None = None,
        tools: dict[str, bool] | None = None,
        directory: str | None = None,
    ) -> None:
        """
        Send a prompt without waiting (fire-and-forget).

        Use this when you don't need to wait for the response,
        for example when streaming events separately.

        Args:
            session_id: The session ID.
            parts: The message parts to send.
            model: Optional model configuration override.
            agent: Optional agent name to use.
            message_id: Optional message ID.
            no_reply: If True, don't generate AI response.
            system: Optional system prompt override.
            tools: Optional tools configuration.
            directory: Optional working directory override.
        """
        self._log.debug("sending_prompt_async", session_id=session_id, agent=agent)
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {
            "parts": [part.model_dump(by_alias=True, exclude_none=True) for part in parts]
        }
        if model is not None:
            body["model"] = model.model_dump(by_alias=True)
        if agent is not None:
            body["agent"] = agent
        if message_id is not None:
            body["messageID"] = message_id
        if no_reply is not None:
            body["noReply"] = no_reply
        if system is not None:
            body["system"] = system
        if tools is not None:
            body["tools"] = tools
        await self._request(
            "POST", f"/session/{session_id}/prompt_async", params=params, json_data=body
        )
        self._log.debug("prompt_async_sent", session_id=session_id)

    async def command(
        self,
        session_id: str,
        *,
        command: str,
        arguments: str,
        agent: str | None = None,
        model: str | None = None,
        message_id: str | None = None,
        directory: str | None = None,
    ) -> MessageWithParts:
        """
        Execute a command in the session.

        Commands are special operations like /clear, /help, etc.

        Args:
            session_id: The session ID.
            command: The command name (without /).
            arguments: Command arguments as a string.
            agent: Optional agent name.
            model: Optional model ID.
            message_id: Optional message ID.
            directory: Optional working directory override.

        Returns:
            The response message.
        """
        self._log.debug(
            "executing_command", session_id=session_id, command=command
        )
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {
            "command": command,
            "arguments": arguments,
        }
        if agent is not None:
            body["agent"] = agent
        if model is not None:
            body["model"] = model
        if message_id is not None:
            body["messageID"] = message_id
        data = await self._request(
            "POST", f"/session/{session_id}/command", params=params, json_data=body
        )
        message = MessageWithParts.model_validate(data)
        self._log.info(
            "command_executed", session_id=session_id, command=command
        )
        return message

    async def shell(
        self,
        session_id: str,
        *,
        command: str,
        agent: str,
        model: ModelConfig | None = None,
        directory: str | None = None,
    ) -> Any:
        """
        Run a shell command.

        Executes a shell command within the session context.

        Args:
            session_id: The session ID.
            command: The shell command to execute.
            agent: The agent name to use.
            model: Optional model configuration.
            directory: Optional working directory override.

        Returns:
            The command result (AssistantMessage).
        """
        self._log.debug(
            "running_shell_command", session_id=session_id, command=command
        )
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {
            "command": command,
            "agent": agent,
        }
        if model is not None:
            body["model"] = model.model_dump(by_alias=True)
        data = await self._request(
            "POST", f"/session/{session_id}/shell", params=params, json_data=body
        )
        self._log.info("shell_command_completed", session_id=session_id)
        return data

    async def revert(
        self,
        session_id: str,
        *,
        message_id: str,
        part_id: str | None = None,
        directory: str | None = None,
    ) -> Session:
        """
        Revert to a previous message.

        Rolls back the session state to a specific point in the
        conversation history.

        Args:
            session_id: The session ID.
            message_id: The message ID to revert to.
            part_id: Optional specific part ID within the message.
            directory: Optional working directory override.

        Returns:
            The updated session.
        """
        self._log.debug(
            "reverting_session",
            session_id=session_id,
            message_id=message_id,
            part_id=part_id,
        )
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {"messageID": message_id}
        if part_id is not None:
            body["partID"] = part_id
        data = await self._request(
            "POST", f"/session/{session_id}/revert", params=params, json_data=body
        )
        session = Session.model_validate(data)
        self._log.info(
            "session_reverted", session_id=session_id, message_id=message_id
        )
        return session

    async def unrevert(
        self, session_id: str, *, directory: str | None = None
    ) -> Session:
        """
        Restore reverted messages.

        Undoes a previous revert operation.

        Args:
            session_id: The session ID.
            directory: Optional working directory override.

        Returns:
            The updated session.
        """
        self._log.debug("unreverting_session", session_id=session_id)
        params = self._build_params(directory=directory)
        data = await self._request(
            "POST", f"/session/{session_id}/unrevert", params=params
        )
        session = Session.model_validate(data)
        self._log.info("session_unreverted", session_id=session_id)
        return session

    async def respond_to_permission(
        self,
        session_id: str,
        permission_id: str,
        *,
        response: str,
        directory: str | None = None,
    ) -> bool:
        """
        Respond to a permission request.

        When the AI requests permission to perform certain actions,
        this method allows you to approve or reject the request.

        Args:
            session_id: The session ID.
            permission_id: The permission request ID.
            response: One of "once", "always", or "reject".
            directory: Optional working directory override.

        Returns:
            True if the response was recorded successfully.

        Raises:
            ValueError: If response is not a valid value.
        """
        valid_responses = {"once", "always", "reject"}
        if response not in valid_responses:
            raise ValueError(
                f"Invalid response '{response}'. Must be one of: {valid_responses}"
            )
        self._log.debug(
            "responding_to_permission",
            session_id=session_id,
            permission_id=permission_id,
            response=response,
        )
        params = self._build_params(directory=directory)
        body = {"response": response}
        await self._request(
            "POST",
            f"/session/{session_id}/permissions/{permission_id}",
            params=params,
            json_data=body,
        )
        self._log.info(
            "permission_responded",
            session_id=session_id,
            permission_id=permission_id,
            response=response,
        )
        return True

    def messages(self, session_id: str) -> "MessagesResource":
        """
        Get a messages resource scoped to this session.

        Provides a more focused interface for working with messages
        in a specific session.

        Args:
            session_id: The session ID.

        Returns:
            A MessagesResource scoped to the specified session.
        """
        from opencode.resources.messages import MessagesResource

        return MessagesResource(self._client, session_id)
