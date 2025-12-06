"""LSP (Language Server Protocol) related Pydantic models."""

from typing import Literal

from opencode.models._base import OpenCodeModel


class LSPStatus(OpenCodeModel):
    """
    Represents the status of a Language Server Protocol server.

    Contains information about the LSP server's identity and connection status.
    """

    id: str
    """Unique identifier for the LSP server."""

    name: str
    """Human-readable name of the LSP server."""

    root: str
    """The root directory that the LSP server is operating on."""

    status: Literal["connected", "error"]
    """The current connection status of the LSP server."""
