from user.api.v1.schemas.login import WallexLoginResponse, LoginBySateResponse, RefrefshTokenResponse, \
    RefrefshTokenRequest
from utils import ResponseManager

refresh_token_RM = ResponseManager(
    request_model=RefrefshTokenRequest,
    response_model=RefrefshTokenResponse,
    pagination=False,
    is_mock=False
)

wallex_login_RM = ResponseManager(
    request_model=None,
    response_model=WallexLoginResponse,
    pagination=False,
    is_mock=False
)

login_by_state_RM = ResponseManager(
    request_model=None,
    response_model=LoginBySateResponse,
    pagination=False,
    is_mock=False
)
