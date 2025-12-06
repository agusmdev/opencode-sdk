"""Project-related Pydantic models."""

from typing import Literal

from pydantic import Field

from opencode.models._base import OpenCodeModel


class ProjectTime(OpenCodeModel):
    """
    Timestamp information for project lifecycle.

    Tracks when a project was created and optionally when it was initialized.
    """

    created: float
    """Unix timestamp when the project was created."""

    initialized: float | None = None
    """Unix timestamp when the project was initialized, or None if not yet initialized."""


class Project(OpenCodeModel):
    """
    Represents an OpenCode project.

    A project corresponds to a worktree directory, typically a git repository,
    that OpenCode operates on.
    """

    id: str
    """Unique identifier for the project."""

    worktree: str
    """Path to the project's worktree directory."""

    vcs_dir: str | None = Field(default=None, alias="vcsDir")
    """Path to the version control system directory (e.g., .git), if applicable."""

    vcs: Literal["git"] | None = None
    """The version control system used by the project."""

    time: ProjectTime
    """Timestamp information for the project."""
