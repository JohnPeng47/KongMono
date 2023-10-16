
from pymongo.results import InsertOneResult

from common import db_conn
from .schema import User


def create_db_user(user: User) -> InsertOneResult:
    # TODO: add try catch here
    res = db_conn.get_collection("users").insert_one(user.dict())
    return res
