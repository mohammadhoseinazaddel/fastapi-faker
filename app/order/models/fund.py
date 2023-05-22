from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, JSON

from system.base.crud import CRUDBase
from system.dbs.models import Base
from .pay import OrdPay
from .schemas.fund import FundCreateSchema, FundUpdateSchema, FundGetMultiSchema


class OrdFund(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    # order info
    order_id = Column(Integer, ForeignKey(OrdPay.id), nullable=False, unique=True)
    order_amount = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    # credit info
    used_free_credit = Column(Integer, nullable=False, default=0)
    used_non_free_credit = Column(Integer, nullable=False, default=0)
    repaid_free_credit = Column(Integer, default=0)
    repaid_non_free_credit = Column(Integer, default=0)
    used_asset_json = Column(JSON, nullable=True)
    extra_money_to_pay = Column(Integer, default=0)

    # collateral info
    need_collateral = Column(Boolean, default=False)
    collateral_confirmed = Column(Boolean, default=False)

    need_wallex_asset = Column(Boolean, default=False)
    wallex_block_request_id = Column(String, nullable=True)

    # pay info
    payment_amount = Column(Integer, default=0)
    payment_id = Column(Integer, nullable=True)  # this is id of sum of extra_pay and first loan
    paid_at = Column(DateTime, nullable=True)
    completely_repaid_at = Column(DateTime, nullable=True)

    fill_percentage = Column(Integer, nullable=False, default=0, )


class FundCRUD(CRUDBase[OrdFund, FundCreateSchema, FundUpdateSchema, FundGetMultiSchema]):
    pass


fund_crud = FundCRUD(model=OrdFund)
