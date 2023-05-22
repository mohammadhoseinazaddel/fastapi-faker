from pydantic import BaseModel, Field


################################## Base Classes ##################################
class Name(BaseModel):
    name: str = \
        Field(...,
              title='merchant-name',
              description='Name of merchant',
              example='بیت کوین',
              )


class MerchantName(BaseModel):
    name: str = \
        Field(...,
              title='merchant-name',
              description='Name of merchant',
              example='بیت کوین',
              )


class FaName(BaseModel):
    name_fa: str = \
        Field(...,
              title='persian-name',
              description='Name in persian',
              example='علی بابا',
              )


class LogoAddress(BaseModel):
    logo_address: str = \
        Field(...,
              title='logo address',
              description='Merchant logo svg file address',
              example='https://api.dev.wallpay.com:8000/statics/logos/merchants/alibaba.svg',
              )


class LogoBackColor(BaseModel):
    logo_background_color: str = \
        Field(...,
              title='background hex color',
              description='Background hex color',
              example="#FFEBE4",
              )


class BankAccountNumber(BaseModel):
    bank_account_number: int = \
        Field(...,
              title='bank acc number',
              description='bank acc number',
              example="1234234234",
              )


class BankIban(BaseModel):
    bank_iban: str | None = \
        Field(...,
              title='bank iban',
              description='bank iban',
              example="IR234234231234234234",
              )


class BankName(BaseModel):
    bank_name: str = \
        Field(...,
              title='bank name',
              description='bank name',
              example="pasargad",
              )


################################## Merged Classes ##################################
class MerchantInfoResponse(
    Name,
    FaName,
    LogoAddress,
    LogoBackColor
):
    pass


class MerchantInfoLoginResponse(
    MerchantName,
    FaName,
    LogoAddress,
    LogoBackColor,
    BankName,
    BankIban,
    BankAccountNumber
):
    pass
