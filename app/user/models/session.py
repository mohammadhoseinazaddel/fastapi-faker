from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, Index

from system.base.crud import CRUDBase
from system.dbs.models import Base

from user.models.schemas.session import SessionCreateSchema, SessionUpdateSchema, SessionGetMultiSchema


class UsrSession(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    token = Column(String, index=True)
    user_id = Column(Integer, index=True)
    expire_at = Column(DateTime)

    os = Column(String)
    os_version = Column(String)
    browser = Column(String)
    browser_version = Column(String)
    ip = Column(String)

    token_first_used_at = Column(DateTime)
    token_last_used_at = Column(DateTime)

    is_valid = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint("token", "user_id", name='usr_session_unique', ),
    )


class SessionCRUD(
    CRUDBase[
        UsrSession,
        SessionCreateSchema,
        SessionUpdateSchema,
        SessionGetMultiSchema
    ]
):
    pass


session_crud = SessionCRUD(UsrSession)
