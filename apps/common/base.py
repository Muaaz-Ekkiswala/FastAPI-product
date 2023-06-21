import datetime
import uuid

from sqlalchemy import Column, func, TIMESTAMP, Boolean
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr
from sqlalchemy_utils import UUIDType


@as_declarative()
class Base:
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    creation_date: datetime = Column(TIMESTAMP(timezone=True), server_default=func.now())
    update_date: datetime = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    created_by = Column(UUIDType(binary=False), nullable=True)
    updated_by = Column(UUIDType(binary=False), nullable=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()