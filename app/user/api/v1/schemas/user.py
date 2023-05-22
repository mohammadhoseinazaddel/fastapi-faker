import jdatetime
from pydantic import BaseModel, Field, validator
from pydantic.fields import Any
from pydantic.validators import datetime
from persian_tools import national_id
from unidecode import unidecode


class MeRequest(BaseModel):
    pass


class MeResponse(BaseModel):
    id: int = \
        Field(...,
              title='User id',
              description='User id',
              example=1,
              )
    mobile: Any = \
        Field(...,
              title='User Mobile',
              description='User Mobile',
              example='09120001122',
              )
    national_code: Any = \
        Field(...,

              title='User National Code',
              description='User National Code',
              example='1142332289',
              )
    birth_date: Any = \
        Field(...,
              title='User Birth Date',
              description='User Birth Date',
              example='1142332289',
              )
    first_name: Any = \
        Field(...,
              title='User First Name',
              description='User First Name',
              example='علی',
              )
    last_name: Any = \
        Field(...,
              title='User Last Name',
              description='User Last Name',
              example='علی',
              )

    profile_image: Any = \
        Field(...,
              title='User Image Address',
              description='User Image Address',
              example='http://65.78.90.9:8000/statics/me',
              )
    last_login: Any = \
        Field(...,
              title='last_login',
              description='last_login',
              example='2022-09-07T12:3:09.987654',
              )

    iban_number: Any = \
        Field(...,
              title='iban number',
              description='iban_number',
              example='7654883726354997352',
              )


class ValidationRequest(BaseModel):
    national_code: str
    birth_date: str

    @validator('national_code', pre=True)
    def national_code_validator(cls, national_code):
        if not national_id.validate(national_code):
            raise ValueError("کد ملی نامعتبر است")

        return unidecode(national_code)

    @validator('birth_date')
    def birth_date_validator(cls, multi_date_str: str):
        try:
            return datetime.strptime(multi_date_str, "%Y-%m-%d").date()
        except:
            try:
                li = multi_date_str.split('/')
                li = list(map(int, li))
                p = jdatetime.date(li[0], li[1], li[2])
                return p.togregorian()

            except:
                raise ValueError('تاریخ تولد نامعتبر است')


class ValidationResponse(BaseModel):
    new_access_token: str = \
        Field(...,
              title='Access Token',
              description='Access Token',
              example='as/dlkjnieugr9ya[e98vhldaibvn',
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
              example={'national_code': '1142332209', },
              )
