from typing import List
from pydantic import BaseModel

from ext_services.wallex.oauth.schemas.wallex_user_balances import WallexUserBalance


class WallexUserInfo(BaseModel):
    wallex_user_id: str
    first_name: str | None
    last_name: str | None
    mobile: str | None
    kyc_level: int | None
    email: str | None
    national_code: str | None
    birth_date: str | None
    balances_details: List[WallexUserBalance] = []

