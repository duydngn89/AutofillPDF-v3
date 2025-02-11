from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.endpoint import router
from Route import pdf_handle
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

import uvicorn

app = FastAPI(title="AutofillPDF FastAPI App")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# CORS Middleware (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(pdf_handle.router, prefix="/files", tags=["AutoFill PDF"])   
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
