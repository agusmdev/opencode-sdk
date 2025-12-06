"""Tool-related Pydantic models."""

from typing import Any

from opencode.models._base import OpenCodeModel


class ToolListItem(OpenCodeModel):
    """
    Represents a tool available in the system.

    Contains the tool's identifier, description, and its parameter schema.
    """

    id: str
    """Unique identifier for the tool."""

    description: str
    """Human-readable description of what the tool does."""

    parameters: dict[str, Any]
    """JSON Schema describing the tool's parameters."""
