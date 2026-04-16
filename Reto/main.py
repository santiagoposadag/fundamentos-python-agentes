import logging
import requests
import datetime
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel

from db import (
    crear_tablas, registrar_agente, despertar_agente, listar_agentes,
    enviar_mensaje, leer_mensajes, crear_mision, obtener_mision,
    listar_misiones_agente, actualizar_estado_mision, actualizar_energia_agente
)
from agente import PseudoAgente, AgenteAdmin
from config import AGENCIA_API_KEY, EXTERNAL_API_URL

# Configuración de logging
# Elegí nivel INFO para registrar eventos significativos sin saturar el log con detalles de depuración.
# El formato incluye timestamp para trazabilidad temporal de las acciones en la agencia.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

crear_tablas()

app = FastAPI(title="La Agencia de Agentes")

# Dependencia para verificar API Key
# Protegemos los endpoints de escritura para asegurar que solo operadores autorizados realicen cambios.
# Los GET permanecen públicos para facilitar la consulta de información general de la agencia.
async def verificar_api_key(x_api_key: str = Header(...)):
    if x_api_key != AGENCIA_API_KEY:
        logger.error("Intento de acceso con API Key inválida.")
        raise HTTPException(status_code=401, detail="API key inválida")
    return x_api_key

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
    descripcion: str
    agente_asignado: str
    energia_requerida: int
    prioridad: str = "normal"

# Endpoints
@app.get("/")
def home():
    return {"status": "online", "agencia": "La Agencia de Agentes"}

@app.post("/agentes/")
def api_registrar_agente(agente: AgenteRequest, api_key: str = Depends(verificar_api_key)):
    res = registrar_agente(agente.nombre, agente.rol, agente.energia)
    logger.info(f"Registro de agente: {agente.nombre}")
    return {"mensaje": res}

@app.get("/agente/{nombre}")
def api_obtener_agente(nombre: str):
    agente = despertar_agente(nombre)
    if not agente:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    return agente

@app.get("/agentes/")
def api_listar_agentes():
    return listar_agentes()

@app.post("/mensajes/")
def api_enviar_mensaje(msg: MensajeRequest, api_key: str = Depends(verificar_api_key)):
    res = enviar_mensaje(msg.remitente, msg.destinatario, msg.contenido)
    logger.info(f"Mensaje enviado de {msg.remitente} a {msg.destinatario}")
    return {"mensaje": res}

@app.get("/mensajes/{nombre}")
def api_leer_mensajes(nombre: str):
    return leer_mensajes(nombre)

@app.post("/misiones/")
def api_crear_mision(mision: MisionRequest, api_key: str = Depends(verificar_api_key)):
    if not despertar_agente(mision.agente_asignado):
        logger.warning(f"Intento de asignar misión a agente inexistente: {mision.agente_asignado}")
        raise HTTPException(status_code=404, detail=f"Agente '{mision.agente_asignado}' no existe")
    
    mision_id = crear_mision(
        mision.titulo, mision.descripcion, mision.agente_asignado, 
        mision.energia_requerida, mision.prioridad
    )
    logger.info(f"Misión creada con ID {mision_id} para {mision.agente_asignado}")
    return {"mensaje": "Misión creada", "id": mision_id}

@app.get("/misiones/{id}")
def api_obtener_mision(id: int):
    mision = obtener_mision(id)
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    return mision

@app.get("/agente/{nombre}/misiones")
def api_misiones_agente(nombre: str):
    return listar_misiones_agente(nombre)

@app.post("/misiones/{id}/completar")
def api_completar_mision(id: int, api_key: str = Depends(verificar_api_key)):
    mision = obtener_mision(id)
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    
    if mision["estado"] == "completada":
        return {"mensaje": "La misión ya estaba completada"}

    datos_agente = despertar_agente(mision["agente_asignado"])
    if not datos_agente:
        raise HTTPException(status_code=404, detail="El agente asignado ya no existe")

    if datos_agente["rol"].lower() == "admin":
        agente_obj = AgenteAdmin(datos_agente["nombre"], energia=datos_agente["energia"])
    else:
        agente_obj = PseudoAgente(datos_agente["nombre"], rol=datos_agente["rol"], energia=datos_agente["energia"])

    res_energia = agente_obj.descontar_energia(mision["energia_requerida"])
    
    actualizar_energia_agente(agente_obj.nombre, agente_obj.energia)
    actualizar_estado_mision(id, "completada")
    
    logger.info(f"Misión {id} completada por {agente_obj.nombre}. {res_energia}")
    return {
        "mensaje": "Misión completada con éxito",
        "detalle_energia": res_energia,
        "agente_status": {
            "nombre": agente_obj.nombre,
            "energia_restante": agente_obj.energia,
            "es_admin": isinstance(agente_obj, AgenteAdmin)
        }
    }

# Endpoint de Briefing con API externa
# Elegí la API de catfact.ninja para añadir un 'dato curioso' al briefing del agente.
# El plan de contingencia ante fallos externos es omitir el dato y registrar un aviso, evitando romper la respuesta local.
@app.get("/briefing/{nombre}")
def api_briefing_agente(nombre: str):
    datos_agente = despertar_agente(nombre)
    if not datos_agente:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    
    externo_info = "Información externa no disponible actualmente."
    try:
        response = requests.get(EXTERNAL_API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            externo_info = data.get("fact", data.get("message", "Sin contenido relevante"))
        else:
            logger.warning(f"API externa respondió con status {response.status_code}")
    except Exception as e:
        logger.error(f"Error al consultar API externa: {e}")
        externo_info = "Error al conectar con la fuente de inteligencia externa."

    return {
        "agente": datos_agente,
        "inteligencia_adicional": externo_info,
        "fuente_externa": EXTERNAL_API_URL,
        "timestamp": datetime.datetime.now().isoformat()
    }
