from pdf2image import convert_from_path, convert_from_bytes
from io import BytesIO
import base64
from typing import List, Dict
import os
import logging
from google import genai
from google.genai import types

import pathlib
import PIL.Image
logging.basicConfig(level=logging.DEBUG)
def pdf_to_png(pdf_path, output_folder):
    """Convert a PDF file to PNG images (one per page)."""
    images = convert_from_path(pdf_path)  # Convert PDF pages to images
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(image_path, "PNG")
        print(f"Saved: {image_path}")

async def pdf_to_base64(pdf_bytes: bytes) -> List[Dict[str, str]]:
    """Convert a PDF (in bytes) to a list of dictionaries with base64-encoded images."""
    try:
        images = convert_from_bytes(pdf_bytes)  # Convert PDF to images
        logging.debug(f"Converted {len(images)} pages from PDF.")  # Debugging log
        base64_images = []

        for i, image in enumerate(images):
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            base64_images.append({f"image{i + 1}": base64_str})  # Store in dict format
            logging.debug(f"Encoded page {i + 1} as base64.")  # Debugging log

        return base64_images

    except Exception as e:
        logging.error(f"Error in pdf_to_base64: {e}", exc_info=True)
        return []  # Return an empty list instead of failing silently


async def pdf_to_base64_urls(pdf_bytes: bytes) -> List[Dict[str, Dict[str, str]]]:
    """
    Convert a PDF file into a list of base64-encoded image URLs.
    Each dictionary will have an "image_url" key with a "data:image/jpeg;base64,..." value.
    """
    try:
        images = convert_from_bytes(pdf_bytes)
        logging.debug(f"Converted {len(images)} pages from PDF.")

        base64_images = []
        for i, image in enumerate(images):
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")  # Ensure images are JPEG
            base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            base64_images.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_str}"}
            })
            logging.debug(f"Encoded page {i + 1} as base64 URL.")

        return base64_images

    except Exception as e:
        logging.error(f"Error in pdf_to_base64_urls: {e}", exc_info=True)
        return []

async def pdf_to_parts(pdf_bytes: bytes) -> List[types.Part]:
    """
    Convert a PDF file into a list of `Part` objects (image files).
    
    Args:
        pdf_bytes (bytes): The PDF file content as bytes
        
    Returns:
        List[types.Part]: List of Part objects containing the converted images
    """
    try:
        images = convert_from_bytes(pdf_bytes)
        logging.debug(f"Converted {len(images)} pages from PDF.")

        image_parts = []
        for i, image in enumerate(images):
            # Convert PIL Image to bytes
            img_byte_array = BytesIO()
            image.save(img_byte_array, format='PNG')
            img_bytes = img_byte_array.getvalue()
            

            # Create a new Part instance and then call from_bytes
            part = types.Part()
            image_part = part.from_bytes(data=img_bytes, mime_type="image/png")
            image_parts.append(image_part)

            logging.debug(f"Converted page {i + 1} to Part object.")

        return image_parts

    except Exception as e:
        logging.error(f"Error in pdf_to_parts: {e}", exc_info=True)
        return []