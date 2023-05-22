from pydantic import BaseModel, Field


class ScoreMeResponse(BaseModel):
    credit_score: float = \
        Field(...,
              title='user_credit',
              description='user credit score',
              example=0.25
              )

    # age: int = \
    #     Field(...,
    #           title='age',
    #           description='age that user for calc credit score',
    #           example=30
    #           )
