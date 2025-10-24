from tortoise import fields, models
import enum

videos: fields.ReverseRelation["Video"]


class Post(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(150)
    description = fields.TextField(null=True)
    file_path = fields.CharField(255)
    owner = fields.ForeignKeyField("models.User", related_name="videos")
    is_approved = fields.BooleanField(default=False)
    is_ad = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)