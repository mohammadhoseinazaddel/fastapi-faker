import datetime

from pydantic import Field, BaseModel, validator


class InfoResponse(BaseModel):
    credit: int = \
        Field(...,
              title='total-credit',
              description='Total credit amount',
              example=15000000,
              )
    debt: int = \
        Field(...,
              title='total-debt',
              description='Total debt amount in tmn',
              example=15000000,
              )

    max_credit: int = \
        Field(...,
              title='max-credit',
              description='Total credit of user means used and unused',
              example=15000000,
              )

    credit_dont_need_collateral: int = \
        Field(...,
              title='free-credit',
              description='free credit amount',
              example=15000000,
              )

    credit_need_collateral: int = \
        Field(...,
              title='non-free-credit',
              description='non-free credit amount',
              example=15000000,
              )

    due_date: datetime.date = \
        Field(...,
              title='due-date',
              description='debt due date',
              example='2023-05-26',
              )

    @validator('credit', 'debt', 'max_credit', 'credit_dont_need_collateral', 'credit_need_collateral')
    def convert_rial_to_tmn(cls, v):
        return v / 10