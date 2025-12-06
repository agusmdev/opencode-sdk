"""Provider and Model-related Pydantic models."""

from enum import Enum
from typing import Any, Literal

from pydantic import Field

from opencode.models._base import OpenCodeModel


class ModelStatus(str, Enum):
    """Status of a model indicating its lifecycle stage."""

    ALPHA = "alpha"
    """Model is in early testing phase."""

    BETA = "beta"
    """Model is in beta testing phase."""

    DEPRECATED = "deprecated"
    """Model is deprecated and should not be used."""

    ACTIVE = "active"
    """Model is actively supported and recommended for use."""


class ProviderSource(str, Enum):
    """Source of provider configuration."""

    ENV = "env"
    """Provider configured via environment variables."""

    CONFIG = "config"
    """Provider configured via configuration file."""

    CUSTOM = "custom"
    """Provider configured via custom configuration."""

    API = "api"
    """Provider configured via API."""


class ModelApi(OpenCodeModel):
    """API configuration for a model."""

    id: str
    """The unique identifier for the API."""

    url: str
    """The base URL for the API endpoint."""

    npm: str
    """The npm package name for the API client."""


class ModelModalities(OpenCodeModel):
    """Modalities supported by a model for input or output."""

    text: bool
    """Whether text modality is supported."""

    audio: bool
    """Whether audio modality is supported."""

    image: bool
    """Whether image modality is supported."""

    video: bool
    """Whether video modality is supported."""

    pdf: bool
    """Whether PDF modality is supported."""


class ModelCapabilities(OpenCodeModel):
    """Capabilities of a model."""

    temperature: bool | None = None
    """Whether the model supports temperature parameter."""

    reasoning: bool | None = None
    """Whether the model supports reasoning/chain-of-thought."""

    attachment: bool | None = None
    """Whether the model supports file attachments."""

    toolcall: bool | None = None
    """Whether the model supports tool/function calling."""

    input: ModelModalities | None = None
    """Input modalities supported by the model."""

    output: ModelModalities | None = None
    """Output modalities supported by the model."""


class CacheCost(OpenCodeModel):
    """Cost information for cache operations."""

    read: float
    """Cost per token for cache read operations."""

    write: float
    """Cost per token for cache write operations."""


class ModelCost(OpenCodeModel):
    """Cost information for model usage."""

    input: float | None = None
    """Cost per token for input/prompt tokens."""

    output: float | None = None
    """Cost per token for output/completion tokens."""

    cache: CacheCost | None = None
    """Cost information for cache operations."""

    experimental_over_200k: dict[str, Any] | None = Field(
        default=None, alias="experimentalOver200K"
    )
    """Experimental pricing for contexts over 200K tokens."""


class ModelLimit(OpenCodeModel):
    """Token limits for a model."""

    context: int | None = None
    """Maximum context window size in tokens."""

    output: int | None = None
    """Maximum output/completion size in tokens."""


class Model(OpenCodeModel):
    """
    Represents an AI model configuration.

    Contains all information about a model including its capabilities,
    costs, limits, and API configuration.
    """

    id: str | None = None
    """The unique model identifier."""

    provider_id: str | None = Field(default=None, alias="providerID")
    """The ID of the provider that offers this model."""

    api: ModelApi | None = None
    """API configuration for the model."""

    name: str | None = None
    """Human-readable name of the model."""

    capabilities: ModelCapabilities | None = None
    """Capabilities supported by the model."""

    cost: ModelCost | None = None
    """Cost information for using the model."""

    limit: ModelLimit | None = None
    """Token limits for the model."""

    status: ModelStatus | None = None
    """Lifecycle status of the model."""

    options: dict[str, Any] | None = None
    """Additional model-specific options."""

    headers: dict[str, Any] | None = None
    """Custom headers to include in API requests."""


class Provider(OpenCodeModel):
    """
    Represents an AI provider configuration.

    Contains all information about a provider including authentication,
    available models, and configuration options.
    """

    id: str | None = None
    """The unique provider identifier."""

    name: str | None = None
    """Human-readable name of the provider."""

    source: ProviderSource | None = None
    """Source of the provider configuration."""

    env: list[str] | None = None
    """Environment variable names used for authentication."""

    key: str | None = None
    """API key for authentication (if applicable)."""

    options: dict[str, Any] | None = None
    """Additional provider-specific options."""

    models: dict[str, Model] | None = None
    """Dictionary of models available from this provider."""


class ProviderAuthMethod(OpenCodeModel):
    """Authentication method supported by a provider."""

    type: Literal["oauth", "api"]
    """The type of authentication method."""

    label: str
    """Human-readable label for the authentication method."""


class ProviderAuthAuthorization(OpenCodeModel):
    """Authorization configuration for provider authentication."""

    url: str
    """The URL for the authorization endpoint."""

    method: Literal["auto", "code"]
    """The authorization method to use."""

    instructions: str
    """Instructions for completing the authorization flow."""
