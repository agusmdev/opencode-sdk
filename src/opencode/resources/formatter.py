"""Formatter resource for code formatter status."""

from __future__ import annotations

from typing import Literal

from opencode._base import BaseResource
from opencode.models._base import OpenCodeModel


class FormatterStatus(OpenCodeModel):
    """
    Represents the status of a code formatter.

    Contains information about the formatter's identity and connection status.
    """

    id: str
    """Unique identifier for the formatter."""

    name: str
    """Human-readable name of the formatter."""

    root: str
    """The root directory that the formatter is operating on."""

    status: Literal["connected", "error"]
    """The current connection status of the formatter."""


class FormatterResource(BaseResource):
    """
    Access code formatter status.

    Provides information about configured code formatters and their
    connection status.
    """

    async def status(self, *, directory: str | None = None) -> list[FormatterStatus]:
        """
        Get the status of all code formatters.

        Args:
            directory: Optional working directory override.

        Returns:
            List of formatter status objects.
        """
        self._log.debug("getting_formatter_status")
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/formatter", params=params)
        formatters = [FormatterStatus.model_validate(item) for item in data]
        self._log.debug("formatter_status_retrieved", count=len(formatters))
        return formatters
