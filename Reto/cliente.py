import sys
import requests

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "agencia-super-secreta-2026"
HEADERS_AUTH = {"X-API-KEY": API_KEY}

def titulo(texto: str) -> None:
    linea = "=" * 60
    print(f"\n{linea}")
    print(f"  {texto}")
    print(linea)

def ok(texto: str) -> None:
    print(f"  [OK]  {texto}")

def error(texto: str) -> None:
    print(f"  [ERROR] {texto}")

def dato(clave: str, valor) -> None:
    print(f"  {clave}: {valor}")

def abortar(motivo: str) -> None:
    error(motivo)
    error("El servidor debe estar corriendo. Ejecuta en otra terminal:")
    error("  uvicorn main:app --host 127.0.0.1 --port 8000")
    sys.exit(1)

def paso1_verificar_servidor() -> None:
    titulo("PASO 1 — Verificar que el servidor está vivo")
    try:
        r = requests.get(f"{BASE_URL}/", timeout=3)
        r.raise_for_status()
        ok(f"Servidor online. Respuesta: {r.json()['mensaje']}")
    except requests.exceptions.ConnectionError:
        abortar("No se pudo conectar al servidor en http://127.0.0.1:8000")
    except Exception as exc:
        abortar(f"Error inesperado: {exc}")

def paso2_crear_agentes() -> None:
    titulo("PASO 2 — Crear agentes")

    agentes = [
        {"nombre": "Nova",    "rol": "agente", "energia": 120},
        {"nombre": "Orion",   "rol": "admin",  "energia": 200},
        {"nombre": "Lyra",    "rol": "agente", "energia": 90},
    ]

    for agente in agentes:
        r = requests.post(f"{BASE_URL}/agentes/", json=agente, headers=HEADERS_AUTH)
        if r.status_code == 201:
            ok(f"Agente '{agente['nombre']}' creado (rol={agente['rol']}, energía={agente['energia']})")
        elif r.status_code == 409:
            ok(f"Agente '{agente['nombre']}' ya existía — continuando.")
        else:
            error(f"Error creando '{agente['nombre']}': {r.status_code} — {r.json()}")

    if r_sin_key.status_code == 401:
        ok("Sin API key → 401 correctamente rechazado.")
    else:
        error(f"Esperaba 401 sin key, obtuve: {r_sin_key.status_code} — {r_sin_key.json()}")

def paso3_crear_misiones() -> tuple[int, int, int]:
    titulo("PASO 3 — Crear misiones")

    misiones = [
        {
            "titulo": "Infiltrar base enemiga",
            "descripcion": "Acceder al servidor central sin dejar rastro.",
            "agente_asignado": "Nova",
            "energia_requerida": 30,
            "prioridad": 3,
            "creado_por": "control_central",
        },
        {
            "titulo": "Desencriptar mensaje interceptado",
            "descripcion": "Analizar el comunicado cifrado capturado.",
            "agente_asignado": "Orion",
            "energia_requerida": 20,
            "prioridad": 2,
            "creado_por": "control_central",
        },
        {
            "titulo": "Vigilancia perimetral",
            "descripcion": "Monitoreo pasivo del sector norte.",
            "agente_asignado": "Lyra",
            "energia_requerida": 10,
            "prioridad": 1,
            "creado_por": "control_central",
        },
    ]

    ids = []
    for mision in misiones:
        r = requests.post(f"{BASE_URL}/misiones/", json=mision, headers=HEADERS_AUTH)
        if r.status_code == 201:
            datos = r.json()
            ids.append(datos["id"])
            ok(f"Misión '{mision['titulo']}' creada (id={datos['id']}, prioridad={mision['prioridad']})")
        else:
            error(f"Error creando misión: {r.status_code} — {r.json()}")
            ids.append(None)

    r_404 = requests.post(
        f"{BASE_URL}/misiones/",
        json={"titulo": "Ghost op", "agente_asignado": "Fantasma", "energia_requerida": 5},
        headers=HEADERS_AUTH,
    )
    if r_404.status_code == 404:
        ok("Agente inexistente en misión → 404 correctamente devuelto.")
    else:
        error(f"Esperaba 404, obtuve: {r_404.status_code}")

    return tuple(ids)


