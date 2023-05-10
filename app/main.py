import time
from contextlib import asynccontextmanager

import aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin, ModelView
from starlette.requests import Request

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.Hotels.rooms.router import router as router_rooms
from app.Hotels.router import router as router_app
from app.images.router import router as router_images
from app.pages.router import router  as router_pages
from app.importer.router import router as router_import
from app.users.router import router as router_users
from app.prometheus.router import router as router_prometheus

from app.logger import logger
import sentry_sdk
from fastapi_versioning import VersionedFastAPI, version
from prometheus_fastapi_instrumentator import Instrumentator


@asynccontextmanager
async def lifespan(app: FastAPI):

    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

# Это то же самое   , что и
# @app.on_event("startup")
# def startup():
#     redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="cache")

app = FastAPI(lifespan=lifespan  )

sentry_sdk.init(
    dsn="https://92eac5ee89894ebd98d0681c5c094ff2@o4505142140403712.ingest.sentry.io/4505142145646592",
    traces_sample_rate=1.0,
)






app.include_router(router_users)
app.include_router(router_bookings)

app.include_router(router_app)
app.include_router(router_rooms)

app.include_router(router_pages)


app.include_router(router_images)
app.include_router(router_import)

app.include_router(router_prometheus)




origins = [
    'http://localhost:3000',
    'http://localhost:6379',
]

app.add_middleware(
    CORSMiddleware ,
    allow_origins = origins ,
    allow_credentials = True ,
    allow_methods = ['GET','POST','OPTIONS','DELETE','PATCH',"PUT"],
    allow_headers = ["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Authorization"],
)



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request execution time " , extra={
                'process_time': round(process_time , 4) })
    # response.headers["X-Process-Time"] = str(process_time)
    return response

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    # description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)

admin = Admin(app, engine , authentication_backend=authentication_backend)


admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomAdmin)


app.mount('/static' , StaticFiles(directory='app/static'),'static')

@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

instrumentator = Instrumentator(
    should_group_status_codes=False ,
    excluded_handlers=['.*admin.*','/metrics']
)
instrumentator.instrument(app).expose(app)