"""Exception hierarchy for the OpenCode SDK."""

from typing import Any


class OpenCodeError(Exception):
    """Base exception for all SDK errors."""

    pass


class APIError(OpenCodeError):
    """
    HTTP API error with response details.

    Attributes:
        message: Human-readable error message
        status_code: HTTP status code
        error_type: API error type (e.g., "NotFoundError", "BadRequestError")
        response_body: Raw response body as dict
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        error_type: str | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.response_body = response_body

    def __str__(self) -> str:
        if self.error_type:
            return f"[{self.status_code}] {self.error_type}: {self.message}"
        return f"[{self.status_code}] {self.message}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"status_code={self.status_code}, "
            f"error_type={self.error_type!r})"
        )


class BadRequestError(APIError):
    """
    400 Bad Request - validation or input errors.

    Raised when the request parameters are invalid.
    """

    def __init__(
        self,
        message: str = "Bad request",
        *,
        errors: list[dict[str, Any]] | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=400,
            error_type="BadRequestError",
            response_body=response_body,
        )
        self.errors = errors or []


class NotFoundError(APIError):
    """
    404 Not Found.

    Raised when the requested resource does not exist.
    """

    def __init__(
        self,
        message: str = "Resource not found",
        *,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=404,
            error_type="NotFoundError",
            response_body=response_body,
        )


class AuthenticationError(APIError):
    """
    401/403 Authentication or authorization error.

    Raised when provider authentication fails or access is denied.
    """

    def __init__(
        self,
        message: str = "Authentication failed",
        *,
        status_code: int = 401,
        provider_id: str | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=status_code,
            error_type="AuthenticationError",
            response_body=response_body,
        )
        self.provider_id = provider_id


class RateLimitError(APIError):
    """
    429 Rate limit exceeded.

    Raised when too many requests are made in a short period.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        *,
        retry_after: float | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=429,
            error_type="RateLimitError",
            response_body=response_body,
        )
        self.retry_after = retry_after


class ServerError(APIError):
    """
    5xx Server error.

    Raised when the server encounters an internal error.
    """

    def __init__(
        self,
        message: str = "Internal server error",
        *,
        status_code: int = 500,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=status_code,
            error_type="ServerError",
            response_body=response_body,
        )


class StreamingError(OpenCodeError):
    """
    SSE streaming error.

    Raised when there's an error during event streaming.
    """

    def __init__(
        self,
        message: str,
        *,
        retry_count: int = 0,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.retry_count = retry_count
        self.cause = cause

    def __str__(self) -> str:
        if self.retry_count > 0:
            return f"{self.message} (after {self.retry_count} retries)"
        return self.message


class ConnectionError(OpenCodeError):
    """
    Network connectivity error.

    Raised when unable to connect to the API server.
    """

    def __init__(
        self,
        message: str = "Failed to connect to the API server",
        *,
        url: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.url = url
        self.cause = cause

    def __str__(self) -> str:
        if self.url:
            return f"{self.message}: {self.url}"
        return self.message


class ValidationError(OpenCodeError):
    """
    Local validation error.

    Raised when input validation fails before making an API request.
    """

    def __init__(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.field = field
        self.value = value

    def __str__(self) -> str:
        if self.field:
            return f"Validation error for '{self.field}': {self.message}"
        return f"Validation error: {self.message}"
