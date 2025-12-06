"""Auth resource for authentication management."""
from __future__ import annotations
from opencode._base import BaseResource
from opencode.models.auth import Auth

class AuthResource(BaseResource):
    """Manage authentication credentials."""

    async def set(self, provider_id: str, auth: Auth, *, directory: str | None = None) -> bool:
        """Set authentication credentials for a provider. PUT /auth/{id}"""
        params = self._build_params(directory=directory)
        return await self._request("PUT", f"/auth/{provider_id}", params=params, json_data=auth.model_dump(by_alias=True))
