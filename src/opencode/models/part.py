"""Pydantic models for message parts."""

from typing import Annotated, Literal

from pydantic import Field

from opencode.models._base import InputModel, OpenCodeModel
from opencode.models.common import Range
from opencode.models.error import APIErrorModel


# =============================================================================
# Time Models for Parts
# =============================================================================


class PartTime(OpenCodeModel):
    """Time information for a part with required start and optional end."""

    start: float
    """Unix timestamp when the part started."""

    end: float | None = None
    """Unix timestamp when the part ended, if completed."""


class PartTimeRequired(OpenCodeModel):
    """Time information for a part with both start and end required."""

    start: float
    """Unix timestamp when the part started."""

    end: float
    """Unix timestamp when the part ended."""


class ToolTimeCompleted(OpenCodeModel):
    """Time information for a completed tool execution."""

    start: float
    """Unix timestamp when tool execution started."""

    end: float
    """Unix timestamp when tool execution ended."""

    compacted: float | None = None
    """Unix timestamp when the tool output was compacted, if applicable."""


class ToolTimeRunning(OpenCodeModel):
    """Time information for a running tool execution."""

    start: float
    """Unix timestamp when tool execution started."""


class RetryTime(OpenCodeModel):
    """Time information for a retry attempt."""

    created: float
    """Unix timestamp when the retry was created."""


# =============================================================================
# File Part Source Models
# =============================================================================


class FilePartSourceText(OpenCodeModel):
    """Text source information for a file part."""

    value: str
    """The text content."""

    start: int
    """Start position in the source."""

    end: int
    """End position in the source."""


class FileSource(OpenCodeModel):
    """Source information for a file reference."""

    type: Literal["file"] = "file"
    """Discriminator for file source type."""

    text: FilePartSourceText
    """The text source information."""

    path: str
    """Path to the file."""


class SymbolSource(OpenCodeModel):
    """Source information for a symbol reference within a file."""

    type: Literal["symbol"] = "symbol"
    """Discriminator for symbol source type."""

    text: FilePartSourceText
    """The text source information."""

    path: str
    """Path to the file containing the symbol."""

    range: Range
    """Range of the symbol in the file."""

    name: str
    """Name of the symbol."""

    kind: int
    """Kind of the symbol (e.g., function, class, variable)."""


FilePartSource = Annotated[
    FileSource | SymbolSource,
    Field(discriminator="type"),
]
"""Union type for file part sources."""


# =============================================================================
# Tool State Models
# =============================================================================


class ToolStatePending(OpenCodeModel):
    """State for a tool that is pending execution."""

    status: Literal["pending"] = "pending"
    """Discriminator for pending state."""

    input: dict
    """Input parameters for the tool."""

    raw: str
    """Raw input string."""


class ToolStateRunning(OpenCodeModel):
    """State for a tool that is currently running."""

    status: Literal["running"] = "running"
    """Discriminator for running state."""

    input: dict
    """Input parameters for the tool."""

    time: ToolTimeRunning
    """Timing information for the running tool."""

    title: str | None = None
    """Optional title for the tool execution."""

    metadata: dict | None = None
    """Optional metadata about the tool execution."""


class ToolStateCompleted(OpenCodeModel):
    """State for a tool that has completed execution."""

    status: Literal["completed"] = "completed"
    """Discriminator for completed state."""

    input: dict
    """Input parameters for the tool."""

    output: str
    """Output from the tool execution."""

    title: str
    """Title of the tool execution."""

    metadata: dict
    """Metadata about the tool execution."""

    time: ToolTimeCompleted
    """Timing information for the completed tool."""

    attachments: list["FilePart"] | None = None
    """Optional file attachments from the tool."""


class ToolStateError(OpenCodeModel):
    """State for a tool that encountered an error."""

    status: Literal["error"] = "error"
    """Discriminator for error state."""

    input: dict
    """Input parameters for the tool."""

    error: str
    """Error message from the tool execution."""

    time: PartTimeRequired
    """Timing information for the failed tool."""

    metadata: dict | None = None
    """Optional metadata about the error."""


ToolState = Annotated[
    ToolStatePending | ToolStateRunning | ToolStateCompleted | ToolStateError,
    Field(discriminator="status"),
]
"""Union type for tool states."""


# =============================================================================
# Token Models for Step Finish
# =============================================================================


class CacheTokens(OpenCodeModel):
    """Token counts for cache operations."""

    read: int
    """Number of tokens read from cache."""

    write: int
    """Number of tokens written to cache."""


class StepTokens(OpenCodeModel):
    """Token usage information for a step."""

    input: int
    """Number of input tokens used."""

    output: int
    """Number of output tokens generated."""

    reasoning: int
    """Number of reasoning tokens used."""

    cache: CacheTokens
    """Cache token information."""


# =============================================================================
# Agent Source Model
# =============================================================================


class AgentSource(OpenCodeModel):
    """Source information for an agent reference."""

    value: str
    """The source value."""

    start: int
    """Start position in the source."""

    end: int
    """End position in the source."""


# =============================================================================
# Part Models
# =============================================================================


