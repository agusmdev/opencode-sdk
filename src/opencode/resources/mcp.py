"""MCP resource for Model Context Protocol server management."""
from __future__ import annotations
from typing import Any
from opencode._base import BaseResource
from opencode.models.mcp import MCPStatus
from opencode.models.config import McpLocalConfig, McpRemoteConfig

class McpResource(BaseResource):
    """Manage MCP servers."""

    async def status(self, *, directory: str | None = None) -> dict[str, MCPStatus]:
        """Get MCP server status. GET /mcp"""
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/mcp", params=params)
        return {name: MCPStatus.model_validate(status) for name, status in data.items()}

    async def add(self, name: str, config: McpLocalConfig | McpRemoteConfig, *, directory: str | None = None) -> dict[str, MCPStatus]:
        """Add an MCP server. POST /mcp"""
        params = self._build_params(directory=directory)
        body = {"name": name, "config": config.model_dump(by_alias=True)}
        data = await self._request("POST", "/mcp", params=params, json_data=body)
        return {n: MCPStatus.model_validate(s) for n, s in data.items()}
