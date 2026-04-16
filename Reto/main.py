
"""
main.py — API principal con FastAPI

Implementa la aplicación FastAPI y los endpoints.
No se definen clases de dominio ni queries SQL en crudo aquí.
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import logging
import requests
from config import get_env_variable
from db import (
    crear_tablas,
    registrar_agente,
    despertar_agente,
    enviar_mensaje,
    leer_mensajes,
    listar_agentes,
    registrar_mision,
    consultar_mision,
    listar_misiones_agente,
    completar_mision,
    actualizar_energia_agente
)
from agente import PseudoAgente, AgenteAdmin

# Crear tablas al iniciar
crear_tablas()


# Auditoría: Logging
# Se usa nivel INFO para registrar eventos normales (creación, éxito), WARNING para situaciones anómalas (API externa lenta o caída), y ERROR para fallos reales (integridad, excepciones). El formato incluye fecha, nivel y mensaje para trazabilidad y auditoría.
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Auditoría: Autenticación
# Decidí proteger solo los endpoints de escritura (POST de misiones y completar misión) para balancear seguridad y facilidad de consulta pública. Los GET quedan libres para permitir exploración y pruebas abiertas.
def verificar_api_key(x_api_key: str = Header(None)):
    api_key = get_env_variable("AGENCIA_API_KEY")
    if not x_api_key or x_api_key != api_key:
        logger.warning("Intento de acceso con API key inválida o ausente.")
        raise HTTPException(status_code=401, detail="API key inválida")

app = FastAPI(
	title="Agencia de Agentes",
	description="API para gestionar agentes, mensajes y misiones"
)

# Modelos Pydantic
class AgenteRequest(BaseModel):
    nombre: str
    rol: str
    energia: int

class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str

class MisionRequest(BaseModel):
    titulo: str
    descripcion: str = None
    agente_asignado: str
    energia_requerida: int
    prioridad: str = None
    deadline: str = None
    recompensa: int = None

# Endpoints básicos
@app.get("/")
def root():
    return {"mensaje": "Agencia de Agentes operativa"}

@app.get("/agente/{nombre}")
def get_agente(nombre: str):
    agente = despertar_agente(nombre)
    if not agente:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    return agente

@app.get("/agentes/")
def get_agentes():
    return listar_agentes()

@app.post("/agentes/", dependencies=[Depends(verificar_api_key)])
def post_agente(agente: AgenteRequest):
    resultado = registrar_agente(agente.nombre, agente.rol, agente.energia)
    logger.info("Agente creado: %s (%s)", agente.nombre, agente.rol)
    return {"resultado": resultado}

@app.post("/mensajes/")
def post_mensaje(mensaje: MensajeRequest):
    return {"resultado": enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)}

@app.get("/mensajes/{nombre}")
def get_mensajes(nombre: str):
    return leer_mensajes(nombre)

# Endpoints de misiones
@app.post("/misiones/", dependencies=[Depends(verificar_api_key)])
def post_mision(mision: MisionRequest):
    agente = despertar_agente(mision.agente_asignado)
    if not agente:
        logger.error("Intento de asignar misión a agente inexistente: %s", mision.agente_asignado)
        raise HTTPException(status_code=404, detail="Agente asignado no existe")
    mision_id = registrar_mision(
        mision.titulo, mision.descripcion, mision.agente_asignado,
        mision.energia_requerida, mision.prioridad, mision.deadline, mision.recompensa
    )
    logger.info("Misión creada: %s para %s", mision.titulo, mision.agente_asignado)
    return {"id": mision_id}

@app.get("/misiones/{codigo_mision}")
def get_mision(codigo_mision: int):
    mision = consultar_mision(codigo_mision)
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    return mision

@app.get("/agente/{nombre}/misiones")
def get_misiones_agente(nombre: str):
    return listar_misiones_agente(nombre)

@app.post("/misiones/{mision_id}/completar", dependencies=[Depends(verificar_api_key)])
def post_completar_mision(mision_id: int):
    mision = consultar_mision(mision_id)
    if not mision:
        logger.error("Intento de completar misión inexistente: %s", mision_id)
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    agente_data = despertar_agente(mision["agente_asignado"])
    if not agente_data:
        logger.error("Intento de completar misión con agente inexistente: %s", mision['agente_asignado'])
        raise HTTPException(status_code=404, detail="Agente asignado no existe")
    if agente_data["rol"] == "admin":
        agente = AgenteAdmin(agente_data["nombre"], agente_data["energia"])
    else:
        agente = PseudoAgente(agente_data["nombre"], agente_data["energia"])
    agente.descontar_energia(mision["energia_requerida"])
    actualizar_energia_agente(agente.nombre, agente.energia)
    completar_mision(mision_id)
    logger.info("Misión completada: %s por %s", mision_id, agente.nombre)
    return {"mensaje": f"Misión {mision_id} completada y energía descontada"}

# Endpoint briefing (placeholder, API externa en siguiente fase)
@app.get("/briefing/{nombre}")
# Auditoría: Briefing externo
# Se eligió la API de Advice Slip por su sencillez y narrativa. Si la API externa falla o responde lento, se retorna un mensaje de fallback y nunca se interrumpe la respuesta local.
def get_briefing(nombre: str):
    agente = despertar_agente(nombre)
    if not agente:
        logger.error("Briefing solicitado para agente inexistente: %s", nombre)
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    # API pública externa (ejemplo: frase aleatoria)
    api_url = get_env_variable("EXTERNAL_API_URL", "https://api.adviceslip.com/advice")
    externo = {}
    try:
        resp = requests.get(api_url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # Adaptar según la API elegida
        externo = {
            "consejo": data.get("slip", {}).get("advice", "Sin consejo disponible"),
            "fuente_externa": api_url
        }
        logger.info("Briefing externo obtenido para %s", nombre)
    except (
        requests.Timeout,
        requests.ConnectionError,
        requests.HTTPError,
        requests.JSONDecodeError,
    ) as e:
        externo = {"consejo": "No se pudo obtener consejo externo", "fuente_externa": api_url}
        logger.warning("Fallo al obtener briefing externo: %s", e)
    return {"agente": agente, **externo}
