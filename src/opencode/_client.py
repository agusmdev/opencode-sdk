"""Main OpenCode client."""

from __future__ import annotations

from typing import Any

import httpx

from opencode._constants import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, USER_AGENT
from opencode._logging import get_logger


class OpenCode:
    """
    OpenCode API client.
    
    The main entry point for interacting with the OpenCode API.
    Provides access to all API resources through typed properties.
    
    Example:
        async with OpenCode() as client:
            # Create a session
            session = await client.sessions.create(title="My Session")
            
            # Send a prompt
            response = await client.sessions.prompt(
                session.id,
                parts=[TextPartInput(type="text", text="Hello!")]
            )
            
            # Stream events
            async for event in client.events.subscribe():
                print(event)
    
    Args:
        base_url: Base URL for the API (default: http://127.0.0.1:1122)
        directory: Default project directory for all requests
        timeout: Default request timeout in seconds
        headers: Additional HTTP headers to include in all requests
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        directory: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize the OpenCode client."""
        self._base_url = base_url
        self._directory = directory
        self._timeout = timeout
        self._log = get_logger("opencode.client")
        
        # Build headers
        default_headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if headers:
            default_headers.update(headers)
        
        # Create HTTP client
        self._http = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers=default_headers,
        )
        
        # Initialize resources lazily
        self._sessions: SessionsResource | None = None
        self._events: EventsResource | None = None
        self._projects: ProjectsResource | None = None
        self._providers: ProvidersResource | None = None
        self._config: ConfigResource | None = None
        self._files: FilesResource | None = None
        self._find: FindResource | None = None
        self._tools: ToolsResource | None = None
        self._mcp: McpResource | None = None
        self._lsp: LspResource | None = None
        self._agents: AgentsResource | None = None
        self._commands: CommandsResource | None = None
        self._auth: AuthResource | None = None
        self._pty: PtyResource | None = None
        self._vcs: VcsResource | None = None
        self._path: PathResource | None = None
        self._instance: InstanceResource | None = None
        self._formatter: FormatterResource | None = None
        self._tui: TuiResource | None = None
        
        self._log.debug(
            "client_initialized",
            base_url=base_url,
            directory=directory,
        )

    # Resource properties with lazy initialization
    
    @property
    def sessions(self) -> "SessionsResource":
        """Access session management operations."""
        if self._sessions is None:
            from opencode.resources.sessions import SessionsResource
            self._sessions = SessionsResource(self)
        return self._sessions

    @property
    def events(self) -> "EventsResource":
        """Access real-time event streaming."""
        if self._events is None:
            from opencode.resources.events import EventsResource
            self._events = EventsResource(self)
        return self._events

    @property
    def projects(self) -> "ProjectsResource":
        """Access project operations."""
        if self._projects is None:
            from opencode.resources.projects import ProjectsResource
            self._projects = ProjectsResource(self)
        return self._projects

    @property
    def providers(self) -> "ProvidersResource":
        """Access AI provider management."""
        if self._providers is None:
            from opencode.resources.providers import ProvidersResource
            self._providers = ProvidersResource(self)
        return self._providers

    @property
    def config(self) -> "ConfigResource":
        """Access configuration operations."""
        if self._config is None:
            from opencode.resources.config import ConfigResource
            self._config = ConfigResource(self)
        return self._config

    @property
    def files(self) -> "FilesResource":
        """Access file operations."""
        if self._files is None:
            from opencode.resources.files import FilesResource
            self._files = FilesResource(self)
        return self._files

    @property
    def find(self) -> "FindResource":
        """Access search operations."""
        if self._find is None:
            from opencode.resources.find import FindResource
            self._find = FindResource(self)
        return self._find

    @property
    def tools(self) -> "ToolsResource":
        """Access tool management."""
        if self._tools is None:
            from opencode.resources.tools import ToolsResource
            self._tools = ToolsResource(self)
        return self._tools

    @property
    def mcp(self) -> "McpResource":
        """Access MCP server management."""
        if self._mcp is None:
            from opencode.resources.mcp import McpResource
            self._mcp = McpResource(self)
        return self._mcp

    @property
    def lsp(self) -> "LspResource":
        """Access LSP server status."""
        if self._lsp is None:
            from opencode.resources.lsp import LspResource
            self._lsp = LspResource(self)
        return self._lsp

    @property
    def agents(self) -> "AgentsResource":
        """Access agent configuration."""
        if self._agents is None:
            from opencode.resources.agents import AgentsResource
            self._agents = AgentsResource(self)
        return self._agents

    @property
    def commands(self) -> "CommandsResource":
        """Access custom commands."""
        if self._commands is None:
            from opencode.resources.commands import CommandsResource
            self._commands = CommandsResource(self)
        return self._commands

    @property
    def auth(self) -> "AuthResource":
        """Access authentication management."""
        if self._auth is None:
            from opencode.resources.auth import AuthResource
            self._auth = AuthResource(self)
        return self._auth

    @property
    def pty(self) -> "PtyResource":
        """Access PTY session management."""
        if self._pty is None:
            from opencode.resources.pty import PtyResource
            self._pty = PtyResource(self)
        return self._pty

    @property
    def vcs(self) -> "VcsResource":
        """Access version control info."""
        if self._vcs is None:
            from opencode.resources.vcs import VcsResource
            self._vcs = VcsResource(self)
        return self._vcs

    @property
    def path(self) -> "PathResource":
        """Access path information."""
        if self._path is None:
            from opencode.resources.path import PathResource
            self._path = PathResource(self)
        return self._path

    @property
    def instance(self) -> "InstanceResource":
        """Access instance management."""
        if self._instance is None:
            from opencode.resources.instance import InstanceResource
            self._instance = InstanceResource(self)
        return self._instance

    @property
    def formatter(self) -> "FormatterResource":
        """Access formatter status."""
        if self._formatter is None:
            from opencode.resources.formatter import FormatterResource
            self._formatter = FormatterResource(self)
        return self._formatter

    @property
    def tui(self) -> "TuiResource":
        """Access TUI control operations."""
        if self._tui is None:
            from opencode.resources.tui import TuiResource
            self._tui = TuiResource(self)
        return self._tui

    # Lifecycle methods

    async def close(self) -> None:
        """
        Close the client and release resources.
        
        Should be called when done using the client.
        Alternatively, use the client as an async context manager.
        """
        self._log.debug("closing_client")
        await self._http.aclose()
        self._log.info("client_closed")

    async def __aenter__(self) -> "OpenCode":
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit async context manager and close client."""
        await self.close()

    def __repr__(self) -> str:
        """Return string representation."""
        return f"OpenCode(base_url={self._base_url!r}, directory={self._directory!r})"


# Type hints for lazy imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opencode.resources.agents import AgentsResource
    from opencode.resources.auth import AuthResource
    from opencode.resources.commands import CommandsResource
    from opencode.resources.config import ConfigResource
    from opencode.resources.events import EventsResource
    from opencode.resources.files import FilesResource
    from opencode.resources.find import FindResource
    from opencode.resources.formatter import FormatterResource
    from opencode.resources.instance import InstanceResource
    from opencode.resources.lsp import LspResource
    from opencode.resources.mcp import McpResource
    from opencode.resources.path import PathResource
    from opencode.resources.projects import ProjectsResource
    from opencode.resources.providers import ProvidersResource
    from opencode.resources.pty import PtyResource
    from opencode.resources.sessions import SessionsResource
    from opencode.resources.tools import ToolsResource
    from opencode.resources.tui import TuiResource
    from opencode.resources.vcs import VcsResource
