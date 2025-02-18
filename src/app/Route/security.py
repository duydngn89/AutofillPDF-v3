from Utils.security import verify_token
from typing import Dict
from fastapi import APIRouter, Depends
import jwt
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from Utils.security import create_access_token
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
import os

load_dotenv()
password=os.getenv("PASSWORD")


reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

router = APIRouter()


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token."""
    # Dummy authentication (Replace with actual user verification)
    if form_data.username != "demo_test" or form_data.password != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected",dependencies=[Depends(reusable_oauth2)])
def protected_route():
    """A protected route that requires authentication."""
    return {"message": "This is a protected route", "user": "hello"}