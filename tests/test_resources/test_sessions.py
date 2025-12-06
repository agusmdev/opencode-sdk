"""Tests for the Sessions resource."""
from __future__ import annotations

import pytest
from httpx import Response
from respx import MockRouter

from opencode import OpenCode
from opencode.models import Session, MessageWithParts, TextPartInput


class TestSessionsList:
    """Test session listing."""

    @pytest.mark.asyncio
    async def test_list_sessions(self, client: OpenCode, mock_api: MockRouter, session_data):
        """Test listing sessions."""
        mock_api.get("/session").mock(return_value=Response(200, json=[
            session_data(id="ses_1", title="Session 1"),
            session_data(id="ses_2", title="Session 2"),
        ]))

        sessions = await client.sessions.list()

        assert len(sessions) == 2
        assert sessions[0].id == "ses_1"
        assert sessions[0].title == "Session 1"
        assert sessions[1].id == "ses_2"

    @pytest.mark.asyncio
    async def test_list_sessions_empty(self, client: OpenCode, mock_api: MockRouter):
        """Test listing sessions when empty."""
        mock_api.get("/session").mock(return_value=Response(200, json=[]))

        sessions = await client.sessions.list()

        assert sessions == []

    @pytest.mark.asyncio
    async def test_list_sessions_with_directory(self, client: OpenCode, mock_api: MockRouter, session_data):
        """Test listing sessions with directory parameter."""
        mock_api.get("/session").mock(return_value=Response(200, json=[session_data()]))

        await client.sessions.list(directory="/custom/dir")

        assert mock_api.calls.last.request.url.params.get("directory") == "/custom/dir"


class TestSessionsCreate:
    """Test session creation."""

    @pytest.mark.asyncio
    async def test_create_session(self, client: OpenCode, mock_api: MockRouter, session_data):
        """Test creating a session."""
        mock_api.post("/session").mock(return_value=Response(200, json=session_data(title="New Session")))

        session = await client.sessions.create(title="New Session")

        assert session.title == "New Session"
        assert session.id == "ses_test123"

    @pytest.mark.asyncio
    async def test_create_session_with_parent(self, client: OpenCode, mock_api: MockRouter, session_data):
        """Test creating a session with parent ID."""
        mock_api.post("/session").mock(return_value=Response(200, json=session_data(parentID="ses_parent")))

        session = await client.sessions.create(parent_id="ses_parent")

        request_json = mock_api.calls.last.request.read()
        assert b"parentID" in request_json


class TestSessionsGet:
    """Test getting a session."""

    @pytest.mark.asyncio
    async def test_get_session(self, client: OpenCode, mock_api: MockRouter, session_data):
        """Test getting a session by ID."""
        mock_api.get("/session/ses_123").mock(return_value=Response(200, json=session_data(id="ses_123")))

        session = await client.sessions.get("ses_123")

        assert session.id == "ses_123"

    @pytest.mark.asyncio
    async def test_get_session_not_found(self, client: OpenCode, mock_api: MockRouter):
        """Test getting a non-existent session."""
        from opencode import NotFoundError
        
        mock_api.get("/session/ses_invalid").mock(return_value=Response(404, json={
            "name": "NotFoundError",
            "data": {"message": "Session not found"}
        }))

        with pytest.raises(NotFoundError) as exc_info:
            await client.sessions.get("ses_invalid")

        assert exc_info.value.status_code == 404


class TestSessionsDelete:
    """Test deleting a session."""

    @pytest.mark.asyncio
    async def test_delete_session(self, client: OpenCode, mock_api: MockRouter):
        """Test deleting a session."""
        mock_api.delete("/session/ses_123").mock(return_value=Response(200, json=True))

        result = await client.sessions.delete("ses_123")

        assert result is True


class TestSessionsPrompt:
    """Test sending prompts."""

    @pytest.mark.asyncio
    async def test_prompt(self, client: OpenCode, mock_api: MockRouter, message_data):
        """Test sending a prompt."""
        mock_api.post("/session/ses_123/message").mock(return_value=Response(200, json=message_data()))

        response = await client.sessions.prompt(
            "ses_123",
            parts=[TextPartInput(type="text", text="Hello!")],
        )

        assert response.info.id == "msg_test123"
        assert len(response.parts) == 1

    @pytest.mark.asyncio
    async def test_prompt_with_model(self, client: OpenCode, mock_api: MockRouter, message_data):
        """Test sending a prompt with model config."""
        from opencode.models import ModelConfig
        
        mock_api.post("/session/ses_123/message").mock(return_value=Response(200, json=message_data()))

        await client.sessions.prompt(
            "ses_123",
            parts=[TextPartInput(type="text", text="Hello!")],
            model=ModelConfig(provider_id="anthropic", model_id="claude-3"),
        )

        request_json = mock_api.calls.last.request.read()
        assert b"providerID" in request_json
        assert b"modelID" in request_json


class TestSessionsAbort:
    """Test aborting sessions."""

    @pytest.mark.asyncio
    async def test_abort_session(self, client: OpenCode, mock_api: MockRouter):
        """Test aborting a session."""
        mock_api.post("/session/ses_123/abort").mock(return_value=Response(200, json=True))

        result = await client.sessions.abort("ses_123")

        assert result is True


class TestSessionsMessages:
    """Test session messages sub-resource."""

    @pytest.mark.asyncio
    async def test_get_messages(self, client: OpenCode, mock_api: MockRouter, message_data):
        """Test getting session messages."""
        mock_api.get("/session/ses_123/message").mock(return_value=Response(200, json=[message_data()]))

        messages = await client.sessions.get_messages("ses_123")

        assert len(messages) == 1
        assert messages[0].info.id == "msg_test123"

    def test_messages_resource(self, client: OpenCode):
        """Test getting messages resource for a session."""
        messages = client.sessions.messages("ses_123")
        
        assert messages.session_id == "ses_123"
