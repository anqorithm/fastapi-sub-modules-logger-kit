from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import uuid
from typing import Callable
from .logger import app_logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        *,
        exclude_paths: set[str] = None,
        log_request_body: bool = True,
        log_response_body: bool = True
    ):
        super().__init__(app)
        self.exclude_paths = exclude_paths or set()
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
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

    async def _log_request(self, request: Request, request_id: str):
        """Log incoming request details"""
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

    async def _log_response(
        self,
        response: Response,
        request_id: str,
        duration: float
    ):
        """Log response details"""
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
