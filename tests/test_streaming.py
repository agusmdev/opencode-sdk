"""Tests for SSE streaming."""
from __future__ import annotations

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from opencode import OpenCode, EventStream, StreamingError


class TestEventStream:
    """Test EventStream class."""

    @pytest.mark.asyncio
    async def test_stream_is_async_iterator(self):
        """Test EventStream implements async iterator protocol."""
        import httpx
        
        http_client = httpx.AsyncClient()
        stream = EventStream(
            http_client=http_client,
            url="/event",
            params={},
        )

        assert hasattr(stream, "__aiter__")
        assert hasattr(stream, "__anext__")
        
        await http_client.aclose()

    @pytest.mark.asyncio
    async def test_stream_close(self):
        """Test closing the stream."""
        import httpx
        
        http_client = httpx.AsyncClient()
        stream = EventStream(
            http_client=http_client,
            url="/event",
            params={},
        )

        assert not stream.is_closed
        await stream.close()
        assert stream.is_closed
        
        await http_client.aclose()

    @pytest.mark.asyncio
    async def test_stream_context_manager(self):
        """Test stream as context manager."""
        import httpx
        
        http_client = httpx.AsyncClient()
        stream = EventStream(
            http_client=http_client,
            url="/event",
            params={},
        )

        async with stream:
            assert not stream.is_closed
        
        assert stream.is_closed
        await http_client.aclose()

    def test_stream_retry_count(self):
        """Test retry count tracking."""
        import httpx
        
        http_client = httpx.AsyncClient()
        stream = EventStream(
            http_client=http_client,
            url="/event",
            params={},
            max_retries=5,
        )

        assert stream.retry_count == 0


class TestEventsResource:
    """Test EventsResource."""

    def test_subscribe_returns_event_stream(self, client: OpenCode):
        """Test subscribe returns EventStream."""
        stream = client.events.subscribe()
        
        assert isinstance(stream, EventStream)

    def test_subscribe_with_directory(self, client: OpenCode):
        """Test subscribe with directory parameter."""
        stream = client.events.subscribe(directory="/custom/dir")
        
        assert "/custom/dir" in str(stream._params)

    def test_subscribe_global(self, client: OpenCode):
        """Test global event subscription."""
        stream = client.events.subscribe_global()
        
        assert isinstance(stream, EventStream)


class TestEventParsing:
    """Test event parsing."""

    def test_parse_session_status_event(self):
        """Test parsing session status event."""
        from opencode.models.event import parse_event, SessionStatusEvent
        
        data = {
            "type": "session.status",
            "properties": {
                "sessionID": "ses_123",
                "status": {"type": "idle"},
            },
        }

        event = parse_event(data)

        assert isinstance(event, SessionStatusEvent)
        assert event.properties.session_id == "ses_123"

    def test_parse_message_updated_event(self):
        """Test parsing message updated event."""
        from opencode.models.event import parse_event, MessageUpdatedEvent
        
        data = {
            "type": "message.updated",
            "properties": {
                "info": {
                    "id": "msg_123",
                    "sessionID": "ses_123",
                    "role": "assistant",
                    "time": {"created": 1234567890.0},
                    "parentID": "msg_parent",
                    "modelID": "gpt-4",
                    "providerID": "openai",
                    "mode": "chat",
                    "path": {"cwd": "/test", "root": "/test"},
                    "cost": 0.001,
                    "tokens": {
                        "input": 100,
                        "output": 50,
                        "reasoning": 0,
                        "cache": {"read": 0, "write": 0},
                    },
                },
            },
        }

        event = parse_event(data)

        assert isinstance(event, MessageUpdatedEvent)

    def test_parse_session_idle_event(self):
        """Test parsing session idle event."""
        from opencode.models.event import parse_event, SessionIdleEvent
        
        data = {
            "type": "session.idle",
            "properties": {
                "sessionID": "ses_123",
            },
        }

        event = parse_event(data)

        assert isinstance(event, SessionIdleEvent)
        assert event.properties.session_id == "ses_123"

    def test_parse_message_part_updated_event(self):
        """Test parsing message part updated event with delta."""
        from opencode.models.event import parse_event, MessagePartUpdatedEvent
        
        data = {
            "type": "message.part.updated",
            "properties": {
                "part": {
                    "id": "prt_123",
                    "sessionID": "ses_123",
                    "messageID": "msg_123",
                    "type": "text",
                    "text": "Hello",
                },
                "delta": " world",
            },
        }

        event = parse_event(data)

        assert isinstance(event, MessagePartUpdatedEvent)
        assert event.properties.delta == " world"
