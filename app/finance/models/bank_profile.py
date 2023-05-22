from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint, Index

from system.base.crud import CRUDBase
from system.dbs.models import Base

from finance.models.schemas.bank_profile import BankProfileCreate, BankProfileUpdate, BankProfileGetMulti


class FncBankProfile(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer)
    merchant_id = Column(Integer)
    is_default = Column(Boolean)

    first_name = Column(String)
    last_name = Column(String)
    bank_name = Column(String)
    account_no = Column(String)
    iban = Column(String)
    card_no = Column(String)

    __table_args__ = (
        UniqueConstraint('merchant_id', 'is_default', name='just_one_default_account'),
        Index('merchant_default_account', "merchant_id", "is_default"),
    )


class BankProfileCRUD(
    CRUDBase[
        FncBankProfile,
        BankProfileCreate,
        BankProfileUpdate,
        BankProfileGetMulti
    ]
):
    pass


bank_profile_crud = BankProfileCRUD(FncBankProfile)
