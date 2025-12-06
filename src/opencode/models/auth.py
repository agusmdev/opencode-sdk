"""Authentication-related Pydantic models."""

from typing import Literal, Union

from pydantic import Field

from opencode.models._base import OpenCodeModel


class OAuth(OpenCodeModel):
    """
    Represents OAuth authentication credentials.

    Contains tokens and metadata for OAuth-based authentication,
    including optional enterprise URL for self-hosted instances.
    """

    type: Literal["oauth"]
    """The authentication type identifier."""

    refresh: str
    """The OAuth refresh token."""

    access: str
    """The OAuth access token."""

    expires: float
    """Unix timestamp when the access token expires."""

    enterprise_url: str | None = Field(default=None, alias="enterpriseUrl")
    """The enterprise URL for self-hosted instances, if applicable."""


class ApiAuth(OpenCodeModel):
    """
    Represents API key authentication.

    Simple key-based authentication for API access.
    """

    type: Literal["api"]
    """The authentication type identifier."""

    key: str
    """The API key for authentication."""


class WellKnownAuth(OpenCodeModel):
    """
    Represents well-known authentication credentials.

    Used for authentication via well-known discovery endpoints.
    """

    type: Literal["wellknown"]
    """The authentication type identifier."""

    key: str
    """The authentication key."""

    token: str
    """The authentication token."""


Auth = Union[OAuth, ApiAuth, WellKnownAuth]
"""
Union type representing all possible authentication methods.

Can be one of: OAuth, API key, or well-known authentication.
"""
