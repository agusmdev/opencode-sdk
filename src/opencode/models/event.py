"""Pydantic models for SSE (Server-Sent Events) event types."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Annotated, Any, Literal, Union

from pydantic import Field

from opencode.models._base import OpenCodeModel
from opencode.models.common import FileDiff
from opencode.models.error import MessageError
from opencode.models.session import Permission, Session, SessionStatus, Todo

if TYPE_CHECKING:
    from opencode.models.message import Message
    from opencode.models.part import Part
    from opencode.models.pty import Pty


# =============================================================================
# Session Events
# =============================================================================


class SessionStatusEventProperties(OpenCodeModel):
    """Properties for session status change events."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session whose status changed."""

    status: SessionStatus
    """The new status of the session."""


class SessionStatusEvent(OpenCodeModel):
    """Event emitted when a session's status changes."""

    type: Literal["session.status"] = "session.status"
    """Event type discriminator."""

    properties: SessionStatusEventProperties
    """Event properties."""


class SessionIdleEventProperties(OpenCodeModel):
    """Properties for session idle events."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session that became idle."""


class SessionIdleEvent(OpenCodeModel):
    """Event emitted when a session becomes idle."""

    type: Literal["session.idle"] = "session.idle"
    """Event type discriminator."""

    properties: SessionIdleEventProperties
    """Event properties."""


class SessionCreatedEventProperties(OpenCodeModel):
    """Properties for session created events."""

    info: Session
    """The newly created session information."""


class SessionCreatedEvent(OpenCodeModel):
    """Event emitted when a new session is created."""

    type: Literal["session.created"] = "session.created"
    """Event type discriminator."""

    properties: SessionCreatedEventProperties
    """Event properties."""


class SessionUpdatedEventProperties(OpenCodeModel):
    """Properties for session updated events."""

    info: Session
    """The updated session information."""


class SessionUpdatedEvent(OpenCodeModel):
    """Event emitted when a session is updated."""

    type: Literal["session.updated"] = "session.updated"
    """Event type discriminator."""

    properties: SessionUpdatedEventProperties
    """Event properties."""


class SessionDeletedEventProperties(OpenCodeModel):
    """Properties for session deleted events."""

    info: Session
    """The deleted session information."""


class SessionDeletedEvent(OpenCodeModel):
    """Event emitted when a session is deleted."""

    type: Literal["session.deleted"] = "session.deleted"
    """Event type discriminator."""

    properties: SessionDeletedEventProperties
    """Event properties."""


class SessionDiffEventProperties(OpenCodeModel):
    """Properties for session diff events."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session with file changes."""

    diff: list[FileDiff]
    """List of file diffs representing the changes."""


class SessionDiffEvent(OpenCodeModel):
    """Event emitted when file changes occur in a session."""

    type: Literal["session.diff"] = "session.diff"
    """Event type discriminator."""

    properties: SessionDiffEventProperties
    """Event properties."""


class SessionErrorEventProperties(OpenCodeModel):
    """Properties for session error events."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session where the error occurred."""

    error: MessageError | None = None
    """The error that occurred, if any."""


class SessionErrorEvent(OpenCodeModel):
    """Event emitted when an error occurs in a session."""

    type: Literal["session.error"] = "session.error"
    """Event type discriminator."""

    properties: SessionErrorEventProperties
    """Event properties."""


class SessionCompactedEventProperties(OpenCodeModel):
    """Properties for session compacted events."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session that was compacted."""


class SessionCompactedEvent(OpenCodeModel):
    """Event emitted when a session is compacted."""

    type: Literal["session.compacted"] = "session.compacted"
    """Event type discriminator."""

    properties: SessionCompactedEventProperties
    """Event properties."""


# =============================================================================
# Message Events
# =============================================================================


class MessageUpdatedEventProperties(OpenCodeModel):
    """Properties for message updated events."""

    info: Any = Field(...)
    """The updated message information."""
    # Note: Type is 'Any' to avoid circular imports. At runtime, this is a Message.


class MessageUpdatedEvent(OpenCodeModel):
    """Event emitted when a message is updated."""

    type: Literal["message.updated"] = "message.updated"
    """Event type discriminator."""

    properties: MessageUpdatedEventProperties
    """Event properties."""


class MessageRemovedEventProperties(OpenCodeModel):
    """Properties for message removed events."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session containing the message."""

    message_id: str = Field(alias="messageID")
    """The ID of the removed message."""


class MessageRemovedEvent(OpenCodeModel):
    """Event emitted when a message is removed."""

    type: Literal["message.removed"] = "message.removed"
    """Event type discriminator."""

    properties: MessageRemovedEventProperties
    """Event properties."""


