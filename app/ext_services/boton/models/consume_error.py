from sqlalchemy import Column, Integer, String

from system.base.crud import CRUDBase
from system.dbs.models import Base
from .schemas.consume_error import CreateConsumeError, UpdateConsumeError, GetMultiConsumeError


class ExtBotonConsumeError(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    queue = Column(String, index=True)
    body = Column(String, )
    error = Column(String, )

    status = Column(String, default='INIT', index=True)


class ConsumeErrorCRUD(
    CRUDBase[
        ExtBotonConsumeError,
        CreateConsumeError,
        UpdateConsumeError,
        GetMultiConsumeError,
    ]
):
    pass


consume_error_crud = ConsumeErrorCRUD(ExtBotonConsumeError)
