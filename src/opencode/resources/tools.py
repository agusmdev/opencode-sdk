"""Tools resource for tool management."""
from __future__ import annotations
from opencode._base import BaseResource
from opencode.models.tool import ToolListItem

class ToolsResource(BaseResource):
    """Manage tools."""

    async def list_ids(self, *, directory: str | None = None) -> list[str]:
        """List all tool IDs. GET /experimental/tool/ids"""
        params = self._build_params(directory=directory)
        return await self._request("GET", "/experimental/tool/ids", params=params)

    async def list(self, *, provider: str, model: str, directory: str | None = None) -> list[ToolListItem]:
        """List tools with JSON schema for a provider/model. GET /experimental/tool"""
        params = self._build_params(directory=directory, provider=provider, model=model)
        data = await self._request("GET", "/experimental/tool", params=params)
        return [ToolListItem.model_validate(item) for item in data]
