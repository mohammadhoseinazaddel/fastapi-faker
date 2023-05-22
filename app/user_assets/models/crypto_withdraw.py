import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Float

from system.base.crud import CRUDBase
from system.dbs.models import Base
from .schemas.crypto_withdraw import CreateCryptoWithdraw, UpdateCryptoWithdraw, GetMultiCryptoWithdraw
from .wallet_address import UasWalletAddress


class UasCryptoWithdraw(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    unique_id = Column(Integer, nullable=True)  # unique_id
    trace_id = Column(String, default=uuid.uuid4, index=True)  # کد پیگیری مشتری
    user_id = Column(Integer, nullable=False)
    wallet_address_id = Column(Integer, ForeignKey(UasWalletAddress.id), nullable=False)

    from_address = Column(String, nullable=True)
    from_memo = Column(String)

    to_address = Column(String, nullable=False)
    to_memo = Column(String)
    amount = Column(Float, nullable=False)

    ack = Column(Integer)
    verify = Column(Integer)

    bundle_id = Column(Integer)
    is_identical = Column(Integer)
    fee = Column(Float)

    tx_id = Column(String)

    status = Column(String, )


class CryptoWithdrawCRUD(
    CRUDBase[
        UasCryptoWithdraw,
        CreateCryptoWithdraw,
        UpdateCryptoWithdraw,
        GetMultiCryptoWithdraw,
    ]
):
    pass


crypto_withdraw_crud = CryptoWithdrawCRUD(UasCryptoWithdraw)
