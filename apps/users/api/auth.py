import jwt
from fastapi import Depends, HTTPException, APIRouter
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette import status

from apps.users.models import User
from apps.users.schemas import AccessTokenSchema, RefreshTokenSchema, GetAuthSchema, LoginSchema
from apps.users.utils import verify_password
from db.dependency import get_db
from fastapi_product.core.config import settings

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post('/login/', response_model=GetAuthSchema)
async def login(
        payload: LoginSchema,
        db: Session = Depends(get_db),
        authorize: AuthJWT = Depends(),
):
    payload_data = payload.dict()
    existing_user = User.get_user_by_email(db=db, email=payload.email)
    if existing_user:
        is_verified = verify_password(password=payload.password, hashed_pass=existing_user.get('password'))
        if is_verified:
            response = {
                "access": authorize.create_access_token(
                    subject=str(existing_user.id), user_claims=payload_data, fresh=True
                ),
                "refresh": authorize.create_refresh_token(subject=str(existing_user.id), user_claims=payload_data),
                "user": existing_user,
            }
        else:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or password you entered is incorrect"
            )
    else:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with this {payload.email} not exist"
        )
    return response


@auth_router.post('/refresh/', response_model=AccessTokenSchema)
async def refresh(payload: RefreshTokenSchema, authorize: AuthJWT = Depends()):
    """
    Create a access token with 15 minutes for expired time (default),
    info for param and return check to function create token
    """
    try:
        refresh_payload = jwt.decode(
            payload.refresh, settings.AUTHJWT_SECRET_KEY, algorithms=["HS256"]
        )
        payload = {
            "email": refresh_payload.get('email'),
            "user_type": refresh_payload.get('user_type'),
            "entity_id": refresh_payload.get('entity_id'),
        }

        new_access_token = authorize.create_access_token(
            subject=refresh_payload['sub'], fresh=True, user_claims=payload
        )
        return {"access": new_access_token}
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong. Exception : {err}",
        )
