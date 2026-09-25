from fastapi import FastAPI
import models
from database import engine
from app.routers import auth_router, user_router, friend_router, group_router, group_member_router, message_router, status_content_router

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(friend_router.router)
app.include_router(group_router.router)
app.include_router(group_member_router.router)
app.include_router(message_router.router)
app.include_router(status_content_router.router)