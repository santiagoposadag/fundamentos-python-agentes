import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = "http://localhost:8000"
API_KEY = os.getenv("AGENCIA_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta AGENCIA_API_KEY en el entorno. Configura tu archivo .env.")
REQUEST_TIMEOUT = 10

HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY,
}

print("--- GET / ---")
print(requests.get(BASE + "/", timeout=REQUEST_TIMEOUT).json())

print("\n--- POST /agentes/ ---")
agente = {"nombre": "Atlas", "rol": "admin", "energia": 100}
r = requests.post(BASE + "/agentes/", json=agente, headers=HEADERS, timeout=REQUEST_TIMEOUT)
print(r.json())

print("\n--- POST /misiones/ ---")
mision = {
    "titulo": "Demo",
    "descripcion": "Prueba de misión",
    "agente_asignado": "Atlas",
    "energia_requerida": 10
}
r = requests.post(BASE + "/misiones/", json=mision, headers=HEADERS, timeout=REQUEST_TIMEOUT)
print(r.json())

print("\n--- GET /agente/Atlas ---")
print(requests.get(BASE + "/agente/Atlas", timeout=REQUEST_TIMEOUT).json())

print("\n--- GET /agente/Atlas/misiones ---")
print(requests.get(BASE + "/agente/Atlas/misiones", timeout=REQUEST_TIMEOUT).json())
