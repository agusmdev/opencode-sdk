"""Agent-related Pydantic models."""

from typing import Any, Literal

from pydantic import Field

from opencode.models._base import OpenCodeModel


class AgentModel(OpenCodeModel):
    """
    Represents the model configuration for an agent.

    Specifies which AI model and provider the agent should use.
    """

    model_id: str = Field(alias="modelID")
    """The identifier of the specific model to use."""

    provider_id: str = Field(alias="providerID")
    """The identifier of the model provider."""


class AgentPermission(OpenCodeModel):
    """
    Represents permission settings for an agent.

    Defines what actions the agent is allowed to perform.
    """

    # Permission fields can be extended as needed based on the full schema
    pass


class Agent(OpenCodeModel):
    """
    Represents an AI agent configuration.

    Agents are specialized AI assistants with specific configurations,
    prompts, tools, and behavioral settings.
    """

    name: str
    """The name of the agent."""

    description: str | None = None
    """Human-readable description of what the agent does."""

    mode: Literal["subagent", "primary", "all"]
    """The execution mode of the agent."""

    built_in: bool = Field(alias="builtIn")
    """Whether this is a built-in agent or user-defined."""

    top_p: float | None = Field(default=None, alias="topP")
    """The top-p sampling parameter for the model."""

    temperature: float | None = None
    """The temperature parameter for model generation."""

    color: str | None = None
    """The display color for the agent in UI."""

    permission: AgentPermission
    """The permission settings for the agent."""

    model: AgentModel | None = None
    """The model configuration for the agent."""

    prompt: str | None = None
    """The system prompt for the agent."""

    tools: dict[str, Any]
    """The tools available to the agent."""

    options: dict[str, Any]
    """Additional configuration options for the agent."""

    max_steps: int | None = Field(default=None, alias="maxSteps")
    """The maximum number of steps the agent can take."""
