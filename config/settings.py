import os
from dotenv import load_dotenv
from huggingface_hub import login

load_dotenv()

MODEL_SIZE = os.getenv("MODEL_SIZE", "large")
LANGUAGE = os.getenv("LANGUAGE", "pl")


HF_TOKEN = os.getenv("HF_TOKEN", None)

if HF_TOKEN:
    login(token=HF_TOKEN)