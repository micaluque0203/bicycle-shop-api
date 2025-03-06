from fastapi_users import BaseUserManager, FastAPIUsers

from modules.iam.domain.entities import User
from modules.iam.infrastructure.models import UserCreate, UserDB, UserRead


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB

    def on_after_register(self, user: UserDB, request: Request):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserDB, token: str, request: Request
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: UserDB, token: str, request: Request):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> UserDB:
        await self.validate_password(user_create.password, user_create)
        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user:
            raise Exception  # UserAlreadyExists()
        user_dict = user_create.model_dump()
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
        if safe:
            user_dict.pop("is_superuser", None)
            user_dict.pop("is_verified", None)
        user = self.user_db_model(**user_dict)
        print("USER", user)
        user.is_superuser = True
        created = await self.user_db_model.create(user)
        print("USER", created)
        self.on_after_register(user, request)
        return user.model_dump()

    async def get_current_user(self, user: User = Depends(get_current_user)):
        user_dict = user.model_dump()  # Convert User instance to dictionary
        user_read = UserRead(**user_dict)  # Validate and create UserRead instance
        return user_read

    async def authenticate(self, credentials):
        user = await self.user_db.get_by_email(credentials.username)
        if user is None or not verify_password(
            credentials.password, user.hashed_password
        ):
            return None
        return user

    @staticmethod
    def parse_id(user_id: str) -> ObjectId:
        return ObjectId(user_id)
