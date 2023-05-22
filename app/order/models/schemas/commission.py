from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class CreateCommission(BaseModel):
    category: str
    merchant_id: int
    pgw_commission_rate: float = 0.0
    credit_commission_rate: float = 0.0
    credit_limit: int | None
    decrease_fee_on_pay_gw_settle: bool = True
    decrease_commission_on_refund: bool = True


class UpdateCommission(BaseModel):
    # nobody could update any record, just add new record
    pass


class GetMultiCommission(GetMultiBaseModel):
    category: str | None
    merchant_id: int | None
