from fastapi import Depends, APIRouter, Query
from backend.schemas.user_schemas import UserOut
from backend.models.user_models import User
from typing import List
from backend.core.permissions import has_admin_permissions
from backend.core.paginations import paginate


router = APIRouter(prefix="/users", tags=["users"])


@router.get('/')
async def get_users(
    current_user=Depends(has_admin_permissions),
    start: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    return await paginate(User, start=start, limit=limit)