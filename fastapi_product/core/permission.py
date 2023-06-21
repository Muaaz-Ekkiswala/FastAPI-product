import logging
from functools import wraps
from typing import Union, List

from fastapi import HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from starlette import status

logger = logging.getLogger(__name__)


def valid_user(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        user = authorize.get_raw_jwt()
        user["id"] = authorize.get_jwt_subject()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err)
        )
    return user


# def login_required(
#         users: Union[List[str], None, str] = None,
# ):
#     def decorator_auth(func, *args, **kwargs):
#         authorize_user = kwargs['user']
#         if authorize_user['user_type'] not in users:
#             logger.error("Invalid Credentials for user %s, user_type %s",
#                          authorize_user.get("email"), authorize_user.get("user_type"))
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Invalid Credentials"
#             )
#
#         return await func(*args, **kwargs)
#
#     return decorator_auth
