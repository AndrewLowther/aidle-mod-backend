from app.dependencies import get_db
from fastapi import APIRouter
from pydantic import BaseModel

class GuildCreateRequest(BaseModel):
  owner_id: int
  owner_name: str | None = None
  owner_icon: str | None = None
  guild_name: str
  guild_id: int
  guild_icon: str | None = None
  moderate: bool = True

router = APIRouter()

@router.post("/guild", tags=["guild"])
async def create_guild(item: GuildCreateRequest):
  print("Received guild creation request:", item)
  db = await get_db()

  # Check if user exists
  user = await db.user.find_unique(where={"owner_id": item.owner_id})
  print("Found user:", user)

  if not user:
    print("User not found, creating new user.")
    # Create new user
    user = await db.user.create(
      data={
        "owner_id": item.owner_id,
        "owner_name": item.owner_name,
        "owner_icon": item.owner_icon
      }
    )

  print("Using user:", user)
  # Create new guild
  guild = await db.guild.create(
    data={
      "guild_name": item.guild_name,
      "guild_id": item.guild_id,
      "guild_icon": item.guild_icon,
      "moderate": item.moderate,
      "owner_id": user.owner_id
    }
  )

  print("Created guild:", guild)

  await db.disconnect()

  return {"status": "success", "guild_id": guild.guild_id}

@router.delete("/guild/{guild_id}", tags=["guild"])
async def delete_guild(guild_id: int):
  db = await get_db()

  # Delete guild
  deleted_guild = await db.guild.delete(
    where={"guild_id": guild_id}
  )

  await db.disconnect()

  return {"status": "success", "deleted_guild_id": deleted_guild.guild_id}