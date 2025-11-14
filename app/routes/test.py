from app.dependencies import get_db, get_model, get_tokenizer
import jwt
import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request

load_dotenv()
router = APIRouter()

@router.get('/test', tags=['test'])
async def get_me(test_string: str, guild_id: str, request: Request):
  auth_header = request.headers.get(os.getenv('USER_COOKIE_NAME'))
  if not auth_header:
    raise HTTPException(status_code=401, detail="Authorization header missing")

  db = await get_db()

  token = jwt.decode(auth_header, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])

  user = await db.user.find_unique(
    where={
      "owner_id": token["user_id"]
    }
  )

  settings = await db.settings.find_unique(
    where={
      "guild_id": guild_id
    }
  )

  if not user:
    raise HTTPException(status_code=401, detail="User not found")
  
  model = get_model()
  tokenizer = get_tokenizer()

  # Run the model on the input text
  inputs = tokenizer(test_string, return_tensors="pt")
  outputs = model(**inputs)

  # Get the predicted logits
  logits = outputs.logits

  # Apply softmax to get probabilities (scores)
  probabilities = logits.softmax(dim=-1).squeeze()

  # Retrieve the labels
  id2label = model.config.id2label
  labels = [id2label[idx] for idx in range(len(probabilities))]

  # Combine labels and probabilities, then sort
  label_prob_pairs = list(zip(labels, probabilities))
  label_prob_pairs.sort(key=lambda item: item[1], reverse=True) 

  total_probability = 0
  simpleSettings = {
    "enable_ok": False,
    "enable_h": settings.enable_h,
    "enable_v": settings.enable_v,
    "enable_s": settings.enable_s,
    "enable_h2": settings.enable_h2,
    "enable_v2": settings.enable_v2,
    "enable_s3": settings.enable_s3,
    "enable_hr": settings.enable_hr,
    "enable_sh": settings.enable_sh,
  }
  confidence_limit = settings.confidence_limit
  for label, probability in label_prob_pairs:
    if label != "OK" and simpleSettings["enable_" + label.lower()] == True:
      total_probability += float(probability)

  # Prepare the response
  response = [{"label": label, "probability": float(probability)} for label, probability in label_prob_pairs]

  return {
    "results": response,
    "moderate": True if total_probability >= (confidence_limit / 100) else False,
    "moderation_message": settings.moderation_message,
    "total_probability": total_probability
  }

  return response