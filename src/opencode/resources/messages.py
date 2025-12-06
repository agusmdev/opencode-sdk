"""Messages resource for session message operations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from opencode._base import BaseResource
from opencode._pagination import AsyncPaginator
from opencode.models.common import ModelConfig
from opencode.models.message import MessageWithParts
from opencode.models.part import PartInput

if TYPE_CHECKING:
    from opencode._client import OpenCode


class MessagesResource:
    """
    Access messages within a specific session.

    This resource is scoped to a session ID and provides methods for listing,
    retrieving, and sending messages within that session. Messages represent
    the conversation history between the user and the AI assistant.

    This class is not instantiated directly. Instead, obtain an instance via
    the sessions resource:

        messages = client.sessions.messages(session_id)

    Example:
        ```python
        # Get the messages resource for a session
        messages = client.sessions.messages("ses_abc123")

        # List all messages in the session
        all_msgs = await messages.list()

        # Get a specific message
        msg = await messages.get("msg_xyz789")

        # Send a new message
        from opencode.models.part import TextPart
        response = await messages.send(
            parts=[TextPart(text="Hello, how can you help?")]
        )
        ```

    Attributes:
        session_id: The session ID this resource is scoped to.
    """

    def __init__(self, client: "OpenCode", session_id: str) -> None:
        """
        Initialize the messages resource.

        This constructor is called internally by the SessionsResource when
        accessing messages for a specific session.

        Args:
            client: The OpenCode client instance providing HTTP and configuration.
            session_id: The unique identifier of the session to scope operations to.
        """
        self._client = client
        self._session_id = session_id

    @property
    def _http(self):
        """Access the underlying HTTP client from the OpenCode client."""
        return self._client._http

    @property
    def _directory(self) -> str | None:
        """Get the project directory configured on the client, if any."""
        return self._client._directory

    def _build_params(self, **kwargs: Any) -> dict[str, Any]:
        """
        Build query parameters with automatic directory injection.

        Filters out None values and automatically adds the client's configured
        directory if not explicitly provided.

        Args:
            **kwargs: Key-value pairs to include as query parameters.

        Returns:
            A dictionary of query parameters with None values filtered out
            and directory injected if configured on the client.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        if self._directory and "directory" not in params:
            params["directory"] = self._directory
        return params

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """
        Execute an HTTP request using the base resource infrastructure.

        This method delegates to the BaseResource._request method to ensure
        consistent error handling and response processing.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            path: API endpoint path (e.g., "/session/{id}/message").
            **kwargs: Additional arguments passed to the HTTP client
                (params, json_data, etc.).

        Returns:
            The parsed JSON response from the API.

        Raises:
            OpenCodeError: If the API request fails.
        """
        base = BaseResource(self._client)
        return await base._request(method, path, **kwargs)

    async def list(
        self,
        *,
        limit: int | None = None,
        directory: str | None = None,
    ) -> list[MessageWithParts]:
        """
        List all messages in this session.

        Retrieves the conversation history for the session, including both
        user messages and assistant responses. Each message includes its
        associated parts (text, tool calls, tool results, etc.).

        Args:
            limit: Maximum number of messages to return. If not specified,
                returns all messages in the session.
            directory: Project directory to use for this request. Overrides
                the client's configured directory if provided.

        Returns:
            A list of MessageWithParts objects representing the conversation
            history, ordered by creation time.

        Example:
            ```python
            messages = client.sessions.messages("ses_abc123")

            # Get all messages
            all_msgs = await messages.list()

            # Get last 10 messages
            recent = await messages.list(limit=10)

            for msg in all_msgs:
                print(f"{msg.role}: {len(msg.parts)} parts")
            ```
        """
        params = self._build_params(directory=directory, limit=limit)
        data = await self._request(
            "GET",
            f"/session/{self._session_id}/message",
            params=params,
        )
        return [MessageWithParts.model_validate(item) for item in data]

    async def get(
        self,
        message_id: str,
        *,
        directory: str | None = None,
    ) -> MessageWithParts:
        """
        Get a specific message by ID.

        Retrieves a single message with all its associated parts. This is
        useful when you need to access a specific message without fetching
        the entire conversation history.

        Args:
            message_id: The unique identifier of the message to retrieve.
            directory: Project directory to use for this request. Overrides
                the client's configured directory if provided.

        Returns:
            The requested MessageWithParts object containing the message
            content and metadata.

        Raises:
            OpenCodeError: If the message is not found or the request fails.

        Example:
            ```python
            messages = client.sessions.messages("ses_abc123")
            msg = await messages.get("msg_xyz789")
            print(f"Role: {msg.role}")
            print(f"Parts: {len(msg.parts)}")
            ```
        """
        params = self._build_params(directory=directory)
        data = await self._request(
            "GET",
            f"/session/{self._session_id}/message/{message_id}",
            params=params,
        )
        return MessageWithParts.model_validate(data)

    async def send(
        self,
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
        Send a new message (prompt) to the session.

        This is a synchronous operation that sends a message and waits for
        the assistant's complete response. The response includes all parts
        generated by the assistant, including text, tool calls, and their
        results.

        For long-running operations or when you want to stream the response,
        consider using send_async() combined with event streaming.

        Args:
            parts: A list of message parts to send. Common types include
                TextPart for text content and FilePart for file references.
            model: Optional model configuration to override the session's
                default model settings (provider, model name, etc.).
            agent: Optional agent identifier to route the message to a
                specific agent configuration.
            system: Optional system prompt to override the default system
                instructions for this message.
            tools: Optional dictionary mapping tool names to boolean values
                to enable or disable specific tools for this request.
            message_id: Optional custom message ID. If not provided, a
                unique ID will be generated automatically.
            no_reply: If True, the assistant will not generate a response.
                The message will be added to the session but no reply
                will be produced.
            directory: Project directory to use for this request. Overrides
                the client's configured directory if provided.

        Returns:
            The assistant's response as a MessageWithParts object containing
            all generated content.

        Raises:
            OpenCodeError: If the request fails or the model encounters
                an error during generation.

        Example:
            ```python
            from opencode.models.part import TextPart

            messages = client.sessions.messages("ses_abc123")

            # Send a simple text message
            response = await messages.send(
                parts=[TextPart(text="What is the capital of France?")]
            )
            print(response.parts[0].text)

            # Send with custom model config
            from opencode.models.common import ModelConfig
            response = await messages.send(
                parts=[TextPart(text="Explain quantum computing")],
                model=ModelConfig(provider="anthropic", model="claude-3-opus")
            )

            # Disable specific tools
            response = await messages.send(
                parts=[TextPart(text="Summarize this without using any tools")],
                tools={"web_search": False, "code_execution": False}
            )
            ```
        """
        params = self._build_params(directory=directory)

        body: dict[str, Any] = {
            "parts": [p.model_dump(by_alias=True, exclude_none=True) for p in parts],
        }
        if model:
            body["model"] = model.model_dump(by_alias=True)
        if agent:
            body["agent"] = agent
        if system:
            body["system"] = system
        if tools:
            body["tools"] = tools
        if message_id:
            body["messageID"] = message_id
        if no_reply is not None:
            body["noReply"] = no_reply

        data = await self._request(
            "POST",
            f"/session/{self._session_id}/message",
            params=params,
            json_data=body,
        )
        return MessageWithParts.model_validate(data)

    async def send_async(
        self,
        *,
        parts: list[PartInput],
        model: ModelConfig | None = None,
        agent: str | None = None,
        system: str | None = None,
        tools: dict[str, bool] | None = None,
        message_id: str | None = None,
        no_reply: bool | None = None,
        directory: str | None = None,
    ) -> None:
        """
        Send a message without waiting for response (fire-and-forget).

        This method initiates message processing asynchronously and returns
        immediately. The assistant's response will be generated in the
        background and can be received via event streaming.

        This is useful for:
        - Long-running operations where you want to show progress
        - Streaming responses to display text as it's generated
        - Non-blocking operations in concurrent applications

        Args:
            parts: A list of message parts to send. Common types include
                TextPart for text content and FilePart for file references.
            model: Optional model configuration to override the session's
                default model settings (provider, model name, etc.).
            agent: Optional agent identifier to route the message to a
                specific agent configuration.
            system: Optional system prompt to override the default system
                instructions for this message.
            tools: Optional dictionary mapping tool names to boolean values
                to enable or disable specific tools for this request.
            message_id: Optional custom message ID. If not provided, a
                unique ID will be generated automatically.
            no_reply: If True, the assistant will not generate a response.
                The message will be added to the session but no reply
                will be produced.
            directory: Project directory to use for this request. Overrides
                the client's configured directory if provided.

        Returns:
            None. Use event streaming to receive the response.

        Raises:
            OpenCodeError: If the request fails to be submitted.

        Example:
            ```python
            from opencode.models.part import TextPart

            messages = client.sessions.messages("ses_abc123")

            # Send message asynchronously
            await messages.send_async(
                parts=[TextPart(text="Analyze this large codebase")]
            )

            # Listen for response via events
            async for event in client.events.subscribe(session_id="ses_abc123"):
                if event.type == "message.created":
                    print("Response started")
                elif event.type == "message.completed":
                    print("Response finished")
            ```
        """
        params = self._build_params(directory=directory)

        body: dict[str, Any] = {
            "parts": [p.model_dump(by_alias=True, exclude_none=True) for p in parts],
        }
        if model:
            body["model"] = model.model_dump(by_alias=True)
        if agent:
            body["agent"] = agent
        if system:
            body["system"] = system
        if tools:
            body["tools"] = tools
        if message_id:
            body["messageID"] = message_id
        if no_reply is not None:
            body["noReply"] = no_reply

        await self._request(
            "POST",
            f"/session/{self._session_id}/prompt_async",
            params=params,
            json_data=body,
        )

    @property
    def session_id(self) -> str:
        """
        Get the session ID this resource is scoped to.

        Returns:
            The unique identifier of the session that all operations
            on this resource will be performed against.
        """
        return self._session_id
