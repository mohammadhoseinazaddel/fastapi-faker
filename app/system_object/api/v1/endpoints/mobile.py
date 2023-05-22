from fastapi import APIRouter

from utils import ResponseManager
from ..schemas.mobile import *

router = APIRouter()

mobile_version_RM = ResponseManager(
    request_model=None,
    response_model=MobileVersionsResponse,
    pagination=False,
    is_mock=True
)


@router.get(
    "/versions",
    response_model=mobile_version_RM.response_model(),
    response_description="Get mobile versions"
)
def mobile_versions():
    try:
        mobile_version_RM.status_code(200)
        return mobile_version_RM.response()
    except Exception as e:
        return mobile_version_RM.exception(e)
