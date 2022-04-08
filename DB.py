from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


class Active_users(Model):
    user_id = fields.IntField(pk=True)
    code_name = fields.TextField()
    user_name = fields.TextField()
    grade = fields.IntField()
    questions: fields.ReverseRelation["Questions"]

    class Meta:
        table = "users"


class Admins(Model):
    user_id = fields.IntField()

    class Meta:
        table = "admins"


class Questions(Model):
    key = fields.TextField(pk=True)
    user_id: fields.ForeignKeyRelation[Active_users] = fields.ForeignKeyField(
        "models.Active_users", related_name='questions')
    question = fields.TextField()

    class Meta:
        table = "questions"


async def run():
    await Tortoise.init(
        db_url="postgres://postgres:1234@localhost:5432/postgres",
        modules={
            "models": ["DB"]
        })
    await Tortoise.generate_schemas()
