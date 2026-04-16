from dotenv import load_dotenv
import os

load_dotenv()

API_KEY: str = os.getenv("AGENCIA_API_KEY", "")
EXTERNAL_API_URL: str = os.getenv(
    "EXTERNAL_API_URL", "https://api.adviceslip.com/advice"
)
