from typing import List
from pydantic import BaseModel
from ext_services.wallex.oauth.schemas.wallex_balance_stat import WallexBalanceStat


class WallexUserBalance(BaseModel):
    symbol: str
    total: float
    freeze: float
    available: float
    stats: List[WallexBalanceStat] = []