class MessagePartUpdatedEventProperties(OpenCodeModel):
    """Properties for message part updated events."""

    part: Any = Field(...)
    """The updated message part."""
    # Note: Type is 'Any' to avoid circular imports. At runtime, this is a Part.

    delta: str | None = None
    """Optional incremental text change for streaming updates."""


class MessagePartUpdatedEvent(OpenCodeModel):
    """Event emitted when a message part is updated."""

    type: Literal["message.part.updated"] = "message.part.updated"
    """Event type discriminator."""

    properties: MessagePartUpdatedEventProperties
    """Event properties."""


class MessagePartRemovedEventProperties(OpenCodeModel):
    """Properties for message part removed events."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session containing the message."""

    message_id: str = Field(alias="messageID")
    """The ID of the message containing the part."""

    part_id: str = Field(alias="partID")
    """The ID of the removed part."""


class MessagePartRemovedEvent(OpenCodeModel):
    """Event emitted when a message part is removed."""

    type: Literal["message.part.removed"] = "message.part.removed"
    """Event type discriminator."""

    properties: MessagePartRemovedEventProperties
    """Event properties."""


# =============================================================================
# Permission Events
# =============================================================================


class PermissionUpdatedEvent(OpenCodeModel):
    """Event emitted when a permission is updated."""

    type: Literal["permission.updated"] = "permission.updated"
    """Event type discriminator."""

    properties: Permission
    """The updated permission."""


class PermissionRepliedEventProperties(OpenCodeModel):
    """Properties for permission replied events."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session containing the permission."""

    permission_id: str = Field(alias="permissionID")
    """The ID of the permission that was replied to."""

    response: bool
    """The user's response to the permission request (True=approved, False=denied)."""


class PermissionRepliedEvent(OpenCodeModel):
    """Event emitted when a user responds to a permission request."""

    type: Literal["permission.replied"] = "permission.replied"
    """Event type discriminator."""

    properties: PermissionRepliedEventProperties
    """Event properties."""


# =============================================================================
# File Events
# =============================================================================


class FileEditedEventProperties(OpenCodeModel):
    """Properties for file edited events."""

    file: str
    """The path to the edited file."""


class FileEditedEvent(OpenCodeModel):
    """Event emitted when a file is edited."""

    type: Literal["file.edited"] = "file.edited"
    """Event type discriminator."""

    properties: FileEditedEventProperties
    """Event properties."""


FileWatcherEventType = Literal["add", "change", "unlink"]
"""The type of file system event: add, change, or unlink (delete)."""


class FileWatcherUpdatedEventProperties(OpenCodeModel):
    """Properties for file watcher update events."""

    file: str
    """The path to the affected file."""

    event: FileWatcherEventType
    """The type of file system event."""


class FileWatcherUpdatedEvent(OpenCodeModel):
    """Event emitted when the file watcher detects a file system change."""

    type: Literal["file.watcher.updated"] = "file.watcher.updated"
    """Event type discriminator."""

    properties: FileWatcherUpdatedEventProperties
    """Event properties."""


# =============================================================================
# PTY Events
# =============================================================================


class PtyCreatedEventProperties(OpenCodeModel):
    """Properties for PTY created events."""

    info: Any = Field(...)
    """The created PTY information."""
    # Note: Type is 'Any' to avoid circular imports. At runtime, this is a Pty.


class PtyCreatedEvent(OpenCodeModel):
    """Event emitted when a new PTY (pseudo-terminal) is created."""

    type: Literal["pty.created"] = "pty.created"
    """Event type discriminator."""

    properties: PtyCreatedEventProperties
    """Event properties."""


class PtyUpdatedEventProperties(OpenCodeModel):
    """Properties for PTY updated events."""

    info: Any = Field(...)
    """The updated PTY information."""
    # Note: Type is 'Any' to avoid circular imports. At runtime, this is a Pty.


class PtyUpdatedEvent(OpenCodeModel):
    """Event emitted when a PTY is updated."""

    type: Literal["pty.updated"] = "pty.updated"
    """Event type discriminator."""

    properties: PtyUpdatedEventProperties
    """Event properties."""


class PtyExitedEventProperties(OpenCodeModel):
    """Properties for PTY exited events."""

    id: str
    """The ID of the exited PTY."""

    exit_code: int = Field(alias="exitCode")
    """The exit code of the PTY process."""


