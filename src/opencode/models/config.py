"""Configuration models for OpenCode settings."""

from typing import Any, Literal

from pydantic import Field

from opencode.models._base import OpenCodeModel


# Permission value types
PermissionValue = Literal["ask", "allow", "deny"]


class PermissionConfig(OpenCodeModel):
    """
    Permission settings for various operations.

    Controls whether operations require user confirmation,
    are automatically allowed, or are denied.
    """

    edit: PermissionValue | None = None
    """Permission for file edit operations."""

    bash: PermissionValue | dict[str, Any] | None = None
    """Permission for bash command execution. Can be a value or detailed config."""

    webfetch: PermissionValue | None = None
    """Permission for web fetch operations."""

    doom_loop: PermissionValue | None = Field(default=None, alias="doomLoop")
    """Permission for doom loop detection."""

    external_directory: PermissionValue | None = Field(
        default=None, alias="externalDirectory"
    )
    """Permission for accessing external directories."""


class AgentConfig(OpenCodeModel):
    """
    Configuration for an AI agent.

    Defines the model, behavior, and permissions for an agent.
    """

    model: str | None = None
    """The model identifier to use for this agent."""

    temperature: float | None = None
    """Temperature setting for response generation."""

    top_p: float | None = Field(default=None, alias="topP")
    """Top-p (nucleus) sampling parameter."""

    prompt: str | None = None
    """System prompt for the agent."""

    tools: dict[str, Any] | None = None
    """Tool configurations for the agent."""

    disable: bool | None = None
    """Whether this agent is disabled."""

    description: str | None = None
    """Description of the agent's purpose."""

    mode: Literal["subagent", "primary", "all"] | None = None
    """Agent execution mode."""

    color: str | None = None
    """Hex color code for the agent (pattern: ^#[0-9a-fA-F]{6}$)."""

    max_steps: int | None = Field(default=None, alias="maxSteps")
    """Maximum number of steps the agent can take."""

    permission: PermissionConfig | None = None
    """Permission settings specific to this agent."""


class McpLocalConfig(OpenCodeModel):
    """
    Configuration for a local MCP (Model Context Protocol) server.

    Runs a local command as an MCP server.
    """

    type: Literal["local"]
    """Server type identifier."""

    command: list[str]
    """Command and arguments to execute."""

    environment: dict[str, str] | None = None
    """Environment variables for the command."""

    enabled: bool | None = None
    """Whether this MCP server is enabled."""

    timeout: int | None = None
    """Timeout in milliseconds for server operations."""


class McpRemoteConfig(OpenCodeModel):
    """
    Configuration for a remote MCP (Model Context Protocol) server.

    Connects to a remote MCP server via URL.
    """

    type: Literal["remote"]
    """Server type identifier."""

    url: str
    """URL of the remote MCP server."""

    enabled: bool | None = None
    """Whether this MCP server is enabled."""

    headers: dict[str, str] | None = None
    """HTTP headers for authentication or other purposes."""

    timeout: int | None = None
    """Timeout in milliseconds for server operations."""


McpConfig = McpLocalConfig | McpRemoteConfig
"""Union type for MCP server configurations."""


class ProviderOptions(OpenCodeModel):
    """
    Connection options for an AI provider.

    Contains authentication and endpoint configuration.
    """

    api_key: str | None = Field(default=None, alias="apiKey")
    """API key for authentication."""

    base_url: str | None = Field(default=None, alias="baseURL")
    """Base URL for the API endpoint."""

    enterprise_url: str | None = Field(default=None, alias="enterpriseUrl")
    """Enterprise-specific URL override."""

    set_cache_key: bool | None = Field(default=None, alias="setCacheKey")
    """Whether to set cache key for requests."""

    timeout: int | Literal[False] | None = None
    """Request timeout in milliseconds, or false to disable."""


class ProviderConfig(OpenCodeModel):
    """
    Configuration for an AI model provider.

    Defines connection settings and model configurations for a provider.
    """

    api: str | None = None
    """API type identifier."""

    name: str | None = None
    """Display name of the provider."""

    env: list[str] | None = None
    """Environment variable names for configuration."""

    id: str | None = None
    """Unique provider identifier."""

    npm: str | None = None
    """NPM package name for the provider."""

    models: dict[str, Any] | None = None
    """Model-specific configurations."""

    whitelist: list[str] | None = None
    """List of allowed models."""

    blacklist: list[str] | None = None
    """List of blocked models."""

    options: ProviderOptions | None = None
    """Connection options for this provider."""


