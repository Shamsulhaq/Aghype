from fastapi import Depends, APIRouter
from backend.schemas.user_schemas import UserOut
from backend.models.user_models import User
from typing import List
from backend.core.permissions import has_admin_permissions


router = APIRouter(prefix="/users", tags=["users"])


@router.get('/', response_model=List[UserOut])
async def get_users(current_user=Depends(has_admin_permissions)):
    users = await User.all()
    return users