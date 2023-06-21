from apps.users.models import User
from apps.users.schemas import UserCreate, UserUpdate
from db.crud import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    ...


user_action = CRUDUser(User)