import datetime
import logging
import random
import string
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from credit import credit_router
from ext_services.jibit.api.api import jibit_router
from ext_services.jibit.payment_gateway.token import jibit_pay_gw_get_token
from ext_services.jibit.transferor.token import jibit_transferor_get_token
from ext_services.sms_ir.sms_ir_interface import sms_ir_agent
from finance.api.api import finance_router
from notification.api.api import notification_router
from order import order_router
from system.config import settings
from system.logger.log import requests_logger
from system_object import SystemObjectsService, system_objects_router
from user import user_router
from user_assets import user_assets_router
from utils.custom_http_exception import CustomHttpException
from utils.global_request_validator import global_422_response_model, global_request_validator

app = FastAPI(title=settings.APP_NAME)

# app.router.route_class = LoggerRouteHandler
wallpay_routes = [
    user_router,
    credit_router,
    order_router,
    finance_router,
    notification_router,
    user_assets_router,
    system_objects_router,
    jibit_router
]


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    requests_logger.info("INFO" + f"rid={idem}" + f"start request path={request.url.path}")

    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    requests_logger.info(
        f"INFO rid={idem}"
        + f"completed_in={formatted_process_time}ms "
        + f"status_code={response.status_code}"
    )

    return response


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await global_request_validator(request, exc)


for route in wallpay_routes:
    app.include_router(
        route,
        prefix="/api",
        responses={
            422: global_422_response_model,
            # 401: global_422_response_model,
            404: {"description": "Not found"},
        },
    )


@app.get("/")
async def root():
    return {
        "APP_NAME": settings.APP_NAME,
        "WALLPAY_BASE_URL": settings.WALLPAY_BASE_URL,
        "FRONT_BASE_URL": settings.FRONT_BASE_URL,
        "SERVICE_STATUS": "Running",
        "TIME_ZONE": settings.APP_TIME_ZONE,
        "SERVER_TIME": datetime.datetime.now(),
    }


# app.mount("/statics", StaticFiles(directory="system/statics"), name="statics")


@app.on_event("startup")
async def startup_event() -> None:  # type: ignore
    time.tzset()
    try:
        from ext_services.jibit.jibit_service import JibitService
        jibit_sr = JibitService()

        system_object_sr = SystemObjectsService()
        system_object_sr.coin.update_coin_price()
        jibit_sr.identity_validate.jibit_get_token()  # توکن سرویس استعلام ثبت احوال و شاهکار
        jibit_pay_gw_get_token()  # توکن درگاه پرداخت
        jibit_transferor_get_token()
        sms_ir_agent.get_token()

        # boton_sr = BotonService()
        # boton_sr.run_worker()

    except Exception as e:
        print(e)


@app.on_event("shutdown")
async def shutdown_event() -> None:  # type: ignore
    logging.info("Wallpay Services Application Shutdown")

# @app.exception_handler(CustomHttpException)
# async def custom_exception_handler(request: Request, exc: CustomHttpException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content=exc.detail,
#     )
