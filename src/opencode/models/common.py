"""Common/shared Pydantic models used across the SDK."""

from pydantic import Field

from opencode.models._base import OpenCodeModel


class Position(OpenCodeModel):
    """
    Represents a position in a text document.

    Used to specify locations within files, such as cursor positions
    or the start/end of a text range.
    """

    line: int
    """Zero-based line number."""

    character: int
    """Zero-based character offset within the line."""


class Range(OpenCodeModel):
    """
    Represents a range in a text document.

    A range is defined by a start and end position, commonly used
    to specify text selections or regions of interest in a file.
    """

    start: Position
    """The start position of the range (inclusive)."""

    end: Position
    """The end position of the range (exclusive)."""


class FileDiff(OpenCodeModel):
    """
    Represents a diff for a single file.

    Contains the file path, before/after content snapshots,
    and statistics about the changes made.
    """

    file: str
    """The path to the file that was modified."""

    before: str
    """The content of the file before the change."""

    after: str
    """The content of the file after the change."""

    additions: int
    """The number of lines added."""

    deletions: int
    """The number of lines deleted."""


class Time(OpenCodeModel):
    """
    Timestamp information for resource creation and updates.

    Contains Unix timestamps (seconds since epoch) for tracking
    when a resource was created and last modified.
    """

    created: float
    """Unix timestamp when the resource was created."""

    updated: float
    """Unix timestamp when the resource was last updated."""


class TimeWithCompleted(Time):
    """
    Extended timestamp information including completion time.

    Inherits creation and update timestamps from Time, and adds
    an optional completion timestamp for trackable tasks.
    """

    completed: float | None = None
    """Unix timestamp when the resource was completed, or None if not yet completed."""


class ModelConfig(OpenCodeModel):
    """
    Configuration identifying a specific AI model.

    Specifies both the provider (e.g., 'anthropic', 'openai') and
    the specific model identifier within that provider's offerings.
    """

    provider_id: str = Field(alias="providerID")
    """The identifier of the model provider (e.g., 'anthropic', 'openai')."""

    model_id: str = Field(alias="modelID")
    """The identifier of the specific model (e.g., 'claude-3-opus', 'gpt-4')."""
