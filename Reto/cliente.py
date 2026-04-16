"""
cliente.py — Guion de demostración end-to-end de La Agencia de Agentes.

Ejecutar con el servidor corriendo:
    uvicorn main:app --reload
    python cliente.py
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"
HEADERS = {"X-API-KEY": os.getenv("AGENCIA_API_KEY", "")}


def separador(titulo: str) -> None:
    print(f"\n{'─' * 50}")
    print(f"  {titulo}")
    print(f"{'─' * 50}")


# ─── Paso 1: Verificar que el servidor está vivo ──────────────────────────────
separador("PASO 1 — Verificar servidor")
resp = requests.get(f"{BASE_URL}/")
print(f"Status: {resp.status_code} | {resp.json()}")


# ─── Paso 2: Crear agentes ────────────────────────────────────────────────────
separador("PASO 2 — Crear agentes")

agentes = [
    {"nombre": "Orion", "rol": "admin", "energia": 150},
    {"nombre": "Nova", "rol": "explorador", "energia": 100},
    {"nombre": "Vega", "rol": "estratega", "energia": 120},
]

for agente in agentes:
    resp = requests.post(f"{BASE_URL}/agentes/", json=agente, headers=HEADERS)
    print(f"  [{resp.status_code}] {agente['nombre']}: {resp.json()}")


# ─── Paso 3: Crear misiones ───────────────────────────────────────────────────
separador("PASO 3 — Crear misiones")

misiones = [
    {
        "titulo": "Reconocimiento Sector Alfa",
        "descripcion": "Explorar el perímetro norte y reportar actividad.",
        "agente_asignado": "Nova",
        "estado": "pendiente",
        "energia_requerida": 20,
        "prioridad": "alta",
    },
    {
        "titulo": "Análisis de Datos Interceptados",
        "descripcion": "Procesar logs capturados en la operación anterior.",
        "agente_asignado": "Vega",
        "estado": "en_curso",
        "energia_requerida": 30,
        "prioridad": "media",
    },
    {
        "titulo": "Briefing de Alto Mando",
        "descripcion": "Preparar informe ejecutivo para el consejo.",
        "agente_asignado": "Orion",
        "estado": "pendiente",
        "energia_requerida": 15,
        "prioridad": "baja",
    },
]

ids_misiones = []
for mision in misiones:
    resp = requests.post(f"{BASE_URL}/misiones/", json=mision, headers=HEADERS)
    data = resp.json()
    ids_misiones.append(data.get("id"))
    print(f"  [{resp.status_code}] {mision['titulo']}: {data}")


# ─── Paso 4: Completar primera misión ────────────────────────────────────────
separador("PASO 4 — Completar misión")
id_completar = ids_misiones[0]
resp = requests.post(f"{BASE_URL}/misiones/{id_completar}/completar", headers=HEADERS)
print(f"  [{resp.status_code}] Misión #{id_completar}: {resp.json()}")


# ─── Paso 5: Briefing del agente ─────────────────────────────────────────────
separador("PASO 5 — Briefing de agente")
resp = requests.get(f"{BASE_URL}/briefing/Orion")
data = resp.json()
print(f"  [{resp.status_code}] Agente: {data['agente']}")
print(f"  Consejo de misión: {data['consejo_de_mision']}")
print(f"  Fuente externa: {data['fuente_externa']}")


# ─── Paso 6: Mensajes entre agentes ──────────────────────────────────────────
separador("PASO 6 — Mensajes")

mensajes = [
    {"remitente": "Orion", "destinatario": "Nova", "contenido": "¿Listo para el reconocimiento?"},
    {"remitente": "Nova", "destinatario": "Orion", "contenido": "Afirmativo. Salgo en 5 minutos."},
    {"remitente": "Vega", "destinatario": "Orion", "contenido": "Datos procesados. Adjunto informe."},
    {"remitente": "Orion", "destinatario": "Vega", "contenido": "Recibido. Excelente trabajo."},
    {"remitente": "Nova", "destinatario": "Vega", "contenido": "Sector norte despejado."},
]

for msg in mensajes:
    resp = requests.post(f"{BASE_URL}/mensajes/", json=msg)
    print(f"  [{resp.status_code}] {msg['remitente']} → {msg['destinatario']}: OK")

print()
resp = requests.get(f"{BASE_URL}/mensajes/Orion")
bandeja = resp.json()
print(f"  Bandeja de Orion ({len(bandeja)} mensajes):")
for m in bandeja:
    print(f"    [{m['timestamp']}] {m['remitente']}: {m['contenido']}")

separador("DEMO COMPLETADA")
print("  Circuito end-to-end ejecutado sin errores.")
