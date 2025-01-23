"""FastAPI middleware for request and response logging."""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
from .logger import app_logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""

    def __init__(
        self,
        app,
        *,
        exclude_paths=None,
        log_request_body=True,
        log_response_body=True
    ):
        """Initialize the middleware.
        
        Args:
            app: The ASGI application
            exclude_paths: Set of paths to exclude from logging
            log_request_body: Whether to log request body
            log_response_body: Whether to log response body
        """
        super().__init__(app)
        self.exclude_paths = exclude_paths or set()
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body

    async def dispatch(self, request, call_next):
        """Process the request and log details.
        
        Args:
            request: The incoming request
            call_next: The next middleware in chain
        
        Returns:
            The response from the next middleware
        """
        # Skip logging for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Start timing the request
        start_time = time.time()

        # Log request
        await self._log_request(request, request_id)

        try:
            # Process the request and get response
            response = await call_next(request)

            # Log response
            await self._log_response(
                response,
                request_id,
                time.time() - start_time
            )

            return response
        except Exception as e:
            # Log any unhandled exceptions
            app_logger.error(
                {
                    "request_id": request_id,
                    "type": "error",
                    "error": str(e),
                    "path": request.url.path,
                    "method": request.method,
                }
            )
            raise

    async def _log_request(self, request, request_id):
        """Log incoming request details.
        
        Args:
            request: The incoming request
            request_id: Unique identifier for the request
        """
        log_dict = {
            "request_id": request_id,
            "type": "request",
            "path": request.url.path,
            "method": request.method,
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
        }

        if self.log_request_body:
            try:
                body = await request.body()
                if body:
                    log_dict["body"] = body.decode()
            except Exception:
                log_dict["body"] = "Could not read request body"

        app_logger.info(log_dict)

    async def _log_response(self, response, request_id, duration):
        """Log response details.
        
        Args:
            response: The response object
            request_id: Unique identifier for the request
            duration: Time taken to process the request
        """
        log_dict = {
            "request_id": request_id,
            "type": "response",
            "status_code": response.status_code,
            "duration": f"{duration:.4f}s",
            "headers": dict(response.headers),
        }

        if self.log_response_body:
            try:
                body = response.body
                if body:
                    log_dict["body"] = body.decode()
            except Exception:
                log_dict["body"] = "Could not read response body"

        app_logger.info(log_dict)
