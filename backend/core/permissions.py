from fastapi import Depends, HTTPException, status
from backend.routers.auth import get_current_user
from backend.models.user_models import RoleEnum


async def admin_required(user=Depends(get_current_user)):
    if user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
    return user


async def advertiser_or_admin(user=Depends(get_current_user)):
    if user.role not in (RoleEnum.ADVERTISER, RoleEnum.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Advertiser or Admin only")
    return user


async def has_admin_permissions(user=Depends(get_current_user)):
    if user.role not in (RoleEnum.ADMIN, RoleEnum.SUPER_ADMIN, RoleEnum.MODERATOR):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin, Super Admin or Moderator only")
    return user