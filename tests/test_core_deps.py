import pytest
from fastapi import Request
from core.deps import get_db
from unittest.mock import MagicMock

class DummyRequest:
    def __init__(self, db):
        self.app = MagicMock()
        self.app.state.db = db

def test_get_db_returns_db():
    dummy_db = MagicMock()
    request = DummyRequest(dummy_db)
    result = get_db(request)
    assert result == dummy_db

