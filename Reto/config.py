import os
from dotenv import load_dotenv

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=_env_path)

AGENCIA_API_KEY: str = os.environ.get("AGENCIA_API_KEY", "")

EXTERNAL_API_URL: str = os.environ.get(
    "EXTERNAL_API_URL",
    "https://openlibrary.org/search.json",
)
