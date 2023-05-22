import datetime
from pydantic import BaseModel, Field, validator


################################## Base Classes ##################################
class UserId(BaseModel):
    user_id: int = \
        Field(...,
              title='credit user id',
              description='db id of user record',
              example=13
              )


class CreatedDate(BaseModel):
    created_at: datetime.date = \
        Field(...,
              title='created_date',
              description='credit create date',
              example='1400/01/01')


class AvailableCredit(BaseModel):
    available_credit: int = \
        Field(...,
              title='amount',
              description='money',
              example=1500000)

    @validator('available_credit')
    def convert_rial_to_tmn(cls, v):
        return int(v / 10)


class UsedCredit(BaseModel):
    used_credit: int = \
        Field(...,
              title='amount',
              description='money',
              example=1500000)

    @validator('used_credit')
    def convert_rial_to_tmn(cls, v):
        return int(v / 10)


################################## Merged Classes ##################################
class UserCreditResponse(
    UserId,
    CreatedDate,
    AvailableCredit,
    UsedCredit
):
    pass


################################## Util Classes ##################################
class CqGetCreditDetails(BaseModel):
    user_id: int | None
    created_at_ge: datetime.datetime | None
    created_at_le: datetime.datetime | None
