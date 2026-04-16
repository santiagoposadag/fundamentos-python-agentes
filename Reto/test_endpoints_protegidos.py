
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000"
API_KEY = os.getenv("AGENCIA_API_KEY", "testkey")
REQUEST_TIMEOUT = 10

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

def test_post_mision():
    data = {
        "titulo": "Misión Test",
        "descripcion": "Prueba automatizada",
        "agente_asignado": "AgenteX",
        "energia_requerida": 10
    }
    resp = requests.post(f"{API_URL}/misiones/", json=data, headers=headers, timeout=REQUEST_TIMEOUT)
    print("POST /misiones/", resp.status_code, resp.json())

def test_post_agente():
    data = {
        "nombre": "AgenteX",
        "rol": "operativo",
        "energia": 100
    }
    resp = requests.post(f"{API_URL}/agentes/", json=data, headers=headers, timeout=REQUEST_TIMEOUT)
    print("POST /agentes/", resp.status_code, resp.json())
    return resp


def test_post_completar_mision(mision_id):
    resp = requests.post(f"{API_URL}/misiones/{mision_id}/completar", headers=headers, timeout=REQUEST_TIMEOUT)
    print(f"POST /misiones/{mision_id}/completar", resp.status_code, resp.json())

def main():
    print("== Prueba de endpoints protegidos ==")
    test_post_mision()

    test_post_agente()

if __name__ == "__main__":
    main()
