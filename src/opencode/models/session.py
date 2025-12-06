"""Session-related Pydantic models."""

from typing import Annotated, Any, Literal

from pydantic import Field

from opencode.models._base import OpenCodeModel
from opencode.models.common import FileDiff


class SessionStatusIdle(OpenCodeModel):
    """Represents an idle session status when no operation is in progress."""

    type: Literal["idle"]
    """The status type identifier."""


class SessionStatusBusy(OpenCodeModel):
    """Represents a busy session status when an operation is in progress."""

    type: Literal["busy"]
    """The status type identifier."""


class SessionStatusRetry(OpenCodeModel):
    """Represents a retry session status when an operation is being retried."""

    type: Literal["retry"]
    """The status type identifier."""

    attempt: int
    """The current retry attempt number."""

    message: str
    """A message describing the retry reason."""

    next: float
    """Unix timestamp for the next retry attempt."""


SessionStatus = Annotated[
    SessionStatusIdle | SessionStatusBusy | SessionStatusRetry,
    Field(discriminator="type"),
]
"""Discriminated union of all possible session status types."""


class SessionSummary(OpenCodeModel):
    """Summary of changes made during a session."""

    additions: int
    """The number of lines added across all files."""

    deletions: int
    """The number of lines deleted across all files."""

    files: int
    """The number of files modified."""

    diffs: list[FileDiff] | None = None
    """Optional list of file diffs showing detailed changes."""


class SessionShare(OpenCodeModel):
    """Information about a shared session."""

    url: str
    """The URL where the session can be accessed."""


class SessionTime(OpenCodeModel):
    """Timestamp information for a session."""

    created: float
    """Unix timestamp when the session was created."""

    updated: float
    """Unix timestamp when the session was last updated."""

    compacting: float | None = None
    """Unix timestamp when the session was last compacted, if applicable."""


class SessionRevert(OpenCodeModel):
    """Information about a session revert operation."""

    message_id: str = Field(alias="messageID")
    """The ID of the message to revert to."""

    part_id: str | None = Field(default=None, alias="partID")
    """The ID of the specific part within the message, if applicable."""

    snapshot: str | None = None
    """The snapshot identifier for the revert point."""

    diff: str | None = None
    """The diff representing the revert changes."""


class Session(OpenCodeModel):
    """
    Represents a session in OpenCode.

    A session encapsulates a conversation with the AI assistant,
    including all messages, file changes, and metadata.
    """

    id: str
    """The unique session identifier (prefixed with 'ses')."""

    project_id: str = Field(alias="projectID")
    """The ID of the project this session belongs to."""

    directory: str
    """The working directory for the session."""

    title: str
    """The title or summary of the session."""

    version: str
    """The version of the session format."""

    time: SessionTime
    """Timestamp information for the session."""

    parent_id: str | None = Field(default=None, alias="parentID")
    """The ID of the parent session, if this is a child session."""

    summary: SessionSummary | None = None
    """Summary of changes made during the session."""

    share: SessionShare | None = None
    """Information about session sharing, if shared."""

    revert: SessionRevert | None = None
    """Information about revert state, if applicable."""


class PermissionTime(OpenCodeModel):
    """Timestamp information for a permission."""

    created: float
    """Unix timestamp when the permission was created."""


class Permission(OpenCodeModel):
    """
    Represents a permission request in a session.

    Permissions are requested when the AI needs to perform
    actions that require user approval, such as file modifications.
    """

    id: str
    """The unique permission identifier."""

    type: str
    """The type of permission being requested."""

    session_id: str = Field(alias="sessionID")
    """The ID of the session this permission belongs to."""

    message_id: str = Field(alias="messageID")
    """The ID of the message that triggered this permission request."""

    title: str
    """A human-readable title describing the permission."""

    metadata: dict[str, Any]
    """Additional metadata about the permission request."""

    time: PermissionTime
    """Timestamp information for the permission."""

    pattern: str | list[str] | None = None
    """Optional pattern(s) for matching affected resources."""

    call_id: str | None = Field(default=None, alias="callID")
    """The ID of the tool call associated with this permission, if applicable."""


class Todo(OpenCodeModel):
    """
    Represents a todo item in a session.

    Todos are used to track tasks and their completion status
    during a session.
    """

    id: str
    """Unique identifier for the todo item."""

    content: str
    """Brief description of the task."""

    status: str
    """Current status of the task: pending, in_progress, completed, cancelled."""

    priority: str
    """Priority level of the task: high, medium, low."""
