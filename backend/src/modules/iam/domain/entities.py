from beanie import Document
from pydantic import EmailStr
from pymongo.collation import Collation


class User(Document):
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    class Settings:
        collection = "users"
        email_collation = Collation(locale="en", strength=2)
