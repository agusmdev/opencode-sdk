"""Tests for session models."""
from __future__ import annotations

import pytest

from opencode.models import (
    Session,
    SessionStatus,
    SessionStatusIdle,
    SessionStatusBusy,
    SessionStatusRetry,
    Todo,
    Permission,
)


class TestSession:
    """Test Session model."""

    def test_parse_session(self):
        """Test parsing session from dict."""
        data = {
            "id": "ses_123",
            "projectID": "proj_456",
            "directory": "/test",
            "title": "Test Session",
            "version": "1.0.0",
            "time": {"created": 1234567890.0, "updated": 1234567890.0},
        }

        session = Session.model_validate(data)

        assert session.id == "ses_123"
        assert session.project_id == "proj_456"
        assert session.directory == "/test"
        assert session.title == "Test Session"
        assert session.time.created == 1234567890.0

    def test_parse_session_with_optional_fields(self):
        """Test parsing session with optional fields."""
        data = {
            "id": "ses_123",
            "projectID": "proj_456",
            "directory": "/test",
            "title": "Test Session",
            "version": "1.0.0",
            "time": {"created": 1234567890.0, "updated": 1234567890.0},
            "parentID": "ses_parent",
            "summary": {
                "additions": 10,
                "deletions": 5,
                "files": 3,
            },
            "share": {"url": "https://share.opencode.ai/xxx"},
        }

        session = Session.model_validate(data)

        assert session.parent_id == "ses_parent"
        assert session.summary is not None
        assert session.summary.additions == 10
        assert session.share is not None
        assert session.share.url == "https://share.opencode.ai/xxx"

    def test_serialize_session(self):
        """Test serializing session to dict."""
        data = {
            "id": "ses_123",
            "projectID": "proj_456",
            "directory": "/test",
            "title": "Test Session",
            "version": "1.0.0",
            "time": {"created": 1234567890.0, "updated": 1234567890.0},
        }

        session = Session.model_validate(data)
        serialized = session.model_dump(by_alias=True)

        assert serialized["projectID"] == "proj_456"


class TestSessionStatus:
    """Test SessionStatus discriminated union."""

    def test_parse_idle_status(self):
        """Test parsing idle status."""
        data = {"type": "idle"}
        
        # This would need TypeAdapter for discriminated union
        status = SessionStatusIdle.model_validate(data)
        assert status.type == "idle"

    def test_parse_busy_status(self):
        """Test parsing busy status."""
        data = {"type": "busy"}
        
        status = SessionStatusBusy.model_validate(data)
        assert status.type == "busy"

    def test_parse_retry_status(self):
        """Test parsing retry status."""
        data = {
            "type": "retry",
            "attempt": 3,
            "message": "Rate limited",
            "next": 1234567890.0,
        }
        
        status = SessionStatusRetry.model_validate(data)
        assert status.type == "retry"
        assert status.attempt == 3
        assert status.message == "Rate limited"


class TestTodo:
    """Test Todo model."""

    def test_parse_todo(self):
        """Test parsing todo."""
        data = {
            "id": "todo_123",
            "content": "Implement feature",
            "status": "in_progress",
            "priority": "high",
        }

        todo = Todo.model_validate(data)

        assert todo.id == "todo_123"
        assert todo.content == "Implement feature"
        assert todo.status == "in_progress"
        assert todo.priority == "high"


class TestPermission:
    """Test Permission model."""

    def test_parse_permission(self):
        """Test parsing permission."""
        data = {
            "id": "perm_123",
            "type": "edit",
            "sessionID": "ses_123",
            "messageID": "msg_456",
            "title": "Edit file",
            "metadata": {"file": "/path/to/file.py"},
            "time": {"created": 1234567890.0},
        }

        perm = Permission.model_validate(data)

        assert perm.id == "perm_123"
        assert perm.type == "edit"
        assert perm.session_id == "ses_123"
