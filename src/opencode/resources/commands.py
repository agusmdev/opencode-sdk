"""Commands resource for managing custom commands."""

from __future__ import annotations

from opencode._base import BaseResource
from opencode.models.command import Command


class CommandsResource(BaseResource):
    """
    Access custom command definitions.

    Commands are user-defined actions that can be executed with
    specific templates and optional agent/model configurations.
    """

    async def list(self, *, directory: str | None = None) -> list[Command]:
        """
        List all available commands.

        Args:
            directory: Optional working directory override.

        Returns:
            List of command definitions.
        """
        self._log.debug("listing_commands")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/command", params=params)
        commands = [Command.model_validate(item) for item in data]
        self._log.info("commands_listed", count=len(commands))
        return commands
