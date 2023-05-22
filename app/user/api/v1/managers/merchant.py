from user.api.v1.schemas.merchant import MerchantInfoResponse, MerchantInfoLoginResponse
from utils.response_manager import ResponseManager

merchant_info_RM = ResponseManager(
    request_model=None,
    response_model=MerchantInfoResponse,
    pagination=False,
    is_mock=False
)

merchant_info_by_login_RM = ResponseManager(
    request_model=None,
    response_model=MerchantInfoLoginResponse,
    pagination=False,
    is_mock=False
)

