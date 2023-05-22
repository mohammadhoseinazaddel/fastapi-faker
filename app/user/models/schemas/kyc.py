from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from system.base.schema import GetMultiBaseModel


class KycCreateSchema(BaseModel):
    sabte_ahval_inquired_at: datetime
    sabte_ahval_track_no: str | None
    sabte_ahval_verified: bool | None

    shahkar_inquired_at: datetime
    shahkar_verified: bool | None
    first_name: str | None
    last_name: str | None
    father_name: str | None


class KycUpdateSchema(BaseModel):
    sabte_ahval_inquired_at: datetime | None
    sabte_ahval_track_no: str | None
    sabte_ahval_verified: bool | None

    shahkar_inquired_at: datetime | None
    shahkar_verified: bool | None
    first_name: str | None
    last_name: str | None
    father_name: str | None


class KycGetMultiSchema(GetMultiBaseModel):
    sabte_ahval_track_no: str | None
    sabte_ahval_verified: bool | None

    shahkar_verified: bool | None
    first_name: str | None
    last_name: str | None
    father_name: str | None
