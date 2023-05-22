from utils.response_manager import ResponseManager
from ..schemas.wallet import \
    DepositAddressRequest, DepositAddressResponse, \
    VerifyAddressRequest, VerifyAddressResponse, \
    UserAssetEstimateResponse, UserAssetListResponse, \
    WithdrawRequest, WithdrawResponse

user_asset_estimate_RM = ResponseManager(
    request_model=None,
    response_model=UserAssetEstimateResponse,
    pagination=False,
    is_mock=False
)

user_asset_list_RM = ResponseManager(
    request_model=None,
    response_model=UserAssetListResponse,
    pagination=False,
    is_mock=False
)

deposit_address_RM = ResponseManager(
    request_model=DepositAddressRequest,
    response_model=DepositAddressResponse,
    pagination=False,
    is_mock=False
)

verify_address_RM = ResponseManager(
    request_model=VerifyAddressRequest,
    response_model=VerifyAddressResponse,
    pagination=False,
    is_mock=False
)

withdraw_RM = ResponseManager(
    request_model=WithdrawRequest,
    response_model=WithdrawResponse,
    pagination=False,
    is_mock=False
)
