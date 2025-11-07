from app.dependencies import get_model, get_tokenizer
from fastapi import APIRouter
from pydantic import BaseModel

class ModerationRequest(BaseModel):
  input_text: str

router = APIRouter()

@router.post("/moderate", tags=["moderation"])
async def moderate_text(item: ModerationRequest):
  model = get_model()
  tokenizer = get_tokenizer()

  # Run the model on the input text
  inputs = tokenizer(item.input_text, return_tensors="pt")
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

  # Prepare the response
  response = [{"label": label, "probability": float(probability)} for label, probability in label_prob_pairs]

  return {"results": response}