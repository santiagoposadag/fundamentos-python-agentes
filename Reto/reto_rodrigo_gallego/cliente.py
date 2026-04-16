"""
cliente.py - Guion de Demostración End-to-End

Este script simula el uso de la API por parte de un operador de la Agencia.
Ejecuta el flujo completo de creación, asignación y completitud de misiones.
"""

import time
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "mi-secreto-de-agencia"  # Debe coincidir con el valor en .env

def headers():
    return {"X-API-KEY": API_KEY}

def print_banner(msg):
    print(f"\n{'='*50}")
    print(f" 🕶️  {msg}")
    print(f"{'='*50}")

def ejecutar_demo():
    print_banner("Iniciando Demostración de la Agencia")

    # 1. Verificar salud del servidor
    print("1. Verificando servidor...")
    res = requests.get(f"{BASE_URL}/")
    print(f"Respuesta: {res.json()}")

    # 2. Crear un Agente (Post con Auth)
    print("\n2. Registrando agente 'Rodrigo'...")
    agente_data = {"nombre": "Rodrigo", "tokens": 150, "rol": "admin"}
    res = requests.post(f"{BASE_URL}/agentes/", json=agente_data, headers=headers())
    print(f"Resultado: {res.status_code} - {res.json()}")

    # 3. Crear una Misión (Post con Auth)
    print("\n3. Creando misión 'Infiltración'...")
    mision_data = {
        "titulo": "Infiltración Alpha",
        "descripcion": "Recuperar microchip en base enemiga",
        "agente_asignado": "Rodrigo",
        "energia_requerida": 40
    }
    res = requests.post(f"{BASE_URL}/misiones/", json=mision_data, headers=headers())
    mision_id = res.json().get("id")
    print(f"ID Misión: {mision_id}")

    # 4. Completar la Misión (Post con Auth)
    print("\n4. Completando misión...")
    res = requests.post(f"{BASE_URL}/misiones/{mision_id}/completar", headers=headers())
    print(f"Resultado: {res.json()}")

    # 5. Consultar Briefing (GET con integración externa)
    print("\n5. Consultando briefing estratégico para 'Rodrigo'...")
    res = requests.get(f"{BASE_URL}/briefing/Rodrigo")
    data = res.json()
    print(f"Agente: {data['agente']['nombre']} (Energía: {data['agente']['tokens']})")
    print(f"Intel Externa: {data['intel_externa']}")
    print(f"Fuente: {data['fuente_externa']}")

    # 6. Mensajería entre agentes
    print("\n6. Enviando mensaje rápido...")
    # Creamos un segundo agente para recibir
    requests.post(f"{BASE_URL}/agentes/", json={"nombre": "Athena", "rol": "invitado"}, headers=headers())
    msg_data = {"remitente": "Rodrigo", "destinatario": "Athena", "contenido": "Misión cumplida, cambio y fuera."}
    requests.post(f"{BASE_URL}/mensajes/", json=msg_data)
    
    # Leemos la bandeja
    res = requests.get(f"{BASE_URL}/mensajes/Athena")
    print(f"Bandeja de Athena: {res.json()}")

if __name__ == "__main__":
    try:
        ejecutar_demo()
    except Exception as e:
        print(f"\n❌ Error en la demo: {e}")
        print("Asegúrate de que uvicorn esté corriendo: 'uvicorn main:app --reload'")