class KeybindsConfig(OpenCodeModel):
    """
    Keyboard shortcut configuration.

    Defines key bindings for various application actions.
    """

    leader: str | None = None
    """Leader key for command sequences."""

    app_exit: str | None = Field(default=None, alias="appExit")
    """Keybind to exit the application."""

    editor_open: str | None = Field(default=None, alias="editorOpen")
    """Keybind to open the editor."""

    theme_list: str | None = Field(default=None, alias="themeList")
    """Keybind to show theme list."""

    session_new: str | None = Field(default=None, alias="sessionNew")
    """Keybind to create a new session."""

    session_list: str | None = Field(default=None, alias="sessionList")
    """Keybind to show session list."""

    session_share: str | None = Field(default=None, alias="sessionShare")
    """Keybind to share the current session."""

    history_previous: str | None = Field(default=None, alias="historyPrevious")
    """Keybind to navigate to previous history item."""

    history_next: str | None = Field(default=None, alias="historyNext")
    """Keybind to navigate to next history item."""

    input_clear: str | None = Field(default=None, alias="inputClear")
    """Keybind to clear input."""

    input_paste: str | None = Field(default=None, alias="inputPaste")
    """Keybind to paste from clipboard."""

    input_submit: str | None = Field(default=None, alias="inputSubmit")
    """Keybind to submit input."""

    messages_page_up: str | None = Field(default=None, alias="messagesPageUp")
    """Keybind to scroll messages up."""

    messages_page_down: str | None = Field(default=None, alias="messagesPageDown")
    """Keybind to scroll messages down."""


class TuiConfig(OpenCodeModel):
    """
    Terminal UI configuration.

    Settings for the terminal user interface appearance and behavior.
    """

    scroll_speed: int | None = Field(default=None, alias="scrollSpeed")
    """Number of lines to scroll per scroll event."""

    diff_style: Literal["unified", "split"] | None = Field(
        default=None, alias="diffStyle"
    )
    """Style for displaying diffs."""

    show_line_numbers: bool | None = Field(default=None, alias="showLineNumbers")
    """Whether to show line numbers in code blocks."""

    word_wrap: bool | None = Field(default=None, alias="wordWrap")
    """Whether to wrap long lines."""

    syntax_highlight: bool | None = Field(default=None, alias="syntaxHighlight")
    """Whether to enable syntax highlighting."""


class Config(OpenCodeModel):
    """
    Main OpenCode configuration.

    Top-level configuration object containing all settings.
    """

    schema_: str | None = Field(default=None, alias="$schema")
    """JSON schema URL for validation."""

    theme: str | None = None
    """Theme name or path."""

    keybinds: KeybindsConfig | None = None
    """Keyboard shortcut configuration."""

    tui: TuiConfig | None = None
    """Terminal UI settings."""

    command: dict[str, Any] | None = None
    """Custom command configurations."""

    watcher: dict[str, Any] | None = None
    """File watcher settings."""

    plugin: list[str] | None = None
    """List of enabled plugins."""

    snapshot: bool | None = None
    """Whether to enable snapshots."""

    share: Literal["manual", "auto", "disabled"] | None = None
    """Session sharing mode."""

    autoupdate: bool | dict[str, Any] | None = None
    """Auto-update configuration."""

    disabled_providers: list[str] | None = Field(
        default=None, alias="disabledProviders"
    )
    """List of disabled provider IDs."""

    enabled_providers: list[str] | None = Field(default=None, alias="enabledProviders")
    """List of enabled provider IDs."""

    model: str | None = None
    """Default model identifier."""

    small_model: str | None = Field(default=None, alias="smallModel")
    """Model for lightweight tasks."""

    username: str | None = None
    """Username for display."""

    agent: dict[str, AgentConfig] | None = None
    """Agent configurations by name."""

    provider: dict[str, ProviderConfig] | None = None
    """Provider configurations by ID."""

    mcp: dict[str, McpConfig] | None = None
    """MCP server configurations by name."""

    formatter: dict[str, Any] | None = None
    """Code formatter settings."""

    lsp: dict[str, Any] | None = None
    """Language server protocol settings."""

    instructions: list[str] | None = None
    """Custom instructions for the AI."""

    permission: PermissionConfig | None = None
    """Global permission settings."""

    tools: dict[str, Any] | None = None
    """Tool configurations."""

    enterprise: dict[str, Any] | None = None
    """Enterprise-specific settings."""

    experimental: dict[str, Any] | None = None
    """Experimental feature flags."""
