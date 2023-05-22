import datetime
from pydantic import BaseModel, Field, validator


################################## Base Classes ##################################
class UserId(BaseModel):
    user_id: int = \
        Field(...,
              title='user id',
              description='db id of user record',
              example=13
              )


class FirstName(BaseModel):
    first_name: str | None = \
        Field(...,
              title='first name',
              description='first name of user',
              example="damon"
              )


class LastName(BaseModel):
    last_name: str | None = \
        Field(...,
              title='last name',
              description='last name of user',
              example="azaddel"
              )


class PhoneNumber(BaseModel):
    phone_number: str | None = \
        Field(...,
              title='user phone number',
              description='user phone number',
              example='0912345678'
              )


class CreatedDate(BaseModel):
    created_at: datetime.date = \
        Field(...,
              title='created_date',
              description='user create date',
              example='1400/01/01')


class Verification(BaseModel):
    verified: bool | None = \
        Field(...,
              title='verified',
              description='is user verified',
              example=True
              )


# class Amount(BaseModel):
#     amount: int = \
#         Field(...,
#               title='amount',
#               description='money',
#               example=1500000)
#
#     @validator('max_credit', 'available_credit')
#     def convert_rial_to_tmn(cls, v):
#         return int(v / 10)


################################## Merged Classes ##################################
class UserListResponse(
    UserId,
    FirstName,
    LastName,
    PhoneNumber,
    Verification,
    CreatedDate
):
    pass


################################## Util Classes ##################################
class CqGetUserDetails(BaseModel):
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    user_id: int | None
    verified: bool | None
    created_at_ge: datetime.datetime | None
    created_at_le: datetime.datetime | None
