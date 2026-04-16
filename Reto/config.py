
"""
config.py — Carga de variables de entorno

Utiliza python-dotenv para cargar variables desde .env
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

def get_env_variable(key: str, default=None):
    """Devuelve el valor de una variable de entorno o el valor por defecto si no existe."""
    return os.getenv(key, default)
