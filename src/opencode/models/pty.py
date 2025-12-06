"""PTY (pseudo-terminal) related Pydantic models."""

from typing import Literal

from opencode.models._base import OpenCodeModel


class Pty(OpenCodeModel):
    """
    Represents a pseudo-terminal (PTY) instance.

    A PTY is a terminal session running a command, with its own
    process ID and lifecycle status.
    """

    id: str
    """Unique identifier for the PTY, matching pattern ^pty.*"""

    title: str
    """Display title for the PTY session."""

    command: str
    """The command being executed in the PTY."""

    args: list[str]
    """Command-line arguments passed to the command."""

    cwd: str
    """Current working directory of the PTY."""

    status: Literal["running", "exited"]
    """Current status of the PTY process."""

    pid: int
    """Process ID of the PTY."""
