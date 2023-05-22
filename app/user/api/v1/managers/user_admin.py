from utils.response_manager import ResponseManager
from ..schemas.user_admin import UserListResponse

user_list_RM = ResponseManager(
    request_model=None,
    response_model=UserListResponse,
    pagination=True,
    is_mock=True,
    is_list=True
)
