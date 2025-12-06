"""File-related Pydantic models."""

from typing import Literal

from opencode.models._base import OpenCodeModel
from opencode.models.common import Range


class FileNode(OpenCodeModel):
    """
    Represents a node in a file tree.

    Can be either a file or a directory, with information about
    its path and whether it's ignored by version control.
    """

    name: str
    """The name of the file or directory."""

    path: str
    """The relative path to the file or directory."""

    absolute: str
    """The absolute path to the file or directory."""

    type: Literal["file", "directory"]
    """The type of the node."""

    ignored: bool
    """Whether the node is ignored by version control."""


class FilePatch(OpenCodeModel):
    """
    Represents a patch/diff for a file.

    Contains the hunks that describe the changes made to the file.
    """

    hunks: list[str]
    """The diff hunks describing the changes."""


class FileContent(OpenCodeModel):
    """
    Represents the content of a file.

    Contains the actual file content along with optional diff
    information and encoding details.
    """

    type: Literal["text"]
    """The type of content."""

    content: str
    """The file content."""

    diff: str | None = None
    """The diff representation of changes, if applicable."""

    patch: FilePatch | None = None
    """The patch information, if applicable."""

    encoding: Literal["base64"] | None = None
    """The encoding of the content, if not plain text."""

    mime_type: str | None = None
    """The MIME type of the file content."""


class File(OpenCodeModel):
    """
    Represents a file with change statistics.

    Used to describe files that have been modified, with counts
    of added and removed lines.
    """

    path: str
    """The path to the file."""

    added: int
    """The number of lines added."""

    removed: int
    """The number of lines removed."""

    status: Literal["added", "deleted", "modified"]
    """The status of the file change."""


class SymbolLocation(OpenCodeModel):
    """
    Represents the location of a symbol in a file.

    Contains the URI of the file and the range where the symbol is defined.
    """

    uri: str
    """The URI of the file containing the symbol."""

    range: Range
    """The range within the file where the symbol is located."""


class Symbol(OpenCodeModel):
    """
    Represents a code symbol (e.g., function, class, variable).

    Contains information about the symbol's name, kind, and location
    in the source code.
    """

    name: str
    """The name of the symbol."""

    kind: int
    """The kind of symbol (e.g., function, class, variable). Uses LSP SymbolKind values."""

    location: SymbolLocation
    """The location of the symbol in the source code."""
