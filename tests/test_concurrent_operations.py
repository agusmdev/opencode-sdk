"""Tests for concurrent operations and race conditions identified in the SDK analysis."""
from __future__ import annotations

import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from httpx import Response
import respx

from opencode import OpenCode


class TestConcurrentResourceInitialization:
    """Test concurrent resource initialization race condition (Bug #5)."""

    @pytest.mark.asyncio
    async def test_concurrent_sessions_property_access(self):
        """Test that concurrent access to sessions property doesn't create multiple instances."""
        client = OpenCode()

        # Simulate concurrent access to sessions property
        async def access_sessions():
            return client.sessions

        # Create multiple concurrent tasks
        tasks = [access_sessions() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # All should return the same instance
        first_instance = results[0]
        for result in results[1:]:
            assert result is first_instance, "Multiple instances created concurrently"

    @pytest.mark.asyncio
    async def test_concurrent_events_property_access(self):
        """Test that concurrent access to events property doesn't create multiple instances."""
        client = OpenCode()

        async def access_events():
            return client.events

        tasks = [access_events() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        first_instance = results[0]
        for result in results[1:]:
            assert result is first_instance

    @pytest.mark.asyncio
    async def test_concurrent_all_properties_access(self):
        """Test concurrent access to all lazy properties."""
        client = OpenCode()

        async def access_all_properties():
            # Access all lazy properties concurrently
            return (
                client.sessions,
                client.events,
                client.projects,
                client.providers,
                client.config,
                client.files,
                client.find,
                client.tools,
                client.mcp,
                client.lsp,
                client.agents,
                client.commands,
                client.auth,
                client.pty,
                client.vcs,
                client.path,
                client.instance,
                client.formatter,
                client.tui,
            )

        # Run multiple times concurrently
        tasks = [access_all_properties() for _ in range(5)]
        results = await asyncio.gather(*tasks)

        # All property instances should be the same across all calls
        first_result = results[0]
        for result in results[1:]:
            for i, (first_prop, prop) in enumerate(zip(first_result, result)):
                assert prop is first_prop, f"Property {i} has different instances"


class TestConcurrentStreamingOperations:
    """Test concurrent streaming operations."""

    @pytest.mark.asyncio
    async def test_concurrent_event_stream_creation(self, client: OpenCode):
        """Test creating multiple event streams concurrently."""
        async def create_stream():
            return client.events.subscribe()

        tasks = [create_stream() for _ in range(5)]
        streams = await asyncio.gather(*tasks)

        # All streams should be different instances
        for i, stream1 in enumerate(streams):
            for j, stream2 in enumerate(streams):
                if i != j:
                    assert stream1 is not stream2

    @pytest.mark.asyncio
    async def test_concurrent_event_stream_close(self, client: OpenCode):
        """Test closing multiple event streams concurrently."""
        streams = []
        for _ in range(5):
            stream = client.events.subscribe()
            streams.append(stream)

        # Close all streams concurrently
        close_tasks = [stream.close() for stream in streams]
        await asyncio.gather(*close_tasks)

        # All should be closed
        for stream in streams:
            assert stream.is_closed


class TestConcurrentPagination:
    """Test concurrent pagination operations."""

    @pytest.mark.asyncio
    async def test_concurrent_pagination_creation(self, client: OpenCode, mock_api):
        """Test creating multiple paginators concurrently."""
        mock_api.get("/session").mock(return_value=Response(200, json=[]))

        async def create_paginator():
            return client.sessions.list_iter()

        tasks = [create_paginator() for _ in range(5)]
        paginators = await asyncio.gather(*tasks)

        # All should be different instances
        for i, pag1 in enumerate(paginators):
            for j, pag2 in enumerate(paginators):
                if i != j:
                    assert pag1 is not pag2

    @pytest.mark.asyncio
    async def test_concurrent_pagination_iteration(self, client: OpenCode, mock_api):
        """Test iterating through multiple paginators concurrently."""
        # Mock API with some data
        session_data = [
            {"id": f"ses_{i}", "projectID": "proj_123", "directory": "/test",
             "title": f"Session {i}", "version": "1.0.0",
             "time": {"created": 1234567890.0, "updated": 1234567890.0}}
            for i in range(10)
        ]

        def mock_session_response(request):
            """Mock response that handles pagination parameters."""
            params = request.url.params
            offset = int(params.get("offset", 0))
            limit = int(params.get("limit", len(session_data)))
            paginated_data = session_data[offset:offset + limit]
            return Response(200, json=paginated_data)

        mock_api.get("/session").mock(side_effect=mock_session_response)

        async def iterate_paginator():
            paginator = client.sessions.list_iter(page_size=3)
            count = 0
            async for session in paginator:
                count += 1
            return count

        # Run multiple paginators concurrently
        tasks = [iterate_paginator() for _ in range(3)]
        results = await asyncio.gather(*tasks)

        # All should have processed the same number of items
        expected_count = len(session_data)
        for result in results:
            assert result == expected_count


class TestConcurrentClientOperations:
    """Test concurrent operations on the same client instance."""

    @pytest.mark.asyncio
    async def test_concurrent_session_operations(self, client: OpenCode, mock_api):
        """Test concurrent session list operations."""
        session_data = [
            {"id": f"ses_{i}", "projectID": "proj_123", "directory": "/test",
             "title": f"Session {i}", "version": "1.0.0",
             "time": {"created": 1234567890.0, "updated": 1234567890.0}}
            for i in range(5)
        ]
        mock_api.get("/session").mock(return_value=Response(200, json=session_data))

        async def list_sessions():
            return await client.sessions.list()

        # Run multiple concurrent list operations
        tasks = [list_sessions() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # All should return the same data
        first_result = results[0]
        for result in results[1:]:
            assert result == first_result
            assert len(result) == 5

    @pytest.mark.asyncio
    async def test_concurrent_file_operations(self, client: OpenCode, mock_api):
        """Test concurrent file list operations."""
        file_data = [
            {"name": f"file_{i}.py", "path": f"/file_{i}.py", "absolute": f"/abs/file_{i}.py",
             "type": "file", "ignored": False}
            for i in range(5)
        ]
        mock_api.get("/file").mock(return_value=Response(200, json=file_data))

        async def list_files():
            return await client.files.list("/")

        tasks = [list_files() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        first_result = results[0]
        for result in results[1:]:
            assert result == first_result
            assert len(result) == 5


class TestConcurrentMessagesResource:
    """Test concurrent operations on MessagesResource."""

    @pytest.mark.asyncio
    async def test_concurrent_messages_creation(self, client: OpenCode):
        """Test creating multiple MessagesResource instances concurrently."""
        async def create_messages_resource():
            return client.sessions.messages("ses_123")

        tasks = [create_messages_resource() for _ in range(10)]
        resources = await asyncio.gather(*tasks)

        # All should be different instances but point to same session
        for i, res1 in enumerate(resources):
            assert res1._session_id == "ses_123"
            for j, res2 in enumerate(resources):
                if i != j:
                    assert res1 is not res2

    @pytest.mark.asyncio
    async def test_concurrent_messages_operations(self, client: OpenCode, mock_api):
        """Test concurrent operations on MessagesResource."""
        message_data = {
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
            "parts": [{
                "id": "prt_123",
                "sessionID": "ses_123",
                "messageID": "msg_123",
                "type": "text",
                "text": "Hello!",
            }],
        }
        mock_api.get("/session/ses_123/message").mock(return_value=Response(200, json=[message_data]))

        messages = client.sessions.messages("ses_123")

        async def list_messages():
            return await messages.list()

        tasks = [list_messages() for _ in range(5)]
        results = await asyncio.gather(*tasks)

        first_result = results[0]
        for result in results[1:]:
            assert result == first_result


class TestConcurrentHTTPClientUsage:
    """Test concurrent usage of the underlying HTTP client."""

    @pytest.mark.asyncio
    async def test_concurrent_http_requests(self, client: OpenCode, mock_api):
        """Test that concurrent requests don't interfere with each other."""
        # Mock different endpoints with different responses
        mock_api.get("/session").mock(return_value=Response(200, json=[{"id": "ses_1", "projectID": "proj_123", "directory": "/test", "title": "Session 1", "version": "1.0.0", "time": {"created": 1234567890.0, "updated": 1234567890.0}}]))
        mock_api.get("/project").mock(return_value=Response(200, json=[{"id": "proj_1", "worktree": "/test", "time": {"created": 1234567890.0}}]))
        mock_api.get("/file").mock(return_value=Response(200, json=[{"name": "test.py", "path": "/test.py", "absolute": "/abs/test.py", "type": "file", "ignored": False}]))

        async def make_request(endpoint, expected_key):
            if endpoint == "sessions":
                result = await client.sessions.list()
                return getattr(result[0], expected_key)
            elif endpoint == "projects":
                result = await client.projects.list()
                return getattr(result[0], expected_key)
            elif endpoint == "files":
                result = await client.files.list("/")
                return getattr(result[0], expected_key)

        # Make concurrent requests to different endpoints
        tasks = [
            make_request("sessions", "id"),
            make_request("projects", "id"),
            make_request("files", "name"),
            make_request("sessions", "title"),
            make_request("projects", "worktree"),
        ]

        results = await asyncio.gather(*tasks)

        # Verify results are correct and not mixed up
        assert results[0] == "ses_1"  # sessions id
        assert results[1] == "proj_1"  # projects id
        assert results[2] == "test.py"  # files name
        assert results[3] == "Session 1"  # sessions title
        assert results[4] == "/test"  # projects worktree


class TestResourceCleanupConcurrency:
    """Test resource cleanup under concurrent operations."""

    @pytest.mark.asyncio
    async def test_concurrent_client_close(self):
        """Test closing client while operations are in progress."""
        client = OpenCode()

        # Start some operations
        async def dummy_operation():
            await asyncio.sleep(0.1)  # Simulate some work
            return "done"

        # Start operations and close concurrently
        task = asyncio.create_task(dummy_operation())
        close_task = asyncio.create_task(client.close())

        # Both should complete without issues
        result = await task
        await close_task

        assert result == "done"
        assert client._http.is_closed