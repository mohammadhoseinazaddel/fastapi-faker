from jinja2.nodes import List
from pydantic import BaseModel


class WallexBalanceStat(BaseModel):
    base_market_name: str
    change_percentage: str | None
    estimated_value: str | None
    last_24_hours_estimated_change: str | None


