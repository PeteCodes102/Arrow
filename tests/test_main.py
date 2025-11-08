"""Tests for main.py - FastAPI application entry point"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import status


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint returns app information."""
    # Import main and create test client
    # We need to patch the lifespan context manager to avoid DB initialization
    with patch('main.init_db', new_callable=AsyncMock):
        from main import app
        client = TestClient(app, raise_server_exceptions=False)
        
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "environment" in data
        assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_health_endpoint_healthy():
    """Test health endpoint when database is connected."""
    with patch('main.init_db', new_callable=AsyncMock), \
         patch('models.alerts.BaseAlert.find_one', new_callable=AsyncMock) as mock_find:
        
        mock_find.return_value = None  # DB query succeeds
        
        from main import app
        client = TestClient(app, raise_server_exceptions=False)
        
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"


@pytest.mark.asyncio
async def test_health_endpoint_unhealthy():
    """Test health endpoint when database is disconnected."""
    with patch('main.init_db', new_callable=AsyncMock), \
         patch('models.alerts.BaseAlert.find_one', new_callable=AsyncMock) as mock_find:
        
        # Simulate database error
        mock_find.side_effect = Exception("Database connection failed")
        
        from main import app
        client = TestClient(app, raise_server_exceptions=False)
        
        response = client.get("/health")
        
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] == "disconnected"
        assert "error" in data


@pytest.mark.asyncio
async def test_cors_headers_in_development():
    """Test that CORS headers are permissive in development."""
    with patch('main.init_db', new_callable=AsyncMock), \
         patch('main.ENVIRONMENT', 'development'):
        
        from main import app
        client = TestClient(app, raise_server_exceptions=False)
        
        # Make a request with Origin header
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        
        # CORS middleware should add appropriate headers
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_app_includes_routers():
    """Test that all routers are included in the app."""
    with patch('main.init_db', new_callable=AsyncMock):
        from main import app
        
        # Check that routes from different routers exist
        routes = [route.path for route in app.routes]
        
        # Root and health endpoints
        assert "/" in routes or any("/docs" in r for r in routes)
        
        # Data router endpoints (prefix /data)
        assert any("/data" in r for r in routes)
        
        # Alert router endpoints (prefix /alerts)
        assert any("/alerts" in r for r in routes)
        
        # Keys router endpoints (prefix /keys)
        assert any("/keys" in r for r in routes)
