import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from logger_kit import app_logger, RequestLoggingMiddleware
import json

def test_logger_singleton():
    """Test that logger is a singleton"""
    logger1 = app_logger
    logger2 = app_logger
    assert logger1 is logger2

def test_logger_methods():
    """Test all logging methods"""
    # These should not raise any exceptions
    app_logger.debug("Debug message")
    app_logger.info("Info message")
    app_logger.warning("Warning message")
    app_logger.error("Error message")
    app_logger.critical("Critical message")

    # Test dictionary logging
    test_dict = {"key": "value"}
    app_logger.info(test_dict)

def test_middleware():
    """Test the request logging middleware"""
    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)

    @app.get("/test")
    async def test_endpoint():
        return {"message": "test"}

    @app.post("/test")
    async def test_post_endpoint(data: dict):
        return data

    client = TestClient(app)

    # Test GET request
    response = client.get("/test")
    assert response.status_code == 200

    # Test POST request with body
    test_data = {"test": "data"}
    response = client.post(
        "/test",
        json=test_data
    )
    assert response.status_code == 200
    assert response.json() == test_data

@pytest.mark.asyncio
async def test_middleware_exclude_paths():
    """Test middleware path exclusion"""
    app = FastAPI()
    app.add_middleware(
        RequestLoggingMiddleware,
        exclude_paths={"/health"}
    )

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
