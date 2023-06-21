from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from apps.users.crud import user_action
from apps.users.models import User
from apps.users.schemas import UserCreate, GetAuthSchema
from apps.users.utils import get_hashed_password
from db.dependency import get_db
from fastapi_product.core.permission import valid_user

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@user_router.post("/", response_model=GetAuthSchema)
async def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends(),
):
    payload_data = payload.dict()
    User.check_user_exist(db=db, email=payload_data.get('email'))
    User.check_mobile_exist(db=db, mobile=payload_data.get('mobile'))
    payload_data['password'] = get_hashed_password(password=payload.password)
    new_user = await user_action.create(db=db, obj_in=payload_data)
    response = {
        "access": authorize.create_access_token(
            subject=str(new_user.id), user_claims=payload_data, fresh=True
        ),
        "refresh": authorize.create_refresh_token(subject=str(new_user.id), user_claims=payload_data),
        "user": new_user,
    }
    return response


@user_router.put("/{id}/")
# @login_required()
async def update_user(
        id: str,
        db: Session = Depends(get_db),
        user: dict = Depends(valid_user),
):
    user_instance = db.query(User).filter(User.id == id)
    updated_user = await user_action.update(db=db, db_obj=user_instance, obj_in=id)
    return updated_user
