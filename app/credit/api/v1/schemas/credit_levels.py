from pydantic import BaseModel, Field


class CreditLevelsResponse(BaseModel):
    display_name: str = \
        Field(...,
              title='display_name',
              description='display name',
              example="سطح ۱",
              )
    credit: int = \
        Field(...,
              title='credit',
              description='given credit to user',
              example=300000,
              )
    is_eligble: bool = \
        Field(...,
              title='is_eligble',
              description='Is user eliglble for this level',
              example=True,
              )
