from datetime import datetime
from typing import Any

from sqlalchemy import Integer, Float, String, Column, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr


class TimeStampMixin:
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)


@as_declarative()
class Base(TimeStampMixin):
    id: Any
    __name__: str

    # Generate __table name__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__
        table_name = []
        for index, letter in enumerate(name):
            if letter.isupper() and index != 0:
                table_name.append('_' + letter.lower())
            else:
                table_name.append(letter)
        return ''.join(table_name).lower()


class TransactionModelFields:
    type = Column(String, nullable=False)

    input_type = Column(String, nullable=False)
    input_unique_id = Column(Integer, nullable=False)

    amount = Column(Float, nullable=False)
    user_id = Column(Integer, nullable=False)
