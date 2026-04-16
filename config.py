import os
from dotenv import load_dotenv

load_dotenv()

# Clave maestra que deben enviar los clientes en el header X-API-KEY para
# acceder a los endpoints de escritura protegidos.
AGENCIA_API_KEY: str = os.getenv("AGENCIA_API_KEY", "")

# URL de la API pública externa usada en el briefing de agentes.
# Por defecto apunta a Advice Slip (consejos estratégicos, sin autenticación).
EXTERNAL_API_URL: str = os.getenv("EXTERNAL_API_URL", "https://api.adviceslip.com/advice")
