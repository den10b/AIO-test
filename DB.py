from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


class DATA(Model):
    key = fields.TextField(pk=True)
    user_id = fields.IntField()
    question = fields.TextField()

    class Meta:
        table = "questions"


class ACTIVE_USERS(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()

    class Meta:
        table = "users"


async def run():
    await Tortoise.init(db_url="postgres://postgres:1234@localhost:5432/postgres", modules={"models": ["DB"]})
    await Tortoise.generate_schemas()
