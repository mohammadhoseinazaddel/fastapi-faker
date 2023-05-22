import datetime
import uuid
from typing import Type

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, CheckConstraint
from sqlalchemy.orm import Session, relationship

from system.base.crud import CRUDBase, ModelType
from system.dbs.models import Base
from .kyc import UsrKyc
from .schemas.user import UserCreateSchema, UserGetMultiSchema, UserUpdateSchema
from .user_merchants import user_merchants


class UsrUser(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    kyc_id = Column(Integer, ForeignKey(UsrKyc.id), nullable=True)

    email = Column(String, )
    mobile = Column(String, index=True, unique=True)
    username = Column(String, index=True, unique=True)
    hashed_pass = Column(String, )

    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)
    gender = Column(String)
    national_code = Column(String, index=True, unique=True)
    birth_date = Column(Date, nullable=True)
    profile_image = Column(String, )

    last_login = Column(DateTime, )
    identifier = Column(String, index=True, default=uuid.uuid4)

    is_disabled = Column(Boolean, default=False)

    verified = Column(Boolean, default=False)
    verified_by = Column(String, )
    verified_at = Column(DateTime)

    __table_args__ = (
        CheckConstraint('NOT(mobile IS NULL AND username IS NULL)'),
    )

    merchant = relationship(
        'UsrMerchant', secondary=user_merchants, uselist=False, back_populates="user"
    )


class UserCRUD(
    CRUDBase[
        UsrUser,
        UserCreateSchema,
        UserUpdateSchema,
        UserGetMultiSchema
    ]
):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)

    def get_all_user_details(
            self,
            db: Session,
            limit: int = None,
            skip: int = None,
            phone_number: str = None,
            first_name: str = None,
            last_name: str = None,
            user_id: int = None,
            verified: bool = None,
            created_at_ge: datetime.datetime = None,
            created_at_le: datetime.datetime = None,
    ):

        query = db.query(
            self.model
        )
        if user_id:
            query = query.filter(self.model.id == user_id)
        if phone_number:
            query = query.filter(self.model.mobile == phone_number)
        if first_name:
            query = query.filter(self.model.first_name == first_name)
        if last_name:
            query = query.filter(self.model.last_name == last_name)
        if verified:
            query = query.filter(self.model.verified == verified)
        if created_at_ge:
            query = query.filter(self.model.created_at >= created_at_ge)
        if created_at_le:
            query = query.filter(self.model.created_at <= created_at_le)

        # query.filter(self.model.merchant.)

        # total_count = query.count()
        if limit:
            query = query.limit(limit)
        if skip:
            query = query.offset(skip)
        # return {"query_result": query.all(), "total_count": total_count}
        return query


user_crud = UserCRUD(UsrUser)
