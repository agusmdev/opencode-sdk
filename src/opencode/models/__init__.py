"""OpenCode SDK models - Pydantic models for API data structures."""

from opencode.models._base import InputModel, OpenCodeModel
from opencode.models.agent import Agent
from opencode.models.auth import ApiAuth, Auth, OAuth, WellKnownAuth
from opencode.models.command import Command
from opencode.models.common import (
    FileDiff,
    ModelConfig,
    Range,
    Position,
    Time,
    TimeWithCompleted,
)
from opencode.models.config import (
    AgentConfig,
    Config,
    KeybindsConfig,
    McpLocalConfig,
    McpRemoteConfig,
    PermissionConfig,
    ProviderConfig,
)
from opencode.models.error import (
    APIErrorModel,
    MessageAbortedError,
    MessageOutputLengthError,
    ProviderAuthError,
    UnknownError,
)
from opencode.models.event import (
    Event,
    GlobalEvent,
    # Session events
    SessionStatusEvent,
    SessionIdleEvent,
    SessionCreatedEvent,
    SessionUpdatedEvent,
    SessionDeletedEvent,
    SessionDiffEvent,
    SessionErrorEvent,
    SessionCompactedEvent,
    # Message events
    MessageUpdatedEvent,
    MessageRemovedEvent,
    MessagePartUpdatedEvent,
    MessagePartRemovedEvent,
    # Permission events
    PermissionUpdatedEvent,
    PermissionRepliedEvent,
    # File events
    FileEditedEvent,
    FileWatcherUpdatedEvent,
    # PTY events
    PtyCreatedEvent,
    PtyUpdatedEvent,
    PtyExitedEvent,
    PtyDeletedEvent,
    # Other events
    TodoUpdatedEvent,
    LspUpdatedEvent,
    LspClientDiagnosticsEvent,
    CommandExecutedEvent,
    VcsBranchUpdatedEvent,
    ServerConnectedEvent,
    ServerInstanceDisposedEvent,
    InstallationUpdatedEvent,
    InstallationUpdateAvailableEvent,
    TuiPromptAppendEvent,
    TuiCommandExecuteEvent,
    TuiToastShowEvent,
    parse_event,
)
from opencode.models.file import File, FileContent, FileNode, Symbol
from opencode.models.lsp import LSPStatus
from opencode.models.mcp import MCPStatus, MCPStatusConnected, MCPStatusDisabled, MCPStatusFailed
from opencode.models.message import (
    AssistantMessage,
    Message,
    MessageWithParts,
    UserMessage,
)
from opencode.models.part import (
    # Response parts
    Part,
    TextPart,
    ReasoningPart,
    FilePart,
    ToolPart,
    StepStartPart,
    StepFinishPart,
    SnapshotPart,
    PatchPart,
    AgentPart,
    RetryPart,
    CompactionPart,
    SubtaskPart,
    # Tool states
    ToolState,
    ToolStatePending,
    ToolStateRunning,
    ToolStateCompleted,
    ToolStateError,
    # Input parts
    PartInput,
    TextPartInput,
    FilePartInput,
    AgentPartInput,
    SubtaskPartInput,
    # File sources
    FileSource,
    SymbolSource,
    FilePartSource,
    FilePartSourceText,
)
from opencode.models.project import Project
from opencode.models.provider import Model, Provider, ProviderAuthMethod, ProviderAuthAuthorization
from opencode.models.pty import Pty
from opencode.models.session import (
    Permission,
    Session,
    SessionStatus,
    SessionStatusBusy,
    SessionStatusIdle,
    SessionStatusRetry,
    Todo,
)
from opencode.models.tool import ToolListItem

__all__ = [
    # Base
    "OpenCodeModel",
    "InputModel",
    # Common
    "FileDiff",
    "ModelConfig",
    "Range",
    "Position",
    "Time",
    "TimeWithCompleted",
    # Session
    "Session",
    "SessionStatus",
    "SessionStatusIdle",
    "SessionStatusBusy",
    "SessionStatusRetry",
    "Permission",
    "Todo",
    # Message
    "Message",
    "UserMessage",
    "AssistantMessage",
    "MessageWithParts",
    # Parts
    "Part",
    "TextPart",
    "ReasoningPart",
    "FilePart",
    "ToolPart",
    "StepStartPart",
    "StepFinishPart",
    "SnapshotPart",
    "PatchPart",
    "AgentPart",
    "RetryPart",
    "CompactionPart",
    "SubtaskPart",
    "ToolState",
    "ToolStatePending",
    "ToolStateRunning",
    "ToolStateCompleted",
    "ToolStateError",
    "PartInput",
    "TextPartInput",
    "FilePartInput",
    "AgentPartInput",
    "SubtaskPartInput",
    "FileSource",
    "SymbolSource",
    "FilePartSource",
    "FilePartSourceText",
    # Events
    "Event",
    "GlobalEvent",
    "SessionStatusEvent",
    "SessionIdleEvent",
    "SessionCreatedEvent",
    "SessionUpdatedEvent",
    "SessionDeletedEvent",
    "SessionDiffEvent",
    "SessionErrorEvent",
    "SessionCompactedEvent",
    "MessageUpdatedEvent",
    "MessageRemovedEvent",
    "MessagePartUpdatedEvent",
    "MessagePartRemovedEvent",
    "PermissionUpdatedEvent",
    "PermissionRepliedEvent",
    "FileEditedEvent",
    "FileWatcherUpdatedEvent",
    "PtyCreatedEvent",
    "PtyUpdatedEvent",
    "PtyExitedEvent",
    "PtyDeletedEvent",
    "TodoUpdatedEvent",
    "LspUpdatedEvent",
    "LspClientDiagnosticsEvent",
    "CommandExecutedEvent",
    "VcsBranchUpdatedEvent",
    "ServerConnectedEvent",
    "ServerInstanceDisposedEvent",
    "InstallationUpdatedEvent",
    "InstallationUpdateAvailableEvent",
    "TuiPromptAppendEvent",
    "TuiCommandExecuteEvent",
    "TuiToastShowEvent",
    "parse_event",
    # Provider
    "Provider",
    "Model",
    "ProviderAuthMethod",
    "ProviderAuthAuthorization",
    # Config
    "Config",
    "AgentConfig",
    "ProviderConfig",
    "KeybindsConfig",
    "McpLocalConfig",
    "McpRemoteConfig",
    "PermissionConfig",
    # Project
    "Project",
    # PTY
    "Pty",
    # File
    "File",
    "FileContent",
    "FileNode",
    "Symbol",
    # Tool
    "ToolListItem",
    # MCP/LSP
    "MCPStatus",
    "MCPStatusConnected",
    "MCPStatusDisabled",
    "MCPStatusFailed",
    "LSPStatus",
    # Auth
    "Auth",
    "OAuth",
    "ApiAuth",
    "WellKnownAuth",
    # Agent
    "Agent",
    # Command
    "Command",
    # Error models
    "ProviderAuthError",
    "UnknownError",
    "MessageOutputLengthError",
    "MessageAbortedError",
    "APIErrorModel",
]