def paso4_completar_misiones(id_nova: int, id_orion: int) -> None:
    titulo("PASO 4 — Completar misiones (descuento de energía por clase)")

    for mision_id, etiqueta in [(id_nova, "Nova (agente)"), (id_orion, "Orion (admin)")]:
        r = requests.post(
            f"{BASE_URL}/misiones/{mision_id}/completar",
            headers=HEADERS_AUTH,
        )
        if r.status_code == 200:
            datos = r.json()
            ok(f"Misión {mision_id} completada por {etiqueta}")
            dato("  es_admin",         datos["es_admin"])
            dato("  energía restante", datos["energia_restante"])
            dato("  detalle",          datos["detalle_energia"])
        else:
            error(f"Error completando misión {mision_id}: {r.status_code} — {r.json()}")

    r_409 = requests.post(f"{BASE_URL}/misiones/{id_nova}/completar", headers=HEADERS_AUTH)
    if r_409.status_code == 409:
        ok("Misión ya completada → 409 correctamente devuelto.")
    else:
        error(f"Esperaba 409, obtuve: {r_409.status_code}")


def paso5_briefing() -> None:
    titulo("PASO 5 — Briefing combinado (local + fuente externa)")

    for nombre in ["Nova", "Orion"]:
        r = requests.get(f"{BASE_URL}/briefing/{nombre}", timeout=10)
        if r.status_code == 200:
            datos = r.json()
            ok(f"Briefing de '{nombre}':")
            dato("  tipo_clase",           datos["tipo_clase"])
            dato("  energía",              datos["agente"]["energia"])
            dato("  misiones_completadas", datos["misiones_completadas"])
            dato("  misiones_pendientes",  datos["misiones_pendientes"])
            lectura = datos["inteligencia_externa"].get("lectura_recomendada", "—")
            fuente  = datos["fuente_externa"]
            dato("  lectura recomendada",  lectura)
            dato("  fuente_externa",       fuente)
            if "no disponible" in fuente:
                ok("  Fallback externo activado correctamente (API externa inaccesible).")
        else:
            error(f"Error en briefing de '{nombre}': {r.status_code} — {r.json()}")

def paso6_mensajeria() -> None:
    titulo("PASO 6 — Mensajería entre agentes")

    mensajes = [
        {"remitente": "Orion",  "destinatario": "Nova", "contenido": "Misión completada. Regresa a base."},
        {"remitente": "Nova",   "destinatario": "Lyra", "contenido": "Necesito refuerzos en el sector norte."},
        {"remitente": "Orion",  "destinatario": "Lyra", "contenido": "Mantén el perímetro vigilado."},
        {"remitente": "Lyra",   "destinatario": "Nova", "contenido": "Confirmo posición. En espera."},
        {"remitente": "Nova",   "destinatario": "Orion", "contenido": "Objetivo alcanzado. Retiro exitoso."},
    ]

    for msg in mensajes:
        r = requests.post(f"{BASE_URL}/mensajes/", json=msg, headers=HEADERS_AUTH)
        if r.status_code == 201:
            ok(f"Mensaje: {msg['remitente']} → {msg['destinatario']}")
        else:
            error(f"Error enviando mensaje: {r.status_code} — {r.json()}")

    print()
    r = requests.get(f"{BASE_URL}/mensajes/Nova")
    if r.status_code == 200:
        bandeja = r.json()
        ok(f"Bandeja de Nova ({len(bandeja)} mensajes):")
        for msg in bandeja:
            print(f"    [{msg['timestamp'][:19]}] {msg['remitente']}: {msg['contenido']}")
    else:
        error(f"Error leyendo bandeja: {r.status_code}")

if __name__ == "__main__":
    print("\n" + "█" * 60)
    print("  AGENCIA DE AGENTES — Demostración end-to-end")
    print("█" * 60)

    paso1_verificar_servidor()
    paso2_crear_agentes()
    ids = paso3_crear_misiones()
    paso4_completar_misiones(ids[0], ids[1])
    paso5_briefing()
    paso6_mensajeria()

    titulo("DEMO COMPLETADA")
    ok("El circuito completo funcionó de punta a punta.")
    print()