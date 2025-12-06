"""OpenCode SDK resources - API resource classes."""

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
from opencode.resources.messages import MessagesResource
from opencode.resources.path import PathResource
from opencode.resources.projects import ProjectsResource
from opencode.resources.providers import ProvidersResource
from opencode.resources.pty import PtyResource
from opencode.resources.sessions import SessionsResource
from opencode.resources.tools import ToolsResource
from opencode.resources.tui import TuiResource
from opencode.resources.vcs import VcsResource

__all__ = [
    "AgentsResource",
    "AuthResource",
    "CommandsResource",
    "ConfigResource",
    "EventsResource",
    "FilesResource",
    "FindResource",
    "FormatterResource",
    "InstanceResource",
    "LspResource",
    "McpResource",
    "MessagesResource",
    "PathResource",
    "ProjectsResource",
    "ProvidersResource",
    "PtyResource",
    "SessionsResource",
    "ToolsResource",
    "TuiResource",
    "VcsResource",
]
