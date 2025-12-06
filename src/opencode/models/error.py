"""Pydantic models for API error types."""

from typing import Annotated, Literal, Union

from pydantic import Field

from opencode.models._base import OpenCodeModel


class ProviderAuthErrorData(OpenCodeModel):
    """Data payload for provider authentication errors."""

    provider_id: str = Field(alias="providerID")
    """The ID of the provider that failed authentication."""

    message: str
    """Human-readable error message."""


class ProviderAuthError(OpenCodeModel):
    """Error indicating provider authentication failure."""

    name: Literal["ProviderAuthError"] = "ProviderAuthError"
    """Error type discriminator."""

    data: ProviderAuthErrorData
    """Error details."""


class UnknownErrorData(OpenCodeModel):
    """Data payload for unknown errors."""

    message: str
    """Human-readable error message."""


class UnknownError(OpenCodeModel):
    """Error indicating an unknown or unexpected error occurred."""

    name: Literal["UnknownError"] = "UnknownError"
    """Error type discriminator."""

    data: UnknownErrorData
    """Error details."""


class MessageOutputLengthErrorData(OpenCodeModel):
    """Data payload for message output length errors."""

    pass


class MessageOutputLengthError(OpenCodeModel):
    """Error indicating the message output exceeded the maximum allowed length."""

    name: Literal["MessageOutputLengthError"] = "MessageOutputLengthError"
    """Error type discriminator."""

    data: MessageOutputLengthErrorData
    """Error details."""


class MessageAbortedErrorData(OpenCodeModel):
    """Data payload for message aborted errors."""

    message: str
    """Human-readable error message."""


class MessageAbortedError(OpenCodeModel):
    """Error indicating the message was aborted."""

    name: Literal["MessageAbortedError"] = "MessageAbortedError"
    """Error type discriminator."""

    data: MessageAbortedErrorData
    """Error details."""


class APIErrorData(OpenCodeModel):
    """Data payload for API errors."""

    message: str
    """Human-readable error message."""

    is_retryable: bool = Field(alias="isRetryable")
    """Whether the request can be retried."""

    status_code: int | None = Field(default=None, alias="statusCode")
    """HTTP status code if available."""

    response_headers: dict[str, str] | None = Field(
        default=None, alias="responseHeaders"
    )
    """Response headers if available."""

    response_body: str | None = Field(default=None, alias="responseBody")
    """Response body if available."""


class APIErrorModel(OpenCodeModel):
    """Error indicating an API-level error occurred.

    Named APIErrorModel to avoid conflict with exception classes.
    """

    name: Literal["APIError"] = "APIError"
    """Error type discriminator."""

    data: APIErrorData
    """Error details."""


MessageError = Annotated[
    Union[
        ProviderAuthError,
        UnknownError,
        MessageOutputLengthError,
        MessageAbortedError,
        APIErrorModel,
    ],
    Field(discriminator="name"),
]
"""Union type representing any message-level error."""
