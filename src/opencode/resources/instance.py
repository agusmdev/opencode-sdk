"""Instance resource for managing OpenCode server instances."""

from __future__ import annotations

from opencode._base import BaseResource


class InstanceResource(BaseResource):
    """
    Manage OpenCode server instances.

    Provides methods to control the OpenCode server instance lifecycle.
    """

    async def dispose(self, *, directory: str | None = None) -> bool:
        """
        Dispose of the current server instance.

        Terminates the OpenCode server instance, cleaning up resources.

        Args:
            directory: Optional working directory override.

        Returns:
            True if the instance was disposed successfully.
        """
        self._log.debug("disposing_instance")
        params = self._build_params(directory=directory)
        await self._request("POST", "/instance/dispose", params=params)
        self._log.info("instance_disposed")
        return True
