import asyncio
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.dependencies.auth import auth_backend, fastapi_users
from api.infrastructure.client import get_mongodb, mongodb_instance
from api.routers.cart import router as cart_router
from api.routers.parts import router as parts_router
from api.routers.products import router as products_router
from api.routers.rules import router as rules_router
from modules.iam.infrastructure.models import User, UserCreate, UserRead, UserUpdate

origins = ["http://localhost:5174", "http://127.0.0.1:3000", "http://0.0.0.0:5173"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def start_db():
        async with mongodb_instance as db:
            await db.init_db()

    asyncio.create_task(start_db())
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(User, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(products_router, tags=["products"])
app.include_router(cart_router, tags=["cart"])
app.include_router(parts_router, tags=["parts"])
app.include_router(rules_router, tags=["rules"])
