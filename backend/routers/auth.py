from fastapi import APIRouter, HTTPException, Depends, status
from backend.schemas.user_schemas import UserCreate, Token, UserOut, LoginForm
from backend.models.user_models import User
from backend.core.auth import hash_password, verify_password, create_access_token, decode_token
from tortoise.exceptions import DoesNotExist
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post('/register', response_model=UserOut)
async def register(payload: UserCreate):
    user = await User.create(
    username=payload.username,
    email=payload.email,
    hashed_password=hash_password(payload.password),
    role=payload.role,
    )
    return user


@router.post('/login', response_model=Token)
async def login(payload: LoginForm):
    username = payload.username
    password = payload.password
    try:
        user = await User.get(username=username)
    except DoesNotExist:
        raise HTTPException(status_code=400, detail='Invalid credentials')
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Invalid credentials')
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}


@router.get('/me', response_model=UserOut)
async def read_users_me(current_user=Depends(oauth2_scheme)):
    return await get_current_user(current_user)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id = int(payload.get('sub'))
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    return user


