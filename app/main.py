from fastapi import FastAPI
from .routes import moderation
from .routes import guild
from .routes import auth

api = FastAPI()

api.include_router(moderation.router)
api.include_router(guild.router)
api.include_router(auth.router)

@api.get("/")
async def root():
  return {"message": "Welcome to the Text Moderation API"}