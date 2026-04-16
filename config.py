# config.py
# Lee las variables del archivo .env y las deja disponibles para el proyecto.
# Asi evitamos escribir claves directamente en el codigo.

import os
from dotenv import load_dotenv

# load_dotenv() carga el archivo .env para que os.getenv() las pueda leer
load_dotenv()

AGENCIA_API_KEY = os.getenv("AGENCIA_API_KEY", "")
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://restcountries.com/v3.1")
DB_PATH = os.getenv("DB_PATH", "agentes.db")
