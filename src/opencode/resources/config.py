"""Config resource for managing OpenCode configuration."""

from __future__ import annotations

from opencode._base import BaseResource
from opencode.models.config import Config


class ConfigResource(BaseResource):
    """
    Manage OpenCode configuration.

    Provides access to read and update the current configuration settings.
    """

    async def get(self, *, directory: str | None = None) -> Config:
        """
        Get the current configuration.

        Args:
            directory: Optional working directory override.

        Returns:
            The current configuration.
        """
        self._log.debug("getting_config")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/config", params=params)
        config = Config.model_validate(data)
        self._log.debug("config_retrieved")
        return config

    async def update(
        self,
        config: Config,
        *,
        directory: str | None = None,
    ) -> Config:
        """
        Update the configuration.

        Args:
            config: The configuration updates to apply.
            directory: Optional working directory override.

        Returns:
            The updated configuration.
        """
        self._log.debug("updating_config")
        params = self._build_params(directory=directory)
        data = await self._request(
            "PATCH",
            "/config",
            params=params,
            json_data=config.model_dump(by_alias=True, exclude_none=True),
        )
        updated_config = Config.model_validate(data)
        self._log.info("config_updated")
        return updated_config
