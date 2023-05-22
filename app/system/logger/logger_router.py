from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

from system.logger.log import requests_logger


class LoggerRouteHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def route_handler(request: Request) -> Response:
            # Add fastapi context to logs
            ctx = {
                "path": request.url.path,
                "route": self.path,
                "method": request.method,
            }
            requests_logger.append_keys(fastapi=ctx)
            requests_logger.info("Received request")

            return await original_route_handler(request)

        return route_handler
