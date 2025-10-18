from core.constants import Settings
import os

def test_settings_env(monkeypatch):
    monkeypatch.setenv('MONGO_DB_CONNECTION_STRING', 'mongodb://localhost')
    monkeypatch.setenv('MONGO_DB_NAME', 'testdb')
    settings = Settings()
    assert settings.MONGO_DB_CONNECTION_STRING == 'mongodb://localhost'
    assert settings.MONGO_DB_NAME == 'testdb'

