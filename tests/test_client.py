"""Tests for the OpenCode client."""
from __future__ import annotations

import pytest
from httpx import Response
from respx import MockRouter

from opencode import OpenCode


class TestClientInitialization:
    """Test client initialization."""

    def test_default_base_url(self):
        """Test default base URL is set."""
        client = OpenCode()
        assert client._base_url == "http://127.0.0.1:1122"

    def test_custom_base_url(self):
        """Test custom base URL."""
        client = OpenCode(base_url="http://custom:8080")
        assert client._base_url == "http://custom:8080"

    def test_directory_parameter(self):
        """Test directory parameter is stored."""
        client = OpenCode(directory="/my/project")
        assert client._directory == "/my/project"

    def test_timeout_parameter(self):
        """Test timeout parameter is stored."""
        client = OpenCode(timeout=60.0)
        assert client._timeout == 60.0


class TestClientContextManager:
    """Test client as async context manager."""

    @pytest.mark.asyncio
    async def test_context_manager(self, mock_api: MockRouter):
        """Test client works as async context manager."""
        async with OpenCode(base_url="http://test") as client:
            assert client is not None
            assert not client._http.is_closed
        
        # Client should be closed after exiting context
        assert client._http.is_closed

    @pytest.mark.asyncio
    async def test_close_method(self, mock_api: MockRouter):
        """Test explicit close method."""
        client = OpenCode(base_url="http://test")
        assert not client._http.is_closed
        
        await client.close()
        assert client._http.is_closed


class TestClientResources:
    """Test client resource access."""

    def test_sessions_resource(self):
        """Test sessions resource is accessible."""
        client = OpenCode()
        assert client.sessions is not None
        assert client.sessions.__class__.__name__ == "SessionsResource"

    def test_events_resource(self):
        """Test events resource is accessible."""
        client = OpenCode()
        assert client.events is not None
        assert client.events.__class__.__name__ == "EventsResource"

    def test_projects_resource(self):
        """Test projects resource is accessible."""
        client = OpenCode()
        assert client.projects is not None

    def test_providers_resource(self):
        """Test providers resource is accessible."""
        client = OpenCode()
        assert client.providers is not None

    def test_config_resource(self):
        """Test config resource is accessible."""
        client = OpenCode()
        assert client.config is not None

    def test_files_resource(self):
        """Test files resource is accessible."""
        client = OpenCode()
        assert client.files is not None

    def test_resource_lazy_initialization(self):
        """Test resources are lazily initialized."""
        client = OpenCode()
        # Before accessing, internal attribute should be None
        assert client._sessions is None
        
        # After accessing, it should be initialized
        _ = client.sessions
        assert client._sessions is not None


class TestClientRepr:
    """Test client string representation."""

    def test_repr_default(self):
        """Test repr with default values."""
        client = OpenCode()
        assert "OpenCode" in repr(client)
        assert "127.0.0.1:1122" in repr(client)

    def test_repr_with_directory(self):
        """Test repr with directory."""
        client = OpenCode(directory="/my/project")
        assert "/my/project" in repr(client)
