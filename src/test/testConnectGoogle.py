import google.generativeai as genai  # ✅ Correct import
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Retrieve API key from .env
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables")

# Configure the Gemini API client
genai.configure(api_key=api_key)

# List available models to confirm the connection
models = genai.list_models()
print("Connected to Google AI models!")
print("Available models:", [model.name for model in models])
