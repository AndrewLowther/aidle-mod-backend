import requests
import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

load_dotenv()
router = APIRouter()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

@router.get("/auth", tags=["auth"])
def authenticate(code, redirect_uri):
  data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect_uri
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  try:
    r = requests.post('%s/oauth2/token' % os.getenv('API_ENDPOINT'), data=data, headers=headers, auth=(client_id, client_secret))
    r.raise_for_status()
    return r.json()
  except requests.exceptions.RequestException as e:
    print(f"Error during authentication: {e}")
    raise HTTPException(status_code=500, detail="Authentication failed")