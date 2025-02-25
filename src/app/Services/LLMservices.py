from google import genai
from dotenv import load_dotenv
import os
from typing import List, Dict
from Model.Pydantic_model import *
from google.genai import types
load_dotenv()


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_id="gemini-2.0-flash"


async def call_gemini_llm(system_prompt: str,
                            user_prompt: str,
                           image_parts: List[types.Part],
                           custom_schema: Optional[Dict] = None) -> Dict:
    """
    Send prompt and base64 image URLs to Gemini LLM and return structured response.
    """
    

    contents = [{"role": "user", "parts": [{"text": system_prompt}]}]  # Text part from user

    # Append user prompt
    contents.append({"role": "user", "parts": [{"text": user_prompt}]})

    # Append each base64 image URL
    for part in image_parts:
        contents.append({"role": "user", "parts": [part]})
    
   
    
    response = client.models.generate_content(
        model=model_id,
        contents=contents,
        config={
            "temperature": 0,
            "top_p": 0.95,
            "response_mime_type": "application/json",
            "response_schema":    custom_schema,
        }
    )

    # Convert Gemini response to dictionary
    print(response.usage_metadata)
    output: Dict = response.parsed
    

    return output  


    