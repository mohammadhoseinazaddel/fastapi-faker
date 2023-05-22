from pydantic import BaseModel, Field, validator


class CreateBankProfileRequest(BaseModel):
    card_number: str = \
        Field(...,
              min_length=16,
              max_length=16,
              title='User card number',
              description='Card number of user',
              example="6104998788978987",
              )


class CreateBankProfileResponse(BaseModel):
    status: str = \
        Field(...,
              title='operation status',
              description='will be success or raising exception in fact its not necessary response model for this api',
              example="success",
              )
