import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Body, Depends
from typing import Optional
import os
from dotenv import load_dotenv
from Services.FileServices import handle_file_service
from Model.Pydantic_model import *
from fastapi.security import HTTPBearer
from Utils.editSchema import *
import logging
import json



router = APIRouter()

# Load environment variables
load_dotenv()
INPUT_FOLDER = os.getenv("UPLOAD_FOLDER")


#Default schema for the input of API
DEFAULT_SCHEMA = {
    "properties": {
        "newField": {
            "type": "string",
            "description": "Example additional field."
        }
    },
    "remove_fields": ["newField"],
    "container_properties": {
        "extraField": {
            "type": "string",
            "description": "Example extra field for container."
        }
    },
    "remove_container_fields": ["extraField"]
}
reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


@router.get("/dump_schema/")
async def dump_schema():
    """Dump the default JSON schema to a file."""
    try:
        base_schema=TypicalTransportJobInformation.model_json_schema()
        container_schema = Container.model_json_schema()
        #add container schema to base schema
        base_schema["properties"]["jobContainers"]["items"] = container_schema

        ##Hot fix: remove additionalProperties from schema because the template of Gemini does not support it
        base_schema.pop("additionalProperties", None)
        container_schema.pop("additionalProperties", None)

        #Dump schema to json
        with open("schema.json", "w") as f:
            json.dump(base_schema, f)
        return {"message": "Schema dumped to schema.json"}
    except Exception as e:
        logging.error(f"Error in dump_schema: {e}", exc_info=True)
        return {"error": str(e)}

@router.post("/handle_file",dependencies=[Depends(reusable_oauth2)])
async def handle_file(
    file: UploadFile = File(...),
    prompt: Optional[str] = Body("", description="Optional prompt to display to the user."),
    custom_schema: Optional[str] = Body(
        DEFAULT_SCHEMA,
        description="Optional custom JSON schema to override defaults. "
                    "This allows adding or removing fields from the default schema."
    )
):
    """Handle a PDF file and optionally override the default response schema."""
    try:

        custom_schema = json.loads(custom_schema) if custom_schema else None

        user_prompt = prompt
        response_schema = modify_schema(custom_schema)
        if  response_schema is None:
            raise ValueError("Schema modification failed.")
       
        result = await handle_file_service(user_prompt,file, custom_schema= response_schema)
      
        return result
    except Exception as e:
        logging.error(f"Error in handle_file: {e}", exc_info=True)
        return {"error": str(e)}


@router.post("/handle_file/import",dependencies=[Depends(reusable_oauth2)])
async def handle_file_import(
    file: UploadFile = File(...),
    prompt: Optional[str] = Body("", description="Optional prompt to display to the user."),
    custom_schema: Optional[str] = Body(
        DEFAULT_SCHEMA,
        description="Optional custom JSON schema to override defaults. "
                    "This allows adding or removing fields from the default schema."
    )
):
    """Handle a PDF file and optionally override the default response schema."""
    try:

        custom_schema = json.loads(custom_schema) if custom_schema else None

        user_prompt = prompt
        response_schema = modify_schema_import(custom_schema)
        if  response_schema is None:
            raise ValueError("Schema modification failed.")

        #Handle the file
        result = await handle_file_service(user_prompt,file, custom_schema= response_schema)


        #Remove white space from the response
        result["aiAgent_response"]["unilocoPortOfDischarge"] = result["aiAgent_response"]["unilocoPortOfDischarge"].replace(" ", "")
        result["aiAgent_response"]["unilocoPortOfLoading"] = result["aiAgent_response"]["unilocoPortOfLoading"].replace(" ", "")
        
        return result
    except Exception as e:
        logging.error(f"Error in handle_file: {e}", exc_info=True)
        return {"error": str(e)}


@router.post("/handle_file/export",dependencies=[Depends(reusable_oauth2)])
async def handle_file_export(
    file: UploadFile = File(...),
    prompt: Optional[str] = Body("", description="Optional prompt to display to the user."),
    custom_schema: Optional[str] = Body(
        DEFAULT_SCHEMA,
        description="Optional custom JSON schema to override defaults. "
                    "This allows adding or removing fields from the default schema."
    )
):
    """Handle a PDF file and optionally override the default response schema."""
    try:

        custom_schema = json.loads(custom_schema) if custom_schema else None

        user_prompt = prompt
        response_schema = modify_schema_export(custom_schema)
        if  response_schema is None:
            raise ValueError("Schema modification failed.")

        #Handle the file
        result = await handle_file_service(user_prompt,file, custom_schema= response_schema)


        #Remove white space from the response
        result["aiAgent_response"]["unilocoPortOfDischarge"] = result["aiAgent_response"]["unilocoPortOfDischarge"].replace(" ", "")
        result["aiAgent_response"]["unilocoPortOfLoading"] = result["aiAgent_response"]["unilocoPortOfLoading"].replace(" ", "")
        
        return result
    except Exception as e:
        logging.error(f"Error in handle_file: {e}", exc_info=True)
        return {"error": str(e)}