class PtyExitedEvent(OpenCodeModel):
    """Event emitted when a PTY process exits."""

    type: Literal["pty.exited"] = "pty.exited"
    """Event type discriminator."""

    properties: PtyExitedEventProperties
    """Event properties."""


class PtyDeletedEventProperties(OpenCodeModel):
    """Properties for PTY deleted events."""

    id: str
    """The ID of the deleted PTY."""


class PtyDeletedEvent(OpenCodeModel):
    """Event emitted when a PTY is deleted."""

    type: Literal["pty.deleted"] = "pty.deleted"
    """Event type discriminator."""

    properties: PtyDeletedEventProperties
    """Event properties."""


# =============================================================================
# Todo Events
# =============================================================================


class TodoUpdatedEventProperties(OpenCodeModel):
    """Properties for todo updated events."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session containing the todos."""

    todos: list[Todo]
    """The updated list of todos."""


class TodoUpdatedEvent(OpenCodeModel):
    """Event emitted when todos are updated in a session."""

    type: Literal["todo.updated"] = "todo.updated"
    """Event type discriminator."""

    properties: TodoUpdatedEventProperties
    """Event properties."""


# =============================================================================
# LSP Events
# =============================================================================


class LspUpdatedEventProperties(OpenCodeModel):
    """Properties for LSP updated events."""

    pass


class LspUpdatedEvent(OpenCodeModel):
    """Event emitted when the LSP (Language Server Protocol) state is updated."""

    type: Literal["lsp.updated"] = "lsp.updated"
    """Event type discriminator."""

    properties: LspUpdatedEventProperties
    """Event properties."""


class LspClientDiagnosticsEventProperties(OpenCodeModel):
    """Properties for LSP client diagnostics events."""

    server_id: str = Field(alias="serverID")
    """The ID of the LSP server."""

    path: str
    """The path to the file with diagnostics."""


class LspClientDiagnosticsEvent(OpenCodeModel):
    """Event emitted when LSP diagnostics are received for a file."""

    type: Literal["lsp.client.diagnostics"] = "lsp.client.diagnostics"
    """Event type discriminator."""

    properties: LspClientDiagnosticsEventProperties
    """Event properties."""


# =============================================================================
# Command Events
# =============================================================================


class CommandExecutedEventProperties(OpenCodeModel):
    """Properties for command executed events."""

    name: str
    """The name of the executed command."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session where the command was executed."""

    arguments: dict[str, Any] | None = None
    """Optional arguments passed to the command."""

    message_id: str | None = Field(default=None, alias="messageID")
    """Optional ID of the message associated with the command."""


class CommandExecutedEvent(OpenCodeModel):
    """Event emitted when a command is executed."""

    type: Literal["command.executed"] = "command.executed"
    """Event type discriminator."""

    properties: CommandExecutedEventProperties
    """Event properties."""


# =============================================================================
# VCS Events
# =============================================================================


class VcsBranchUpdatedEventProperties(OpenCodeModel):
    """Properties for VCS branch updated events."""

    branch: str | None = None
    """The name of the current branch, or None if not on a branch."""


class VcsBranchUpdatedEvent(OpenCodeModel):
    """Event emitted when the VCS (version control system) branch changes."""

    type: Literal["vcs.branch.updated"] = "vcs.branch.updated"
    """Event type discriminator."""

    properties: VcsBranchUpdatedEventProperties
    """Event properties."""


# =============================================================================
# Server Events
# =============================================================================


class ServerConnectedEventProperties(OpenCodeModel):
    """Properties for server connected events."""

    pass


class ServerConnectedEvent(OpenCodeModel):
    """Event emitted when a connection to the server is established."""

    type: Literal["server.connected"] = "server.connected"
    """Event type discriminator."""

    properties: ServerConnectedEventProperties
    """Event properties."""


class ServerInstanceDisposedEventProperties(OpenCodeModel):
    """Properties for server instance disposed events."""

    directory: str
    """The directory of the disposed server instance."""


class ServerInstanceDisposedEvent(OpenCodeModel):
    """Event emitted when a server instance is disposed."""

    type: Literal["server.instance.disposed"] = "server.instance.disposed"
    """Event type discriminator."""

    properties: ServerInstanceDisposedEventProperties
    """Event properties."""


# =============================================================================
# Installation Events
# =============================================================================


class InstallationUpdatedEventProperties(OpenCodeModel):
    """Properties for installation updated events."""

    version: str
    """The current installation version."""


class InstallationUpdatedEvent(OpenCodeModel):
    """Event emitted when the installation is updated."""

    type: Literal["installation.updated"] = "installation.updated"
    """Event type discriminator."""

    properties: InstallationUpdatedEventProperties
    """Event properties."""


