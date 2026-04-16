# Este módulo se encarga de cargar las variables de entorno desde el archivo .env y ponerlas a disposición del resto del programa.

import os
from dotenv import load_dotenv

# Cargamos el archivo .env
load_dotenv()

# Creamos variables que el resto del programa usará
# os.getenv busca el nombre en el .env. Si no lo halla, usa el segundo valor por defecto.
# Es decir, ponemos un valor de respaldo (default) para que el programa no explote.
API_KEY = os.getenv("AGENCIA_API_KEY", "llave-provisional")
API_URL = os.getenv("EXTERNAL_API_URL", "https://google.com")

print("[CONFIG]: Variables de entorno cargadas correctamente.")