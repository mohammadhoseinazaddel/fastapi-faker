from utils import ResponseManager

from ..schemas.otp import SendOtpRequest, SendOtpResponse, CheckOtpRequest, CheckOtpResponse

send_otp_RM = ResponseManager(
    request_model=SendOtpRequest,
    response_model=SendOtpResponse,
    pagination=False,
    is_mock=False,
    is_list=False
)

check_otp_RM = ResponseManager(
    request_model=CheckOtpRequest,
    response_model=CheckOtpResponse,
    pagination=False,
    is_mock=False
)
