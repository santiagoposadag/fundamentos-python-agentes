
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000"
API_KEY = os.getenv("AGENCIA_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta AGENCIA_API_KEY en el entorno. Configura tu archivo .env.")
HEADERS = {"Content-Type": "application/json", "X-API-KEY": API_KEY}
REQUEST_TIMEOUT = 10

AGENTE = {
    "nombre": "AgenteDemo",
    "rol": "operativo",
    "energia": 100
}

MISION = {
    "titulo": "Misión Demo",
    "descripcion": "Demostración end-to-end",
    "agente_asignado": AGENTE["nombre"],
    "energia_requerida": 10,
    "prioridad": "alta",
    "deadline": "2026-04-30",
    "recompensa": 50
}

MENSAJE = {
    "remitente": AGENTE["nombre"],
    "destinatario": "Admin1",
    "contenido": "¡Misión completada!"
}

def check_server():
    resp = requests.get(f"{API_URL}/", timeout=REQUEST_TIMEOUT)
    print("GET /", resp.status_code, resp.json())

def crear_agente():
    resp = requests.post(
        f"{API_URL}/agentes/",
        json=AGENTE,
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    print("POST /agentes/", resp.status_code, resp.json())

def crear_mision():
    resp = requests.post(
        f"{API_URL}/misiones/", json=MISION, headers=HEADERS, timeout=REQUEST_TIMEOUT
    )
    print("POST /misiones/", resp.status_code, resp.json())
    if resp.status_code in (200, 201):
        return resp.json().get("id")
    return None

def completar_mision(mision_id):
    resp = requests.post(
        f"{API_URL}/misiones/{mision_id}/completar",
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    print(f"POST /misiones/{mision_id}/completar", resp.status_code, resp.json())

def consultar_briefing():
    resp = requests.get(
        f"{API_URL}/briefing/{AGENTE['nombre']}", timeout=REQUEST_TIMEOUT
    )
    print(f"GET /briefing/{AGENTE['nombre']}", resp.status_code, resp.json())

def enviar_mensaje():
    resp = requests.post(
        f"{API_URL}/mensajes/",
        json=MENSAJE,
        headers={"Content-Type": "application/json"},
        timeout=REQUEST_TIMEOUT,
    )
    print("POST /mensajes/", resp.status_code, resp.json())

def leer_bandeja():
    resp = requests.get(
        f"{API_URL}/mensajes/{AGENTE['nombre']}", timeout=REQUEST_TIMEOUT
    )
    print(f"GET /mensajes/{AGENTE['nombre']}", resp.status_code, resp.json())

def main():
    print("== Cliente de demostración end-to-end ==")
    check_server()
    crear_agente()
    mision_id = crear_mision()
    if mision_id:
        completar_mision(mision_id)
    consultar_briefing()
    enviar_mensaje()
    leer_bandeja()

if __name__ == "__main__":
    main()
