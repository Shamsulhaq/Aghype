from tortoise.contrib.fastapi import register_tortoise
from backend.config import settings


def init_db(app):
    register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["backend.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
    )