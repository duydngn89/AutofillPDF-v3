import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(key: str):
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Missing environment variable: {key}")
    return value
