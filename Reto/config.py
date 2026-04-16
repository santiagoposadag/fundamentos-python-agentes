import os
from dotenv import load_dotenv

# Cargar variables desde .env
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env"))

AGENCIA_API_KEY = os.getenv("AGENCIA_API_KEY", "agencia_secreta_123")
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://catfact.ninja/fact")
