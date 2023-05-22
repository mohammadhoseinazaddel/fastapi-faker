from typing import Literal

from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class BankProfileCreate(BaseModel):
    user_id: int
    first_name: str | None
    last_name: str | None
    bank_name: str | None
    account_no: str | None
    iban: str | None
    card_no: str | None
    merchant_id: int | None


class BankProfileUpdate(BaseModel):
    user_id: int | None
    first_name: str | None
    last_name: str | None
    bank_name: str | None
    account_no: str | None
    iban: str | None
    card_no: str | None
    merchant_id: int | None


class BankProfileGetMulti(GetMultiBaseModel):
    user_id: int | None
    first_name: str | None
    last_name: str | None
    bank_name: str | None
    account_no: str | None
    merchant_id: int | None
    iban: str | None
    card_no: str | None
