import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from starlette.staticfiles import StaticFiles
from fastapi_signals import TaskMiddleware

from apps import api_router
from fastapi_product.core.cache import redis_conn
from fastapi_product.core.config import settings, Settings
from contextvars import ContextVar


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_conn.get(jti)
    return entry and entry == 'true'


def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        version="1.0",
        debug=settings.DEBUG
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(TaskMiddleware)
    return _app


app = get_application()
request_id_contextvar = ContextVar("request_id", default=None)

static_path = os.path.join(f"{settings.STATIC_PATH}/static")
if not os.path.exists(static_path):
    os.makedirs(static_path)
media_path = os.path.join(f"{settings.MEDIA_PATH}/media")
if not os.path.exists(media_path):
    os.makedirs(media_path)

app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/media", StaticFiles(directory=media_path), name="media")


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(api_router)
