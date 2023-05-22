import datetime
import uuid

from typing import Dict, Any
from sqlalchemy import Column, Integer, String, ForeignKey, func

from finance.models.bank_profile import FncBankProfile
from finance.models.schemas.transfer import TransferCreate, TransferUpdate, TransferGetMulti
from system.base.crud import CRUDBase, ModelType
from typing import Type
from system.dbs.models import Base
from sqlalchemy.orm import Session, relationship


class FncTransfer(Base):
    id = Column(Integer, primary_key=True, index=True)
    bank_profile_id = Column(Integer, ForeignKey(FncBankProfile.id), nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)  # Rial
    description = Column(String)
    merchant_id = Column(Integer, nullable=True, index=True)
    ext_service_name = Column(String, nullable=False)  # Jibit

    input_type = Column(String, nullable=True)
    input_unique_id = Column(Integer, nullable=True)

    batch_id = Column(String, default=uuid.uuid4())
    transfer_id = Column(String, default=uuid.uuid4(), index=True)
    status = Column(String, default='init')
    error_message = Column(String, nullable=True)

    bank_profile = relationship('FncBankProfile')


class TransferCRUD(
    CRUDBase[
        FncTransfer,
        TransferCreate,
        TransferUpdate,
        TransferGetMulti
    ]
):
    
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)

    def get_all_transfers_qeuery_set(
            self,
            db: Session,
            created_at_ge: datetime.datetime = None,
            created_at_le: datetime.datetime = None,
            transfer_price_ge: float = None,
            transfer_price_le: float = None,
            merchant_id: int = None,
            bank_name: str = None,
            transfer_type: str = None,
            transfer_id: int = None
    ):

        query = db.query(
            self.model,
            FncBankProfile
        )
        query = query.join(FncBankProfile, self.model.bank_profile_id == FncBankProfile.id)
        if bank_name:
            query = query.filter(FncBankProfile.bank_name == bank_name)
        if merchant_id:
            query = query.filter(self.model.merchant_id == merchant_id)
        if transfer_id:
            query = query.filter(self.model.id == transfer_id)
        if transfer_type:
            query = query.filter(self.model.type == transfer_type)
        if created_at_ge:
            query = query.filter(self.model.created_at >= created_at_ge)
        if created_at_le:
            query = query.filter(self.model.created_at <= created_at_le)
        if transfer_price_ge:
            query = query.filter(self.model.amount >= transfer_price_ge)
        if transfer_price_le:
            query = query.filter(self.model.amount <= transfer_price_le)
            
        return query

    def get_all_transfers(
            self,
            db: Session,
            limit: int = None,
            skip: int = None,
            created_at_ge: datetime.datetime = None,
            created_at_le: datetime.datetime = None,
            transfer_price_ge: float = None,
            transfer_price_le: float = None,
            bank_name: str = None,
            transfer_type: str = None,
            transfer_id: int = None,
            merchant_id: int = None
    ) -> Dict[str, Any]:

        query = self.get_all_transfers_qeuery_set(db,
                                                  created_at_ge=created_at_ge,
                                                  created_at_le=created_at_le,
                                                  transfer_price_ge=transfer_price_ge,
                                                  transfer_price_le=transfer_price_le,
                                                  transfer_id=transfer_id,
                                                  bank_name=bank_name,
                                                  transfer_type=transfer_type,
                                                  merchant_id=merchant_id)

        total_count = query.count()

        if limit:
            query = query.limit(limit)
        if skip:
            query = query.offset(skip)

        return {"query_result": query.all(), "total_count": total_count}

    def get_all_transfers_summury_query_set(
            self,
            db: Session,
            created_at_ge: datetime.datetime = None,
            created_at_le: datetime.datetime = None,
            transfer_price_ge: float = None,
            transfer_price_le: float = None,
            merchant_id: int = None
    ):

        subquery = self.get_all_transfers_qeuery_set(db,
                                                  created_at_ge,
                                                  created_at_le,
                                                  transfer_price_ge,
                                                  transfer_price_le,
                                                  merchant_id)
        
        query = Session.query(func.sum(subquery.amount).label("sum")).group_by(subquery.merchant_id)
        
        return int(query.all())


transfer_crud = TransferCRUD(FncTransfer)
