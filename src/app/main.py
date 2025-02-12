from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.endpoint import router
from Route import security, pdf_handle

import uvicorn

app = FastAPI(title="AutofillPDF FastAPI App")


# CORS Middleware (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(security.router, prefix="/auth", tags=["Security"])
app.include_router(router)
app.include_router(pdf_handle.router, prefix="/files", tags=["AutoFill PDF"])   
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
