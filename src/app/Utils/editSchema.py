import json
import logging
from Model.Pydantic_model import *
from typing import Dict, Any
def generate_modified_schema(base_model, custom_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a modified schema for a given base model based on user-defined modifications.
    
    :param base_model: The base model class to generate schema from.
    :param custom_schema: Dictionary containing properties to modify the base and container schema.
    :return: Modified base schema.
    """
    try:
        # Generate base and container schema
        base_schema = base_model.model_json_schema()
        container_schema = Container.model_json_schema()

        # Modify container schema if custom properties exist
        if custom_schema:
            container_schema["properties"].update(custom_schema.get("container_properties", {}))

            # Remove specified fields from Container schema
            for field in custom_schema.get("remove_container_fields", []):
                container_schema["properties"].pop(field, None)

        # Integrate modified container schema into base schema
        if "jobContainers" in base_schema.get("properties", {}):
            base_schema["properties"]["jobContainers"]["items"] = container_schema

        # Remove unsupported `additionalProperties` (for Gemini compatibility)
        base_schema.pop("additionalProperties", None)
        container_schema.pop("additionalProperties", None)

        # Modify base schema properties if custom properties exist
        if custom_schema:
            base_schema["properties"].update(custom_schema.get("properties", {}))

            # Remove specified fields from the base schema
            for field in custom_schema.get("remove_fields", []):
                base_schema["properties"].pop(field, None)

        return base_schema

    except Exception as e:
        logging.error(f"Error in generate_modified_schema: {e}", exc_info=True)
        return {}

def modify_schema(custom_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modifies the BaseTransportJobInformation schema based on user-defined modifications.
    """
    return generate_modified_schema(TypicalTransportJobInformation, custom_schema)

def modify_schema_import(custom_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modifies the ImportJobInformation schema based on user-defined modifications.
    """
    return generate_modified_schema(ImportJobInformation, custom_schema)

def modify_schema_export(custom_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modifies the ExportJobInformation schema based on user-defined modifications.
    """
    return generate_modified_schema(ExportJobInformation, custom_schema)