class TextPart(OpenCodeModel):
    """A text content part of a message."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["text"] = "text"
    """Discriminator for text part type."""

    text: str
    """The text content."""

    synthetic: bool | None = None
    """Whether this text was synthetically generated."""

    ignored: bool | None = None
    """Whether this text should be ignored."""

    time: PartTime | None = None
    """Timing information for this part."""

    metadata: dict | None = None
    """Optional metadata for this part."""


class ReasoningPart(OpenCodeModel):
    """A reasoning content part of a message, representing model thinking."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["reasoning"] = "reasoning"
    """Discriminator for reasoning part type."""

    text: str
    """The reasoning text content."""

    time: PartTime
    """Timing information for this part."""

    metadata: dict | None = None
    """Optional metadata for this part."""


class FilePart(OpenCodeModel):
    """A file attachment part of a message."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["file"] = "file"
    """Discriminator for file part type."""

    mime: str
    """MIME type of the file."""

    url: str
    """URL to access the file."""

    filename: str | None = None
    """Optional filename."""

    source: FilePartSource | None = None
    """Optional source information for the file."""


class ToolPart(OpenCodeModel):
    """A tool invocation part of a message."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["tool"] = "tool"
    """Discriminator for tool part type."""

    call_id: str = Field(alias="callID")
    """Unique identifier for this tool call."""

    tool: str
    """Name of the tool being invoked."""

    state: ToolState
    """Current state of the tool execution."""

    metadata: dict | None = None
    """Optional metadata for this part."""


class StepStartPart(OpenCodeModel):
    """Marks the start of a processing step."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["step-start"] = "step-start"
    """Discriminator for step start part type."""

    snapshot: str | None = None
    """Optional snapshot identifier."""


class StepFinishPart(OpenCodeModel):
    """Marks the completion of a processing step with usage statistics."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["step-finish"] = "step-finish"
    """Discriminator for step finish part type."""

    reason: str
    """Reason for step completion."""

    cost: float
    """Cost of this step in credits."""

    tokens: StepTokens
    """Token usage for this step."""

    snapshot: str | None = None
    """Optional snapshot identifier."""


class SnapshotPart(OpenCodeModel):
    """A snapshot part capturing state at a point in time."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["snapshot"] = "snapshot"
    """Discriminator for snapshot part type."""

    snapshot: str
    """The snapshot data."""


class PatchPart(OpenCodeModel):
    """A patch part representing file changes."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["patch"] = "patch"
    """Discriminator for patch part type."""

    hash: str
    """Hash identifying this patch."""

    files: list[str]
    """List of files affected by this patch."""


class AgentPart(OpenCodeModel):
    """An agent invocation part of a message."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["agent"] = "agent"
    """Discriminator for agent part type."""

    name: str
    """Name of the agent being invoked."""

    source: AgentSource | None = None
    """Optional source information for the agent reference."""


class RetryPart(OpenCodeModel):
    """A retry attempt part of a message."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["retry"] = "retry"
    """Discriminator for retry part type."""

    attempt: int
    """The retry attempt number."""

    error: APIErrorModel
    """The error that triggered the retry."""

    time: RetryTime
    """Timing information for this retry."""


class CompactionPart(OpenCodeModel):
    """A compaction event part, indicating message history was compacted."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["compaction"] = "compaction"
    """Discriminator for compaction part type."""

    auto: bool
    """Whether this compaction was automatic."""


class SubtaskPart(OpenCodeModel):
    """A subtask part representing a delegated task."""

    id: str
    """Unique identifier for this part."""

    session_id: str = Field(alias="sessionID")
    """ID of the session this part belongs to."""

    message_id: str = Field(alias="messageID")
    """ID of the message this part belongs to."""

    type: Literal["subtask"] = "subtask"
    """Discriminator for subtask part type."""

    prompt: str
    """The prompt for the subtask."""

    description: str
    """Description of the subtask."""

    agent: str
    """Name of the agent handling the subtask."""


# =============================================================================
# Part Union Type
# =============================================================================


Part = Annotated[
    TextPart
    | ReasoningPart
    | FilePart
    | ToolPart
    | StepStartPart
    | StepFinishPart
    | SnapshotPart
    | PatchPart
    | AgentPart
    | RetryPart
    | CompactionPart
    | SubtaskPart,
    Field(discriminator="type"),
]
"""Union type representing any message part."""


# =============================================================================
# Input Models
# =============================================================================


class TextPartInput(InputModel):
    """Input model for creating a text part."""

    type: Literal["text"] = "text"
    """Part type discriminator."""

    text: str
    """The text content."""

    synthetic: bool | None = None
    """Whether this text is synthetically generated."""

    ignored: bool | None = None
    """Whether this text should be ignored."""


class FilePartInput(InputModel):
    """Input model for creating a file part."""

    type: Literal["file"] = "file"
    """Part type discriminator."""

    mime: str
    """MIME type of the file."""

    url: str
    """URL to access the file."""

    filename: str | None = None
    """Optional filename."""


class AgentPartInput(InputModel):
    """Input model for creating an agent part."""

    type: Literal["agent"] = "agent"
    """Part type discriminator."""

    name: str
    """Name of the agent to invoke."""


class SubtaskPartInput(InputModel):
    """Input model for creating a subtask part."""

    type: Literal["subtask"] = "subtask"
    """Part type discriminator."""

    prompt: str
    """The prompt for the subtask."""

    description: str
    """Description of the subtask."""

    agent: str
    """Name of the agent to handle the subtask."""


PartInput = TextPartInput | FilePartInput | AgentPartInput | SubtaskPartInput
"""Union type for part input models."""


# Update forward references for ToolStateCompleted
ToolStateCompleted.model_rebuild()
