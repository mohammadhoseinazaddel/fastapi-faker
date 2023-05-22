from pydantic import BaseModel, Field


class RefrefshTokenRequest(BaseModel):
    access_token: str = \
        Field(
            ...,
            title='access_token',
            description='access token',
            example='sdkjhwp98eyfoiuaduf0[7sadf[ygauobd'
        )

    refresh_token: str = \
        Field(
            ...,
            title='refresh_token',
            description='refresh token',
            example='sdkjhwp98eyfoiuaduf0[7sadf[ygauobd'
        )


class RefrefshTokenResponse(BaseModel):
    access_token: str = \
        Field(
            ...,
            title='access_token',
            description='access token',
            example='sdkjhwp98eyfoiuaduf0[7sadf[ygauobd'
        )

    refresh_token: str = \
        Field(
            ...,
            title='refresh_token',
            description='refresh token',
            example='sdkjhwp98eyfoiuaduf0[7sadf[ygauobd'
        )


class WallexLoginResponse(BaseModel):
    redirect_url: str = \
        Field(...,
              title='redirect_url',
              description='redirect_url',
              example='https://wallex.ir/oauth/login',
              )


class LoginBySateResponse(BaseModel):
    access_token: str = \
        Field(...,
              title='access_token',
              description='access_token',
              example='dslkgsd9876gaksfb',
              )
    token_type: str = \
        Field(...,
              title='token_type',
              description='token_type',
              example='Bearer',
              )
    user: dict = \
        Field(...,
              title='user',
              description='user',
              example={'national_code': '1142332209', },
              )


class LoginBySateRequest(BaseModel):
    state: str = \
        Field(...,
              title='state',
              description='login state code',
              example='1234-1234-1234-1234',
              )
