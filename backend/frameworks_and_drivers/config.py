# frameworks_and_drivers/config.py

import os
from dotenv import load_dotenv

load_dotenv()

FASTTEXT_MODEL_PATH = os.getenv("FASTTEXT_MODEL_PATH")