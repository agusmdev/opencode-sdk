"""SDK constants and default values."""

from typing import Final

# Default API configuration
DEFAULT_BASE_URL: Final[str] = "http://127.0.0.1:1122"
DEFAULT_TIMEOUT: Final[float] = 30.0
DEFAULT_STREAMING_TIMEOUT: Final[float] = 300.0  # 5 minutes for long-running streams

# Pagination defaults
DEFAULT_PAGE_SIZE: Final[int] = 50
MAX_PAGE_SIZE: Final[int] = 100

# SSE reconnection settings
SSE_MAX_RETRIES: Final[int] = 5
SSE_INITIAL_DELAY: Final[float] = 1.0
SSE_MAX_DELAY: Final[float] = 30.0
SSE_BACKOFF_FACTOR: Final[float] = 2.0

# HTTP headers
USER_AGENT: Final[str] = "opencode-sdk/0.1.0"

# ID prefixes for validation
SESSION_ID_PREFIX: Final[str] = "ses"
MESSAGE_ID_PREFIX: Final[str] = "msg"
PART_ID_PREFIX: Final[str] = "prt"
PTY_ID_PREFIX: Final[str] = "pty"
