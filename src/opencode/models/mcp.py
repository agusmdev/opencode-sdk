"""MCP (Model Context Protocol) related Pydantic models."""

from typing import Literal, Union

from pydantic import Field

from opencode.models._base import OpenCodeModel


class MCPStatusConnected(OpenCodeModel):
    """
    Represents a connected MCP server status.

    Indicates that the MCP server is successfully connected and operational.
    """

    status: Literal["connected"]
    """The status indicating the MCP server is connected."""


class MCPStatusDisabled(OpenCodeModel):
    """
    Represents a disabled MCP server status.

    Indicates that the MCP server is disabled and not in use.
    """

    status: Literal["disabled"]
    """The status indicating the MCP server is disabled."""


class MCPStatusFailed(OpenCodeModel):
    """
    Represents a failed MCP server status.

    Indicates that the MCP server failed to connect, with an error message.
    """

    status: Literal["failed"]
    """The status indicating the MCP server connection failed."""

    error: str
    """The error message describing why the connection failed."""


MCPStatus = Union[MCPStatusConnected, MCPStatusDisabled, MCPStatusFailed]
"""
Union type representing all possible MCP server statuses.

Can be one of: connected, disabled, or failed.
"""
