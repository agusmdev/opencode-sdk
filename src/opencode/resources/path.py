"""Path resource for OpenCode path information."""

from __future__ import annotations

from typing import TypedDict

from opencode._base import BaseResource


class PathInfo(TypedDict):
    """OpenCode path information."""

    state: str
    """Path to the state directory."""

    config: str
    """Path to the configuration directory."""

    worktree: str
    """Path to the worktree directory."""

    directory: str
    """Path to the current working directory."""


class PathResource(BaseResource):
    """
    Access OpenCode path information.

    Provides paths to various OpenCode directories including state,
    configuration, worktree, and the current working directory.
    """

    async def get(self, *, directory: str | None = None) -> PathInfo:
        """
        Get OpenCode path information.

        Args:
            directory: Optional working directory override.

        Returns:
            Dictionary containing path information for state, config,
            worktree, and directory.
        """
        self._log.debug("getting_path_info")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/path", params=params)
        self._log.debug("path_info_retrieved")
        return PathInfo(
            state=data["state"],
            config=data["config"],
            worktree=data["worktree"],
            directory=data["directory"],
        )
