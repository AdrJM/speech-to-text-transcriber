import os
from dotenv import load_dotenv

load_dotenv()

MODEL_SIZE = os.getenv("MODEL_SIZE", "medium")
LANGUAGE = os.getenv("LANGUAGE", "pl")