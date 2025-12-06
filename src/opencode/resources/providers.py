"""Providers resource for AI provider management."""
from __future__ import annotations
from typing import Any
from opencode._base import BaseResource
from opencode.models.provider import Provider, ProviderAuthMethod, ProviderAuthAuthorization

class ProvidersResource(BaseResource):
    """Manage AI providers and authentication."""

    async def list(self, *, directory: str | None = None) -> dict[str, Any]:
        """List all providers with their models. GET /provider"""
        params = self._build_params(directory=directory)
        return await self._request("GET", "/provider", params=params)

    async def list_configured(self, *, directory: str | None = None) -> dict[str, Any]:
        """List configured providers. GET /config/providers"""
        params = self._build_params(directory=directory)
        return await self._request("GET", "/config/providers", params=params)

    async def get_auth_methods(self, *, directory: str | None = None) -> dict[str, list[ProviderAuthMethod]]:
        """Get authentication methods for all providers. GET /provider/auth"""
        params = self._build_params(directory=directory)
        data = await self._request("GET", "/provider/auth", params=params)
        return {
            provider_id: [ProviderAuthMethod.model_validate(m) for m in methods]
            for provider_id, methods in data.items()
        }

    async def authorize(self, provider_id: str, *, method: int, directory: str | None = None) -> ProviderAuthAuthorization:
        """Start OAuth authorization. POST /provider/{id}/oauth/authorize"""
        params = self._build_params(directory=directory)
        data = await self._request("POST", f"/provider/{provider_id}/oauth/authorize", params=params, json_data={"method": method})
        return ProviderAuthAuthorization.model_validate(data)

    async def oauth_callback(self, provider_id: str, *, method: int, code: str | None = None, directory: str | None = None) -> bool:
        """Complete OAuth callback. POST /provider/{id}/oauth/callback"""
        params = self._build_params(directory=directory)
        body: dict[str, Any] = {"method": method}
        if code:
            body["code"] = code
        return await self._request("POST", f"/provider/{provider_id}/oauth/callback", params=params, json_data=body)
