**Note:** This is not the official OpenCode SDK. This is a custom SDK created using OpenCode and Claude Opus 4.5.

# OpenCode Python SDK

Python SDK for the [OpenCode](https://opencode.ai) API.

## Features

- **Fully typed** - Complete type annotations with Pydantic models
- **Async-first** - Built on `httpx` for modern async Python
- **Streaming support** - First-class SSE streaming with automatic reconnection
- **Pagination** - Async iterators for paginated resources
- **Structured logging** - Built-in `structlog` integration

## Installation

```bash
# Using uv (recommended)
uv add opencode-sdk

# Using pip
pip install opencode-sdk
```

## Quick Start

```python
import asyncio
from opencode import OpenCode
from opencode.models import TextPartInput

async def main():
    async with OpenCode() as client:
        # Create a session
        session = await client.sessions.create(title="My Session")
        
        # Send a prompt
        response = await client.sessions.prompt(
            session.id,
            parts=[TextPartInput(type="text", text="Hello, OpenCode!")]
        )
        
        print(f"Response: {response.parts}")

asyncio.run(main())
```

## Streaming Events

```python
async with OpenCode() as client:
    # Subscribe to real-time events
    async for event in client.events.subscribe():
        match event:
            case MessagePartUpdatedEvent(properties=p) if p.delta:
                # Stream text as it arrives
                print(p.delta, end="", flush=True)
            case SessionIdleEvent():
                print("\n--- Session complete ---")
                break
```

## Configuration

```python
from opencode import OpenCode

client = OpenCode(
    base_url="http://127.0.0.1:1122",  # Default
    directory="/path/to/project",       # Optional: default project directory
    timeout=30.0,                        # Request timeout in seconds
)
```

## Resources

The SDK provides access to all OpenCode API resources:

- `client.sessions` - Manage chat sessions
- `client.events` - Subscribe to real-time events (SSE)
- `client.projects` - Project management
- `client.providers` - AI provider configuration
- `client.config` - Configuration management
- `client.files` - File operations
- `client.find` - Search files and symbols
- `client.tools` - Tool management
- `client.mcp` - MCP server integration
- `client.lsp` - LSP server status
- `client.agents` - Agent configuration
- `client.commands` - Custom commands
- `client.pty` - PTY session management
- `client.vcs` - Version control info
- `client.tui` - TUI control (for integrations)

## API Reference

See the [OpenCode documentation](https://opencode.ai/docs) for detailed API reference.

## Development

```bash
# Clone the repository
git clone https://github.com/sst/opencode
cd opencode-sdk

# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Type checking
uv run mypy src

# Linting
uv run ruff check src tests
```

## License

MIT License - see [LICENSE](LICENSE) for details.
