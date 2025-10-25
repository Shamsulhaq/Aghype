from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form, Query
from typing import List
import os
from backend.schemas.post_schemas import PostCreate, PostOut
from backend.models.post_models import Post
from backend.routers.auth import get_current_user
from backend.config import settings
from backend.core.permissions import has_admin_permissions
from backend.core.paginations import paginate
# from backend.schemas.pagination_schemas import PaginatedResponse
import aiofiles


router = APIRouter(prefix="/posts", tags=["posts"])


# @router.get('/', response_model=List[PostOut])
@router.get('/')
async def get_posts(current_user=Depends(get_current_user), start: int = Query(0, ge=0), limit: int = Query(10, le=100),):
    if current_user.role not in ['admin', 'super_admin', 'moderator']:
        return await paginate(Post, start=start, limit=limit, filters={"is_approved": True}, order_by=['-created_at'])
    else:
        return await paginate(Post, start=start, limit=limit, order_by=['-created_at'])


async def post_create_form(
    title: str = Form(...),
    description: str | None = Form(None),
    is_ad: bool = Form(False),
) -> PostCreate:
    return PostCreate(title=title, description=description, is_ad=is_ad)



@router.post('/upload', response_model=PostOut)
async def upload_post(metadata: PostCreate = Depends(post_create_form), file: UploadFile = File(...), current_user=Depends(get_current_user)):
    # save file to MEDIA_DIR
    os.makedirs(settings.MEDIA_DIR, exist_ok=True)
    filename = f"{current_user.id}_{int(__import__('time').time())}_{file.filename}"
    dest = os.path.join(settings.MEDIA_DIR, filename)
    async with aiofiles.open(dest, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    video = await Post.create(
        title=metadata.title,
        description=metadata.description,
        file_path=dest,
        owner_id=current_user.id,
        is_ad=metadata.is_ad,
    )
    return video


@router.get('/pending')
async def pending_posts(current_user=Depends(has_admin_permissions), start: int = Query(0, ge=0), limit: int = Query(10, le=100),):
    return await paginate(Post, start=start, limit=limit, filters={"is_approved": False}, order_by=['-created_at'])


@router.put('/{video_id}/approve')
async def approve_post(video_id: int, current_user=Depends(get_current_user)):
    if current_user.role.name != 'ADMIN':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    video = await Post.get_or_none(id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail='Video not found')
    video.is_approved = True
    await video.save()
    return {"ok": True}


@router.delete('/{video_id}/reject')
async def reject_post(video_id: int, current_user=Depends(get_current_user)):
    if current_user.role.name != 'ADMIN':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    video = await Post.get_or_none(id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail='Video not found')
    await video.delete()
    return {"ok": True}