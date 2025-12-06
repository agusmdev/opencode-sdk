"""VCS resource for version control system information."""

from __future__ import annotations

from typing import TypedDict

from opencode._base import BaseResource


class VcsInfo(TypedDict):
    """Version control system information."""

    branch: str
    """The current branch name."""


class VcsResource(BaseResource):
    """
    Access version control system information.

    Provides information about the current VCS state, such as the
    active branch.
    """

    async def get(self, *, directory: str | None = None) -> VcsInfo:
        """
        Get version control system information.

        Args:
            directory: Optional working directory override.

        Returns:
            Dictionary containing VCS information with the current branch.

        Raises:
            NotFoundError: If no VCS is available for the directory.
        """
        self._log.debug("getting_vcs_info")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/vcs", params=params)
        self._log.debug("vcs_info_retrieved", branch=data.get("branch"))
        return VcsInfo(branch=data["branch"])
