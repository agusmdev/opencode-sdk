"""Tests for exception handling."""
from __future__ import annotations

import pytest
from httpx import Response
from respx import MockRouter

from opencode import (
    OpenCode,
    OpenCodeError,
    APIError,
    BadRequestError,
    NotFoundError,
    AuthenticationError,
    RateLimitError,
    ServerError,
    StreamingError,
    ConnectionError,
    ValidationError,
)


class TestExceptionHierarchy:
    """Test exception class hierarchy."""

    def test_api_error_is_opencode_error(self):
        """Test APIError inherits from OpenCodeError."""
        assert issubclass(APIError, OpenCodeError)

    def test_bad_request_error_is_api_error(self):
        """Test BadRequestError inherits from APIError."""
        assert issubclass(BadRequestError, APIError)

    def test_not_found_error_is_api_error(self):
        """Test NotFoundError inherits from APIError."""
        assert issubclass(NotFoundError, APIError)

    def test_authentication_error_is_api_error(self):
        """Test AuthenticationError inherits from APIError."""
        assert issubclass(AuthenticationError, APIError)

    def test_rate_limit_error_is_api_error(self):
        """Test RateLimitError inherits from APIError."""
        assert issubclass(RateLimitError, APIError)

    def test_server_error_is_api_error(self):
        """Test ServerError inherits from APIError."""
        assert issubclass(ServerError, APIError)

    def test_streaming_error_is_opencode_error(self):
        """Test StreamingError inherits from OpenCodeError."""
        assert issubclass(StreamingError, OpenCodeError)

    def test_connection_error_is_opencode_error(self):
        """Test ConnectionError inherits from OpenCodeError."""
        assert issubclass(ConnectionError, OpenCodeError)


class TestExceptionAttributes:
    """Test exception attributes."""

    def test_api_error_attributes(self):
        """Test APIError has correct attributes."""
        error = APIError(
            "Something went wrong",
            status_code=500,
            error_type="InternalError",
            response_body={"detail": "error"},
        )

        assert error.message == "Something went wrong"
        assert error.status_code == 500
        assert error.error_type == "InternalError"
        assert error.response_body == {"detail": "error"}

    def test_bad_request_error_with_errors(self):
        """Test BadRequestError with validation errors."""
        error = BadRequestError(
            "Validation failed",
            errors=[{"field": "title", "message": "required"}],
        )

        assert error.status_code == 400
        assert len(error.errors) == 1
        assert error.errors[0]["field"] == "title"

    def test_authentication_error_with_provider(self):
        """Test AuthenticationError with provider ID."""
        error = AuthenticationError(
            "Auth failed",
            provider_id="openai",
        )

        assert error.provider_id == "openai"

    def test_rate_limit_error_with_retry_after(self):
        """Test RateLimitError with retry-after."""
        error = RateLimitError(
            "Too many requests",
            retry_after=30.0,
        )

        assert error.retry_after == 30.0

    def test_streaming_error_attributes(self):
        """Test StreamingError attributes."""
        cause = Exception("Connection lost")
        error = StreamingError(
            "Stream failed",
            retry_count=3,
            cause=cause,
        )

        assert error.message == "Stream failed"
        assert error.retry_count == 3
        assert error.cause is cause


class TestExceptionStringRepresentation:
    """Test exception string representations."""

    def test_api_error_str(self):
        """Test APIError string representation."""
        error = APIError(
            "Something went wrong",
            status_code=500,
            error_type="InternalError",
        )

        assert "[500]" in str(error)
        assert "InternalError" in str(error)

    def test_streaming_error_str_with_retries(self):
        """Test StreamingError string with retry count."""
        error = StreamingError("Stream failed", retry_count=3)

        assert "3 retries" in str(error)

    def test_connection_error_str_with_url(self):
        """Test ConnectionError string with URL."""
        error = ConnectionError(
            "Connection failed",
            url="http://localhost:1122",
        )

        assert "localhost:1122" in str(error)


class TestExceptionRaising:
    """Test exceptions are raised correctly by the client."""

    @pytest.mark.asyncio
    async def test_400_raises_bad_request(self, client: OpenCode, mock_api: MockRouter):
        """Test 400 response raises BadRequestError."""
        mock_api.get("/session/ses_123").mock(return_value=Response(400, json={
            "errors": [{"message": "Invalid ID"}],
            "success": False,
        }))

        with pytest.raises(BadRequestError) as exc_info:
            await client.sessions.get("ses_123")

        assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_404_raises_not_found(self, client: OpenCode, mock_api: MockRouter):
        """Test 404 response raises NotFoundError."""
        mock_api.get("/session/ses_123").mock(return_value=Response(404, json={
            "name": "NotFoundError",
            "data": {"message": "Session not found"},
        }))

        with pytest.raises(NotFoundError) as exc_info:
            await client.sessions.get("ses_123")

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_401_raises_authentication_error(self, client: OpenCode, mock_api: MockRouter):
        """Test 401 response raises AuthenticationError."""
        mock_api.get("/session").mock(return_value=Response(401, json={
            "name": "ProviderAuthError",
            "data": {"providerID": "openai", "message": "Invalid API key"},
        }))

        with pytest.raises(AuthenticationError) as exc_info:
            await client.sessions.list()

        assert exc_info.value.status_code == 401
        assert exc_info.value.provider_id == "openai"

    @pytest.mark.asyncio
    async def test_429_raises_rate_limit_error(self, client: OpenCode, mock_api: MockRouter):
        """Test 429 response raises RateLimitError."""
        mock_api.get("/session").mock(return_value=Response(
            429,
            json={"message": "Rate limited"},
            headers={"retry-after": "30"},
        ))

        with pytest.raises(RateLimitError) as exc_info:
            await client.sessions.list()

        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 30.0

    @pytest.mark.asyncio
    async def test_500_raises_server_error(self, client: OpenCode, mock_api: MockRouter):
        """Test 500 response raises ServerError."""
        mock_api.get("/session").mock(return_value=Response(500, json={
            "message": "Internal server error",
        }))

        with pytest.raises(ServerError) as exc_info:
            await client.sessions.list()

        assert exc_info.value.status_code == 500
