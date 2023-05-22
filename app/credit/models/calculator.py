import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, String, BigInteger
from sqlalchemy.dialects.postgresql import JSON

from credit.models.schemas.calculator import CalculatorCreateSchema, CalculatorUpdateSchema, CalculatorGetMulti
from credit.models.user import CrdUser
from system.base.crud import CRUDBase, ModelType
from typing import Type
from sqlalchemy.orm import Session
from system.dbs.models import Base


class CrdCalculator(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    credit_id = Column(Integer, ForeignKey(CrdUser.id), nullable=False)

    input_type = Column(String, nullable=True)
    input_unique_id = Column(Integer, nullable=True)

    non_free_credit = Column(BigInteger, nullable=False)  # available credit
    used_non_free_credit = Column(BigInteger, nullable=False)

    free_credit = Column(Integer, nullable=False)
    used_free_credit = Column(Integer, nullable=False)
    asset_json = Column(JSON)
    cs = Column(Float, nullable=False)


class CalculatorCreditCRUD(
    CRUDBase[
        CrdCalculator,
        CalculatorCreateSchema,
        CalculatorUpdateSchema,
        CalculatorGetMulti]
):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)

    def get_user_all_credit_details(
            self,
            db: Session,
            limit: int,
            skip: int,
            user_id: int = None,
            created_at_ge: datetime.datetime = None,
            created_at_le: datetime.datetime = None,
    ):

        query = db.query(
            self.model
        )
        if user_id:
            query = query.filter(self.model.credit_id == user_id)
        if created_at_ge:
            query = query.filter(self.model.created_at >= created_at_ge)
        if created_at_le:
            query = query.filter(self.model.created_at <= created_at_le)

        total_count = query.count()
        query = query.offset(skip).limit(limit)
        return {"query_result": query.all(), "total_count": total_count}


credit_calculator_crud = CalculatorCreditCRUD(CrdCalculator)
