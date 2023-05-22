from sqlalchemy import Boolean, Column, Integer, String, DateTime

from system.base.crud import CRUDBase
from system.dbs.models import Base

from user.models.schemas.kyc import KycCreateSchema, KycUpdateSchema, KycGetMultiSchema


class UsrKyc(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    sabte_ahval_inquired_at = Column(DateTime, )
    sabte_ahval_track_no = Column(String)
    sabte_ahval_verified = Column(Boolean, default=False)

    shahkar_inquired_at = Column(DateTime, )
    shahkar_verified = Column(Boolean, default=False)

    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)


class KycCRUD(
    CRUDBase[
        UsrKyc,
        KycCreateSchema,
        KycUpdateSchema,
        KycGetMultiSchema
    ]
):
    pass


kyc_crud = KycCRUD(model=UsrKyc)
