from fastapi import APIRouter

from apps.users.api.auth import auth_router
from apps.users.api.user import user_router

users_router = APIRouter()

users_router.include_router(auth_router)
users_router.include_router(user_router)
