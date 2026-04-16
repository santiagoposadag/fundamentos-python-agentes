# cliente.py
# Script de demostracion que prueba todos los endpoints importantes.
# Para correrlo: python cliente.py (con el servidor uvicorn ya corriendo)

import requests
from config import AGENCIA_API_KEY

BASE_URL = "http://localhost:8000"
HEADERS_AUTH = {"X-API-KEY": AGENCIA_API_KEY}


def separador(titulo):
    print(f"\n{'=' * 55}")
    print(f"  {titulo}")
    print(f"{'=' * 55}")


def verificar_respuesta(respuesta, descripcion):
    print(f"\n>> {descripcion}")
    print(f"  Status: {respuesta.status_code}")
    try:
        print(f"  Body:   {respuesta.json()}")
    except Exception:
        print(f"  Body:   {respuesta.text}")


# --- PASO 1: Ver si el servidor responde ---
separador("PASO 1: Health check")

r = requests.get(f"{BASE_URL}/")
verificar_respuesta(r, "GET /")

if r.status_code != 200:
    print("\n[ERROR] El servidor no responde. Correr: uvicorn main:app --reload")
    exit(1)


# --- PASO 2: Crear un agente nuevo ---
separador("PASO 2: Crear agente 'Orion'")

nuevo_agente = {
    "nombre": "Orion",
    "rol": "explorador",
    "energia": 150
}

r = requests.post(f"{BASE_URL}/agentes/", json=nuevo_agente, headers=HEADERS_AUTH)
verificar_respuesta(r, "POST /agentes/ (con API key)")

# Probamos que sin key nos rechaza con 401
r_sin_key = requests.post(f"{BASE_URL}/agentes/", json=nuevo_agente)
verificar_respuesta(r_sin_key, "POST /agentes/ (sin API key -> debe dar 401)")


# --- PASO 3: Crear una mision para Orion ---
separador("PASO 3: Crear mision para 'Orion'")

nueva_mision = {
    "titulo": "Infiltrar base norte",
    "descripcion": "Acceder al servidor de comunicaciones de la base norte sin ser detectado.",
    "agente_asignado": "Orion",
    "energia_requerida": 30,
    "prioridad": "alta",
    "creado_por": "cliente_demo"
}

r = requests.post(f"{BASE_URL}/misiones/", json=nueva_mision, headers=HEADERS_AUTH)
verificar_respuesta(r, "POST /misiones/ (con API key)")

# Guardamos el ID para usarlo despues
mision_id = None
if r.status_code == 200:
    mision_id = r.json().get("id")
    print(f"\n  [INFO] Mision creada con ID: {mision_id}")


# --- PASO 4: Completar la mision ---
separador("PASO 4: Completar la mision")

if mision_id is not None:
    r = requests.post(f"{BASE_URL}/misiones/{mision_id}/completar", headers=HEADERS_AUTH)
    verificar_respuesta(r, f"POST /misiones/{mision_id}/completar (con API key)")

    r_sin_key = requests.post(f"{BASE_URL}/misiones/{mision_id}/completar")
    verificar_respuesta(r_sin_key, f"POST /misiones/{mision_id}/completar (sin API key -> 401)")
else:
    print("\n  [SKIP] No se obtuvo el ID de la mision.")


# --- PASO 5: Briefing del agente con API externa ---
separador("PASO 5: Briefing de 'Orion'")

r = requests.get(f"{BASE_URL}/briefing/Orion")
verificar_respuesta(r, "GET /briefing/Orion (pais aleatorio)")

r = requests.get(f"{BASE_URL}/briefing/Orion?pais=Colombia")
verificar_respuesta(r, "GET /briefing/Orion?pais=Colombia")


# --- PASO 6: Mensajes entre agentes ---
separador("PASO 6: Mensajes")

mensaje1 = {
    "remitente": "Atlas",
    "destinatario": "Orion",
    "contenido": "Orion, necesito tu reporte de la base norte urgente."
}
r = requests.post(f"{BASE_URL}/mensajes/", json=mensaje1)
verificar_respuesta(r, "POST /mensajes/ (Atlas -> Orion)")

mensaje2 = {
    "remitente": "Orion",
    "destinatario": "Atlas",
    "contenido": "Mision completada. Servidor infiltrado. Enviando datos encriptados."
}
r = requests.post(f"{BASE_URL}/mensajes/", json=mensaje2)
verificar_respuesta(r, "POST /mensajes/ (Orion -> Atlas)")

r = requests.get(f"{BASE_URL}/mensajes/Orion")
verificar_respuesta(r, "GET /mensajes/Orion (bandeja de entrada)")


# --- Resumen final ---
separador("RESUMEN: Estado de Orion")

r = requests.get(f"{BASE_URL}/agente/Orion")
if r.status_code == 200:
    datos = r.json()
    print(f"\n  Nombre:  {datos['nombre']}")
    print(f"  Rol:     {datos['rol']}")
    print(f"  Energia: {datos['energia']}")

r_misiones = requests.get(f"{BASE_URL}/agente/Orion/misiones")
if r_misiones.status_code == 200:
    misiones = r_misiones.json()
    print(f"\n  Misiones de Orion: {len(misiones)}")
    for m in misiones:
        print(f"    - [{m['estado']}] {m['titulo']} (energia requerida: {m['energia_requerida']})")

print("\n\nDemo completada.\n")
