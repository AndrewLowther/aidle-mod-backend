from transformers import AutoModelForSequenceClassification, AutoTokenizer
from prisma import Prisma

model = AutoModelForSequenceClassification.from_pretrained("KoalaAI/Text-Moderation")
tokenizer = AutoTokenizer.from_pretrained("KoalaAI/Text-Moderation")

def get_model():
  return model

def get_tokenizer():
  return tokenizer

async def get_db():
  db = Prisma()
  await db.connect()
  return db