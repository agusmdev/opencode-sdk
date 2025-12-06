"""LSP resource for Language Server Protocol status."""

from __future__ import annotations

from opencode._base import BaseResource
from opencode.models.lsp import LSPStatus


class LspResource(BaseResource):
    """
    Access Language Server Protocol (LSP) status.

    Provides information about configured LSP servers and their
    connection status.
    """

    async def status(self, *, directory: str | None = None) -> list[LSPStatus]:
        """
        Get the status of all LSP servers.

        Args:
            directory: Optional working directory override.

        Returns:
            List of LSP server status objects.
        """
        self._log.debug("getting_lsp_status")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/lsp", params=params)
        servers = [LSPStatus.model_validate(item) for item in data]
        self._log.debug("lsp_status_retrieved", count=len(servers))
        return servers
