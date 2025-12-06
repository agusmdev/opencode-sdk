"""Command-related Pydantic models."""

from opencode.models._base import OpenCodeModel


class Command(OpenCodeModel):
    """
    Represents a command definition.

    Commands are user-defined actions that can be executed with
    specific templates and optional agent/model configurations.
    """

    name: str
    """The name of the command."""

    description: str | None = None
    """Human-readable description of what the command does."""

    agent: str | None = None
    """The agent to use for executing the command."""

    model: str | None = None
    """The model to use for the command."""

    template: str
    """The template string for the command."""

    subtask: bool | None = None
    """Whether this command runs as a subtask."""
