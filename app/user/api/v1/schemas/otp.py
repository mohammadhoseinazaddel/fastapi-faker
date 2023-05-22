from pydantic import BaseModel, Field


class SendOtpRequest(BaseModel):
    mobile: str = \
        Field(...,
              title='Mobile',
              description='Mobile Number',
              example='09120001122',
              )


class SendOtpResponse(SendOtpRequest):
    send_sms_status: bool = \
        Field(...,
              title='Send OTP status',
              description='Send OTP status',
              example=True,
              )
    message: str = \
        Field(...,
              title='Send OTP message',
              description='Send OTP message',
              example='شما می توانید پس ا ۱۲۰ ثانیه دوباره تلاش کنید',
              )


class CheckOtpRequest(BaseModel):
    mobile: str = \
        Field(...,
              title='Mobile',
              description='Mobile Number',
              example='09120001122',
              )
    otp: str = \
        Field(...,
              title='OTP',
              description='One Time Password',
              example='121234',
              )


class CheckOtpResponse(BaseModel):
    access_token: str = \
        Field(...,
              title='Access Token',
              description='Access Token',
              example='as/dlkjnieugr9ya[e98vhldaibvn',
              )
    refresh_token: str = \
        Field(...,
              title='Refresh Token',
              description='Refresh Token',
              example='as/dlkjnieugr9ydsffa[e98vhldaibvn',
              )
    token_type: str = \
        Field(...,
              title='token_type',
              description='token_type',
              example='bearer',
              )
    user: dict = \
        Field(...,
              title='user',
              description='user',
              example={'national_code': '1142332209',},
              )