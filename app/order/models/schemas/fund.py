from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class FundCreateSchema(BaseModel):
    order_id: int
    order_amount: int
    user_id: int
    used_non_free_credit: int
    used_free_credit: int


class FundUpdateSchema(BaseModel):
    # credit info
    used_free_credit: int | None
    used_non_free_credit: int | None
    repaid_free_credit: int | None
    repaid_non_free_credit: int | None
    used_asset_json: dict | None
    extra_money_to_pay: int | None

    # wallex info
    need_collateral: bool | None
    need_wallex_asset: bool | None
    wallex_block_request_id: str | None

    # pay info
    payment_amount: int | None
    payment_id: int | None
    paid_at: datetime | None
    completely_repaid_at: datetime | None

    fill_percentage: int | None
    deleted_at: datetime | None


class FundGetMultiSchema(GetMultiBaseModel):
    need_wallex_asset: bool | None
    wallex_block_request_id: str | None

    # pay info
    payment_id: int | None
    paid_at__isnull: datetime | None
    completely_repaid_at__isnull: bool | None
    completely_repaid_at: datetime | None

    fill_percentage: int | None
    user_id: int | None
    order_id: int | None