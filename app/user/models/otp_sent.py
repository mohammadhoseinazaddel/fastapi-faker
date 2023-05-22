from sqlalchemy import Column, Integer, String, DateTime

from system.base.crud import CRUDBase
from system.dbs.models import Base
from .schemas.otp_sent import OtpSentCreateSchema, OtpSentUpdateSchema, OtpSentGetMultiSchema


class UsrOtpSent(Base):
    id = Column(Integer, primary_key=True, nullable=False)

    mobile = Column(String, nullable=False, index=True, )
    otp = Column(String, nullable=False)
    sent_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, )


class OtpSentCRUD(
    CRUDBase[
        UsrOtpSent,
        OtpSentCreateSchema,
        OtpSentUpdateSchema,
        OtpSentGetMultiSchema
    ]
):
    pass


otp_crud = OtpSentCRUD(UsrOtpSent)
