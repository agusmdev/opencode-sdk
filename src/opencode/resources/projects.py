"""Projects resource for managing OpenCode projects."""

from __future__ import annotations

from opencode._base import BaseResource
from opencode.models.project import Project


class ProjectsResource(BaseResource):
    """
    Manage OpenCode projects.

    Projects represent worktree directories (typically git repositories)
    that OpenCode operates on.
    """

    async def list(self, *, directory: str | None = None) -> list[Project]:
        """
        List all available projects.

        Args:
            directory: Optional working directory override.

        Returns:
            List of all projects.
        """
        self._log.debug("listing_projects")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/project", params=params)
        projects = [Project.model_validate(item) for item in data]
        self._log.info("projects_listed", count=len(projects))
        return projects

    async def current(self, *, directory: str | None = None) -> Project:
        """
        Get the current project.

        Returns the project for the current working directory.

        Args:
            directory: Optional working directory override.

        Returns:
            The current project.

        Raises:
            NotFoundError: If no project exists for the directory.
        """
        self._log.debug("getting_current_project")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/project/current", params=params)
        project = Project.model_validate(data)
        self._log.debug("current_project_retrieved", project_id=project.id)
        return project
