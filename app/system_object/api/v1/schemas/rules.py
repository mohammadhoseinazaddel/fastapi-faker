from pydantic import BaseModel, Field


class RulesCreateRequest(BaseModel):
    version: str = \
        Field(...,
              min_length=0,
              max_length=15,
              title='version',
              description='version',
              example='1.0.0',
              )
    rules: str = \
        Field(...,
              min_length=3,
              max_length=2048,
              title='Rules',
              description='Rules',
              example='قوانین و مقررات',
              )


class RulesIdResponse(BaseModel):
    id: int = \
        Field(...,
              # min_length=1,
              # max_length=12,
              title='Rules Id',
              description='Rules Id',
              example=1,
              )


class RulesGetResponse(BaseModel):
    id: int = \
        Field(...,
              # min_length=1,
              # max_length=12,
              title='Rules Id',
              description='Rules Id',
              example=1,
              )
    version: str = \
        Field(...,
              min_length=0,
              max_length=15,
              title='version',
              description='version',
              example='1.0.0',
              )
    rules: str = \
        Field(...,
              min_length=3,
              max_length=2048,
              title='Rules',
              description='Rules',
              example='قوانین و مقررات',
              )

    class Config:
        orm_mode = True
