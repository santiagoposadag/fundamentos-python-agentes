"""
config.py - Configuración de Variables de Entorno

Carga los secretos y URLs desde un archivo .env para evitar hardcodear datos sensibles.
"""

import os
from dotenv import load_dotenv

# Cargamos el archivo .env si existe
load_dotenv()

class Settings:
    """Clase principal de configuración."""
    
    # API Key para proteger los endpoints de escritura
    API_KEY: str = os.getenv("AGENCIA_API_KEY", "default-secret-key")
    
    # URL de la API externa para el briefing (Salto 5.2)
    # Por defecto usamos CatFact API (frases de gatos)
    EXTERNAL_API_URL: str = os.getenv(
        "EXTERNAL_API_URL", 
        "https://catfact.ninja/fact"
    )
    
    # Configuración de base de datos
    DATABASE_NAME: str = "agentes.db"

# Instancia para uso global
settings = Settings()
