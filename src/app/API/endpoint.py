from fastapi import APIRouter

router = APIRouter()

@router.get("/chat/")
async def chat(prompt: str):
    response = "Hello, I am a chatbot. You said: " + prompt
    return {"response": response}