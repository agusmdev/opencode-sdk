"""Agents resource for managing AI agents."""

from __future__ import annotations

from opencode._base import BaseResource
from opencode.models.agent import Agent


class AgentsResource(BaseResource):
    """
    Access AI agent configurations.

    Agents are specialized AI assistants with specific configurations,
    prompts, tools, and behavioral settings.
    """

    async def list(self, *, directory: str | None = None) -> list[Agent]:
        """
        List all available agents.

        Args:
            directory: Optional working directory override.

        Returns:
            List of agent configurations.
        """
        self._log.debug("listing_agents")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/agent", params=params)
        agents = [Agent.model_validate(item) for item in data]
        self._log.info("agents_listed", count=len(agents))
        return agents
