from fastapi import HTTPException
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import column_property
from sqlalchemy_utils import EmailType
from starlette import status

from apps.common.base import Base


class User(Base):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    mobile = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=False)
    password = Column(String, nullable=False)
    full_name = column_property(first_name + " " + last_name)

    @staticmethod
    def check_mobile_exist(db, mobile):
        existing_user = db.query(User).filter(User.mobile == mobile)
        if existing_user.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Mobile already exist",
            )
        return True

    @staticmethod
    def check_user_exist(db, email):
        existing_user = db.query(User).filter(User.email == email)
        if existing_user.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist",
            )

    @staticmethod
    def get_user_by_email(db, email):
        existing_user = db.query(User).filter(User.email == email).first()
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not Found",
            )
        return existing_user