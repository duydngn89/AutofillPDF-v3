import os
import shutil
from fastapi import UploadFile, File, HTTPException
from dotenv import load_dotenv
from Utils.pdfToImage import *
from Services.LLMservices import *
import logging
from google.genai import types
import asyncio
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
        

        system_prompt = """You are an assistant who will extract structured transport job details from the following images which converted from 1 file pdf. Please STRICTLY satisfy the <Requirements>.
                <Requirements> 
                - Requirement 1(Very Important): If multiple containers are present,  MUST structure them as a list and correctly map their details to the schema.
                - Requirement 2: If UNLOCODE port of loading and discharge are not explicitly defined, the value will be infered from the discharge port and loading port.
                - Requirement 3: If file has only a weight, it will be considered as the gross weight of the containers.
                </Requirements>
                """
        # Send the request to Gemini
        try:
            result = await asyncio.wait_for(
                call_gemini_llm(system_prompt, user_prompt, base64_images, custom_schema),
                timeout=120  # Set timeout in seconds
            )

            result=str(result)

            verify_prompt ="""You are an assistant who will verify data format of the structured transport job details from this JSON. Please STRICTLY satisfy the <Requirements>.
                <Requirements> 
                - Requirement 1(Very Important):If any field is null, it MUST be keep as null, remain intact, absolutely do not change the null.
                - Requirement 2: Please correct the voyage fields if there are abnormal.
                - Requirement 3:If the field is defined datetime, so Date and time must be in ISO 8601 format. Example: 2022-01-01T00:00:00
                - Requirement 4:If the field is defined date, Date must be in the format YYYY-MM-DD.
                </Requirements>
"""
            result = await asyncio.wait_for(
                call_gemini_llm(verify_prompt, result, None, custom_schema),
                timeout=120  # Set timeout in seconds
            )
        except asyncio.TimeoutError:
            raise TimeoutError("LLM request timed out.")

        return {"aiAgent_response": result}
    
    except TimeoutError as te:
        logging.error(f"Timeout Error in call_gemini_llm: {te}", exc_info=True)
        return {"error": "LLM request timed out."}
    except Exception as e:
        logging.error(f"Error in handle_file: {e}", exc_info=True)
        return {"error": str(e)}