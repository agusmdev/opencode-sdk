"""Base resource class and HTTP helpers for the SDK."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, TypeVar, overload

import httpx

from opencode._constants import DEFAULT_TIMEOUT
from opencode._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from opencode._logging import get_logger

if TYPE_CHECKING:
    from opencode._client import OpenCode

T = TypeVar("T")


class BaseResource:
    """Base class for all API resources."""

    def __init__(self, client: "OpenCode") -> None:
        """Initialize the resource with a client reference."""
        self._client = client
        self._log = get_logger(f"opencode.{self.__class__.__name__.lower()}")

    @property
    def _http(self) -> httpx.AsyncClient:
        """Get the HTTP client."""
        return self._client._http

    @property
    def _directory(self) -> str | None:
        """Get the default directory."""
        return self._client._directory

    def _build_params(self, **kwargs: Any) -> dict[str, Any]:
        """
        Build query parameters, injecting directory if set.
        
        Filters out None values and adds default directory if not specified.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        if self._directory and "directory" not in params:
            params["directory"] = self._directory
        return params

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> Any:
        """
        Make an HTTP request and handle errors.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (e.g., "/session")
            params: Query parameters
            json_data: JSON body data
            timeout: Optional request timeout override
            
        Returns:
            Parsed JSON response
            
        Raises:
            BadRequestError: For 400 responses
            NotFoundError: For 404 responses
            AuthenticationError: For 401/403 responses
            RateLimitError: For 429 responses
            ServerError: For 5xx responses
            ConnectionError: For network errors
            APIError: For other HTTP errors
        """
        self._log.debug(
            "request_start",
            method=method,
            path=path,
            params=params,
        )
        
        try:
            response = await self._http.request(
                method,
                path,
                params=params,
                json=json_data,
                timeout=timeout or DEFAULT_TIMEOUT,
            )
        except httpx.ConnectError as e:
            raise ConnectionError(
                f"Failed to connect to API server",
                url=str(self._http.base_url) + path,
                cause=e,
            ) from e
        except httpx.TimeoutException as e:
            raise ConnectionError(
                f"Request timed out",
                url=str(self._http.base_url) + path,
                cause=e,
            ) from e

        self._log.debug(
            "request_complete",
            method=method,
            path=path,
            status_code=response.status_code,
        )

        self._raise_for_status(response)
        
        # Handle empty responses (204 No Content)
        if response.status_code == 204 or not response.content:
            return None
            
        return response.json()

    def _raise_for_status(self, response: httpx.Response) -> None:
        """
        Check response status and raise appropriate exception.
        
        Parses error body and creates typed exceptions.
        """
        if response.is_success:
            return

        # Try to parse error body
        error_body: dict[str, Any] | None = None
        error_message = "Unknown error"
        error_type: str | None = None
        
        try:
            error_body = response.json()
            # Handle structured errors like {"name": "NotFoundError", "data": {"message": "..."}}
            if isinstance(error_body, dict):
                if "name" in error_body and "data" in error_body:
                    error_type = error_body.get("name")
                    error_data = error_body.get("data", {})
                    error_message = error_data.get("message", error_message)
                # Handle validation errors like {"errors": [...], "success": false}
                elif "errors" in error_body:
                    errors = error_body.get("errors", [])
                    if errors:
                        error_message = str(errors[0]) if errors else "Validation error"
        except (json.JSONDecodeError, ValueError):
            error_message = response.text or f"HTTP {response.status_code}"

        status_code = response.status_code

        if status_code == 400:
            raise BadRequestError(
                error_message,
                errors=error_body.get("errors") if error_body else None,
                response_body=error_body,
            )
        elif status_code == 404:
            raise NotFoundError(
                error_message,
                response_body=error_body,
            )
        elif status_code in (401, 403):
            provider_id = None
            if error_body and error_body.get("name") == "ProviderAuthError":
                provider_id = error_body.get("data", {}).get("providerID")
            raise AuthenticationError(
                error_message,
                status_code=status_code,
                provider_id=provider_id,
                response_body=error_body,
            )
        elif status_code == 429:
            retry_after = None
            if "retry-after" in response.headers:
                try:
                    retry_after = float(response.headers["retry-after"])
                except ValueError:
                    pass
            raise RateLimitError(
                error_message,
                retry_after=retry_after,
                response_body=error_body,
            )
        elif status_code >= 500:
            raise ServerError(
                error_message,
                status_code=status_code,
                response_body=error_body,
            )
        else:
            raise APIError(
                error_message,
                status_code=status_code,
                error_type=error_type,
                response_body=error_body,
            )
