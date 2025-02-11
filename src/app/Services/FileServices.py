import os
import shutil
from fastapi import UploadFile, File, HTTPException
from dotenv import load_dotenv
from Utils.pdfToImage import *
from Services.LLMservices import *
import logging
from google.genai import types
logging.basicConfig(level=logging.DEBUG)
# Load environment variables
load_dotenv()

async def save_file(file: UploadFile):
    """Save a file to the server."""
    try:
        with open(f"{os.getenv('UPLOAD_FOLDER')}/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def handle_file_service(user_prompt: str,file: UploadFile, custom_schema: Optional[dict]=None):
    """Handle a PDF file and return the Gemini response."""
    try:
        logging.debug(f"Received PDF file: {file.filename}")  # Debugging log
        pdf_bytes = await file.read()
        logging.debug(f"Received {len(pdf_bytes)} bytes from uploaded PDF.")  # Debugging log
        base64_images = await pdf_to_parts(pdf_bytes)
        

        system_prompt = """You are an assistant who will extract structured transport job details from the following images which converted from 1 file pdf. Please strictly satisfy the following requirements: 
                Note 1(Very Important): If multiple containers are present,  MUST structure them as a list and correctly map their details to the schema.
                Note 2: If UNLOCODE port of loading and discharge are not explicitly defined, the value will be infered from the discharge port.
                """
        # Send the request to Gemini
        result = await call_gemini_llm(system_prompt, user_prompt, base64_images, custom_schema)

        return {"aiAgent_response": result}
    except Exception as e:
        logging.error(f"Error in handle_file: {e}", exc_info=True)
        return {"error": str(e)}