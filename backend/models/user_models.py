from tortoise import fields, models
import enum


class RoleEnum(str, enum.Enum):
    USER = "user"
    ADVERTISER = "advertiser"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    email = fields.CharField(100, unique=True)
    hashed_password = fields.CharField(255)
    role = fields.CharEnumField(RoleEnum, default=RoleEnum.USER)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

