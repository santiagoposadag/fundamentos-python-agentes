import sys
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "http://localhost:8000"
API_KEY = os.getenv("AGENCIA_API_KEY", "")

if not API_KEY:
    print("[ERROR] AGENCIA_API_KEY no está configurada. Crea el archivo .env con esa variable.")
    sys.exit(1)

HEADERS_AUTH = {"X-API-KEY": API_KEY}


def separador(titulo: str) -> None:
    print(f"\n{'='*55}")
    print(f"  {titulo}")
    print(f"{'='*55}")


# ──────────────────────────────────────────────
# PASO 1: Verificar que el servidor está vivo
# ──────────────────────────────────────────────
separador("PASO 1 — Estado del servidor")
resp = requests.get(f"{BASE_URL}/")
resp.raise_for_status()
print(f"  Servidor: {resp.json()}")

# ──────────────────────────────────────────────
# PASO 2: Registrar un agente (con autenticación)
# ──────────────────────────────────────────────
separador("PASO 2 — Registrar agente 'Orion'")
nuevo_agente = {"nombre": "Orion", "rol": "estratega", "energia": 200}
resp = requests.post(f"{BASE_URL}/agentes/", json=nuevo_agente, headers=HEADERS_AUTH)
print(f"  POST /agentes/ → {resp.status_code}: {resp.json()}")

# Verificar que el agente existe
resp = requests.get(f"{BASE_URL}/agente/Orion")
resp.raise_for_status()
print(f"  GET /agente/Orion → {resp.json()}")

# ──────────────────────────────────────────────
# PASO 3: Crear una misión asignada a Orion (con autenticación)
# ──────────────────────────────────────────────
separador("PASO 3 — Crear misión para Orion")
nueva_mision = {
    "titulo": "Infiltración en Sector 7",
    "descripcion": "Recuperar datos clasificados del laboratorio secreto.",
    "agente_asignado": "Orion",
    "estado": "pendiente",
    "energia_requerida": 50,
    "prioridad": "alta",
    "recompensa": 20,
    "creado_por": "cliente_demo",
}
resp = requests.post(f"{BASE_URL}/misiones/", json=nueva_mision, headers=HEADERS_AUTH)
resp.raise_for_status()
resultado_mision = resp.json()
mision_id = resultado_mision["id"]
print(f"  POST /misiones/ → {resp.status_code}: {resultado_mision}")

# Consultar la misión recién creada
resp = requests.get(f"{BASE_URL}/misiones/{mision_id}")
resp.raise_for_status()
print(f"  GET /misiones/{mision_id} → {resp.json()}")

# ──────────────────────────────────────────────
# PASO 4: Completar la misión (con autenticación)
# ──────────────────────────────────────────────
separador(f"PASO 4 — Completar misión id={mision_id}")
resp = requests.post(
    f"{BASE_URL}/misiones/{mision_id}/completar", headers=HEADERS_AUTH
)
resp.raise_for_status()
completado = resp.json()
print(f"  POST /misiones/{mision_id}/completar → {resp.status_code}")
print(f"  Mensaje    : {completado['mensaje']}")
print(f"  Es admin   : {completado['es_admin']}")
print(f"  Resultado  : {completado['resultado_clase']}")
print(f"  Energía    : {completado['energia_restante']}")

# ──────────────────────────────────────────────
# PASO 5: Obtener el briefing del agente
# ──────────────────────────────────────────────
separador("PASO 5 — Briefing de Orion")
resp = requests.get(f"{BASE_URL}/briefing/Orion")
resp.raise_for_status()
briefing = resp.json()
print(f"  Agente           : {briefing['agente']}")
print(f"  Misiones totales : {briefing['misiones_asignadas']}")
print(f"  Inteligencia     : {briefing['inteligencia_externa']}")
print(f"  Fuente           : {briefing['fuente_externa']}")

# ──────────────────────────────────────────────
# PASO 6: Enviar mensajes y leer la bandeja
# ──────────────────────────────────────────────
separador("PASO 6 — Mensajería entre agentes")

# Asegurarse de que existe un segundo agente receptor
resp = requests.post(
    f"{BASE_URL}/agentes/",
    json={"nombre": "Atlas", "rol": "explorador", "energia": 150},
    headers=HEADERS_AUTH,
)
print(f"  Registrar Atlas → {resp.status_code}: {resp.json()}")

# Enviar mensajes de Orion a Atlas
for contenido in [
    "Misión completada. Sector 7 asegurado.",
    "Solicito extracción inmediata.",
]:
    resp = requests.post(
        f"{BASE_URL}/mensajes/",
        json={"remitente": "Orion", "destinatario": "Atlas", "contenido": contenido},
        headers=HEADERS_AUTH,
    )
    print(f"  POST /mensajes/ → {resp.status_code}: {resp.json()}")

# Leer bandeja de Atlas
resp = requests.get(f"{BASE_URL}/mensajes/Atlas")
resp.raise_for_status()
mensajes = resp.json()
print(f"\n  --- Bandeja de Atlas ({len(mensajes)} mensajes) ---")
for msg in mensajes:
    print(f"    [{msg['timestamp']}] {msg['remitente']} → {msg['contenido']}")

# ──────────────────────────────────────────────
# DEMOSTRACIÓN DE RECHAZO SIN API KEY
# ──────────────────────────────────────────────
separador("EXTRA — Verificar que 401 se activa sin API key")
resp = requests.post(f"{BASE_URL}/misiones/", json=nueva_mision)
print(f"  POST /misiones/ sin X-API-KEY → {resp.status_code}: {resp.json()}")

separador("FIN DEL DEMO — Circuito completo exitoso")
print("  Abre http://localhost:8000/docs para explorar todos los endpoints.\n")
