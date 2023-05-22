from utils.response_manager import ResponseManager
from ..schemas.user import MeRequest, MeResponse, ValidationResponse, ValidationRequest


me_RM = ResponseManager(
    request_model=MeRequest,
    response_model=MeResponse,
    pagination=False,
    is_mock=False
)


validation_RM = ResponseManager(
    request_model=ValidationRequest,
    response_model=ValidationResponse,
    pagination=False,
    is_mock=False
)
