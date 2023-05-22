import datetime

import jdatetime
from pydantic import BaseModel, Field

from system.base.schema import GetMultiBaseModel
from utils import JDateNavigator


def _calculate_settlement_time():
    jalali_today = jdatetime.date.today()
    jdate_navigator_obj = JDateNavigator(jalali_date=jdatetime.date.today())
    # if jalali_today.day < 25:
    #     jdate_navigator_obj.next_month()
    #     jdate_navigator_obj.replace(day=5)
    #     return jdate_navigator_obj.get_date_in_utc()
    # else:
    #     jdate_navigator_obj.next_month()
    #     jdate_navigator_obj.next_month()
    #     jdate_navigator_obj.replace(day=5)
    #     return jdate_navigator_obj.get_date_in_utc()
    return jdate_navigator_obj.get_date_in_utc()


class DebtCreateSchema(BaseModel):
    fund_id: int
    amount: int
    settlement_time: datetime.datetime = Field(default_factory=_calculate_settlement_time)
    user_id: int


class DebtUpdateSchema(BaseModel):
    paid_at: datetime.datetime | None


class DebtGetMultiSchema(GetMultiBaseModel):
    fund_id: int | None
    payment_id: int | None
    paid_at: datetime.datetime | None
    user_id: int | None
    payment_detail_id: int | None
    paid_at__isnull: bool | None
    deleted_at__isnull: bool | None


class GetMultiFunDebt(GetMultiBaseModel):
    pass
