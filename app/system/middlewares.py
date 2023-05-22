"""
# TODO : //
create class for all middleware files
create middleware folder and add class to that file
add this md eis to the main file with import
totally target is reduce main file middleware codes and transport that file to the other folders
"""

# import string
# import time
# import random
#
# from fastapi import Request
#
# from main import app
# from utils import CustomHttpException
# from logger.config import settings
# from logger.logger import requests_logger
# from logger.logger_router import LoggerRouteHandler
# from logger.global_request_validator import global_request_validator
# from fastapi.exceptions import RequestValidationError
# from starlette.middleware.cors import CORSMiddleware
# from starlette.responses import JSONResponse
#
# app.router.route_class = LoggerRouteHandler
#
#
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#     requests_logger.info(f"INFO rid={idem} start request path={request.url.path}")
#     start_time = time.time()
#
#     response = await call_next(request)
#
#     process_time = (time.time() - start_time) * 1000
#     formatted_process_time = '{0:.2f}'.format(process_time)
#     requests_logger.info(f"INFO rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
#
#     return response
#
#
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
#
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return await global_request_validator(request, exc)
#
#
# @app.exception_handler(CustomHttpException)
# async def custom_exception_handler(request: Request, exc: CustomHttpException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content=exc.detail,
#     )