class InstallationUpdateAvailableEventProperties(OpenCodeModel):
    """Properties for installation update available events."""

    version: str
    """The version of the available update."""


class InstallationUpdateAvailableEvent(OpenCodeModel):
    """Event emitted when an installation update is available."""

    type: Literal["installation.update-available"] = "installation.update-available"
    """Event type discriminator."""

    properties: InstallationUpdateAvailableEventProperties
    """Event properties."""


# =============================================================================
# TUI Events
# =============================================================================


class TuiPromptAppendEventProperties(OpenCodeModel):
    """Properties for TUI prompt append events."""

    text: str
    """The text to append to the prompt."""


class TuiPromptAppendEvent(OpenCodeModel):
    """Event emitted to append text to the TUI prompt."""

    type: Literal["tui.prompt.append"] = "tui.prompt.append"
    """Event type discriminator."""

    properties: TuiPromptAppendEventProperties
    """Event properties."""


class TuiCommandExecuteEventProperties(OpenCodeModel):
    """Properties for TUI command execute events."""

    command: str
    """The command to execute in the TUI."""


class TuiCommandExecuteEvent(OpenCodeModel):
    """Event emitted to execute a command in the TUI."""

    type: Literal["tui.command.execute"] = "tui.command.execute"
    """Event type discriminator."""

    properties: TuiCommandExecuteEventProperties
    """Event properties."""


TuiToastVariant = Literal["info", "success", "warning", "error"]
"""Variant type for TUI toast notifications."""


class TuiToastShowEventProperties(OpenCodeModel):
    """Properties for TUI toast show events."""

    message: str
    """The message to display in the toast."""

    variant: TuiToastVariant
    """The visual variant of the toast (info, success, warning, error)."""

    title: str | None = None
    """Optional title for the toast."""

    duration: int | None = None
    """Optional duration in milliseconds to show the toast."""


class TuiToastShowEvent(OpenCodeModel):
    """Event emitted to show a toast notification in the TUI."""

    type: Literal["tui.toast.show"] = "tui.toast.show"
    """Event type discriminator."""

    properties: TuiToastShowEventProperties
    """Event properties."""


# =============================================================================
# Event Union Type
# =============================================================================


Event = Annotated[
    Union[
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
        # Todo events
        TodoUpdatedEvent,
        # LSP events
        LspUpdatedEvent,
        LspClientDiagnosticsEvent,
        # Command events
        CommandExecutedEvent,
        # VCS events
        VcsBranchUpdatedEvent,
        # Server events
        ServerConnectedEvent,
        ServerInstanceDisposedEvent,
        # Installation events
        InstallationUpdatedEvent,
        InstallationUpdateAvailableEvent,
        # TUI events
        TuiPromptAppendEvent,
        TuiCommandExecuteEvent,
        TuiToastShowEvent,
    ],
    Field(discriminator="type"),
]
"""
Discriminated union of all SSE event types.

Events are discriminated by their 'type' field, which contains a string
like 'session.status', 'message.updated', etc.
"""


# =============================================================================
# Global Event Wrapper
# =============================================================================


class GlobalEvent(OpenCodeModel):
    """
    A wrapper for events that includes the directory context.

    Global events are used when broadcasting events across different
    project directories or when the event source directory is relevant.
    """

    directory: str
    """The directory associated with this event."""

    payload: Event
    """The actual event payload."""


# =============================================================================
# Event Parsing Utilities
# =============================================================================


def parse_event(data: str | dict[str, Any]) -> Event:
    """
    Parse raw event data into a typed Event object.

    This function handles both string (JSON) and dict inputs, automatically
    determining the correct event type based on the 'type' field discriminator.

    Args:
        data: Either a JSON string or a dictionary containing event data.
              Must have a 'type' field that matches one of the known event types.

    Returns:
        A typed Event object corresponding to the event type.

    Raises:
        ValueError: If the data cannot be parsed as JSON (when string input).
        ValidationError: If the data doesn't match any known event type or
                        fails validation.

    Examples:
        >>> event = parse_event('{"type": "session.idle", "properties": {"sessionID": "ses_123"}}')
        >>> isinstance(event, SessionIdleEvent)
        True

        >>> event = parse_event({"type": "session.status", "properties": {"sessionID": "ses_123", "status": {"type": "idle"}}})
        >>> isinstance(event, SessionStatusEvent)
        True
    """
    from pydantic import TypeAdapter

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}") from e

    adapter = TypeAdapter(Event)
    return adapter.validate_python(data)
