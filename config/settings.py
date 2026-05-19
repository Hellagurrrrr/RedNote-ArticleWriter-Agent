import os
import getpass
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not API_KEY:
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")

MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-v4-pro")
BASE_URL = os.getenv("BASE_URL", "https://api.deepseek.com")