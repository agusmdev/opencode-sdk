"""Pytest configuration and shared fixtures."""
from __future__ import annotations

import pytest
import respx
from httpx import Response

from opencode import OpenCode


@pytest.fixture
def mock_api():
    """
    Mock HTTP API using respx.
    
    Usage:
        def test_something(mock_api):
            mock_api.get("/session").mock(return_value=Response(200, json=[]))
            # ... test code
    """
    with respx.mock(base_url="http://test", assert_all_called=False) as respx_mock:
        yield respx_mock


@pytest.fixture
async def client(mock_api):
    """
    Create a test client with mocked HTTP.
    
    Usage:
        async def test_something(client):
            sessions = await client.sessions.list()
    """
    async with OpenCode(base_url="http://test") as test_client:
        yield test_client


@pytest.fixture
def session_data():
    """Factory for creating test session data."""
    def _create(**overrides):
        data = {
            "id": "ses_test123",
            "projectID": "proj_123",
            "directory": "/test/project",
            "title": "Test Session",
            "version": "1.0.0",
            "time": {"created": 1234567890.0, "updated": 1234567890.0},
        }
        data.update(overrides)
        return data
    return _create


@pytest.fixture
def message_data():
    """Factory for creating test message data."""
    def _create(**overrides):
        data = {
            "info": {
                "id": "msg_test123",
                "sessionID": "ses_test123",
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
            "parts": [
                {
                    "id": "prt_test123",
                    "sessionID": "ses_test123",
                    "messageID": "msg_test123",
                    "type": "text",
                    "text": "Hello, world!",
                }
            ],
        }
        if overrides:
            data["info"].update(overrides.get("info", {}))
            if "parts" in overrides:
                data["parts"] = overrides["parts"]
        return data
    return _create


@pytest.fixture
def project_data():
    """Factory for creating test project data."""
    def _create(**overrides):
        data = {
            "id": "proj_test123",
            "worktree": "/test/project",
            "time": {"created": 1234567890.0},
        }
        data.update(overrides)
        return data
    return _create


@pytest.fixture  
def event_data():
    """Factory for creating test event data."""
    def _create(event_type: str, **properties):
        return {
            "type": event_type,
            "properties": properties,
        }
    return _create
