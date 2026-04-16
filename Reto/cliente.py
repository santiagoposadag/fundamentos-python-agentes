import requests
import json
from config import AGENCIA_API_KEY

BASE_URL = "http://localhost:8000"
HEADERS = {"X-API-KEY": AGENCIA_API_KEY}

def mostrar_paso(titulo):
    print(f"\n{'='*50}")
    print(f" PASO: {titulo}")
    print(f"{'='*50}")

def demo_agencia():
    mostrar_paso("Verificando estado del servidor...")
    try:
        res = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {res.status_code}")
        print(res.json())
    except Exception as e:
        print(f"Error: No se pudo conectar al servidor. ¿Está corriendo uvicorn?\n{e}")
        return

    mostrar_paso("Creando Agente Admin 'Neo'...")
    agente_data = {"nombre": "Neo", "rol": "admin", "energia": 200}
    res = requests.post(f"{BASE_URL}/agentes/", json=agente_data, headers=HEADERS)
    print(res.json())

    mostrar_paso("Creando Agente 'Trinity'...")
    agente_data = {"nombre": "Trinity", "rol": "operadora", "energia": 100}
    res = requests.post(f"{BASE_URL}/agentes/", json=agente_data, headers=HEADERS)
    print(res.json())

    mostrar_paso("Asignando misión a Neo...")
    mision_data = {
        "titulo": "Rescate en el edificio",
        "descripcion": "Extraer al rehén antes de la llegada de los agentes.",
        "agente_asignado": "Neo",
        "energia_requerida": 50,
        "prioridad": "alta"
    }
    res = requests.post(f"{BASE_URL}/misiones/", json=mision_data, headers=HEADERS)
    mision_res = res.json()
    print(mision_res)
    mision_id = mision_res.get("id")

    if mision_id:
        mostrar_paso(f"Completando misión ID {mision_id}...")
        res = requests.post(f"{BASE_URL}/misiones/{mision_id}/completar", headers=HEADERS)
        print(json.dumps(res.json(), indent=2))

    mostrar_paso("Consultando Briefing de Neo...")
    res = requests.get(f"{BASE_URL}/briefing/Neo")
    print(json.dumps(res.json(), indent=2))

    mostrar_paso("Neo envía mensaje a Trinity...")
    msg_data = {
        "remitente": "Neo",
        "destinatario": "Trinity",
        "contenido": "Misión cumplida. ¿Cuál es el siguiente paso?"
    }
    res = requests.post(f"{BASE_URL}/mensajes/", json=msg_data, headers=HEADERS)
    print(res.json())

    mostrar_paso("Trinity revisa su bandeja...")
    res = requests.get(f"{BASE_URL}/mensajes/Trinity")
    mensajes = res.json()
    for m in mensajes:
        print(f"[{m['timestamp']}] {m['remitente']}: {m['contenido']}")

if __name__ == "__main__":
    demo_agencia()
