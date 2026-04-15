import logging
import requests as http_client

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from agente import PseudoAgente, AgenteAdmin
from db import (
    crear_tablas,
    registrar_agente,
    despertar_agente,
    listar_agentes,
    actualizar_energia,
    enviar_mensaje,
    leer_mensajes,
    crear_mision,
    obtener_mision,
    listar_misiones_de_agente,
    cambiar_estado_mision,
)
from config import AGENCIA_API_KEY, EXTERNAL_API_URL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

crear_tablas()
logger.info("Tablas de base de datos verificadas/creadas.")

app = FastAPI(
    title="Agencia de Agentes",
    description="API para gestionar agentes, mensajes y misiones. Endpoints de escritura requieren X-API-KEY.",
    version="1.0.0",
)

class AgenteRequest(BaseModel):
    nombre: str
    rol: str = "agente"
    energia: int = 100


class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str


class MisionRequest(BaseModel):
    titulo: str
    descripcion: str = ""
    agente_asignado: str
    energia_requerida: int = 10
    prioridad: int = 1
    creado_por: str = "sistema"


_api_key_scheme = APIKeyHeader(name="X-API-KEY", auto_error=False)

def verificar_api_key(x_api_key: str | None = Depends(_api_key_scheme)) -> str:
    if not AGENCIA_API_KEY:
        logger.error("AGENCIA_API_KEY no configurada en el entorno.")
        raise HTTPException(status_code=500, detail="Servidor mal configurado: falta API key.")
    if x_api_key != AGENCIA_API_KEY:
        logger.warning("Intento de acceso con API key inválida o ausente.")
        raise HTTPException(status_code=401, detail="API key inválida.")
    return x_api_key


def reconstruir_agente(datos: dict) -> PseudoAgente:
    if datos["rol"] == "admin":
        return AgenteAdmin(nombre=datos["nombre"], energia=datos["energia"])
    return PseudoAgente(nombre=datos["nombre"], rol=datos["rol"], energia=datos["energia"])

@app.get("/", summary="Estado del servidor")
def inicio():
    logger.info("Endpoint raíz consultado.")
    return {"status": "online", "mensaje": "Bienvenido a la Agencia de Agentes"}

@app.get("/agentes/", summary="Listar todos los agentes")
def listar():
    agentes = listar_agentes()
    logger.info(f"Listado de agentes consultado: {len(agentes)} registros.")
    return agentes

@app.get("/agente/{nombre}", summary="Obtener un agente por nombre")
def obtener_agente(nombre: str):
    datos = despertar_agente(nombre)
    if datos is None:
        logger.warning(f"Agente '{nombre}' no encontrado.")
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")
    logger.info(f"Agente '{nombre}' consultado.")
    return datos

@app.post("/agentes/", status_code=201, summary="Crear un agente (requiere API key)")
def crear_agente(req: AgenteRequest, _: str = Depends(verificar_api_key)):
    resultado = registrar_agente(req.nombre, req.rol, req.energia)
    if "ya existe" in resultado:
        logger.warning(f"Intento de crear agente duplicado: '{req.nombre}'.")
        raise HTTPException(status_code=409, detail=resultado)
    logger.info(f"Agente '{req.nombre}' creado con rol '{req.rol}'.")
    return {"mensaje": resultado}

@app.post("/mensajes/", status_code=201, summary="Enviar un mensaje (requiere API key)")
def enviar(req: MensajeRequest, _: str = Depends(verificar_api_key)):
    if despertar_agente(req.destinatario) is None:
        logger.warning(f"Mensaje rechazado: destinatario '{req.destinatario}' no existe.")
        raise HTTPException(status_code=404, detail=f"Destinatario '{req.destinatario}' no encontrado.")
    resultado = enviar_mensaje(req.remitente, req.destinatario, req.contenido)
    logger.info(f"Mensaje de '{req.remitente}' a '{req.destinatario}' enviado.")
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}", summary="Leer mensajes recibidos por un agente")
def leer_bandeja(nombre: str):
    if despertar_agente(nombre) is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")
    mensajes = leer_mensajes(nombre)
    logger.info(f"Bandeja de '{nombre}' consultada: {len(mensajes)} mensajes.")
    return mensajes


@app.post("/misiones/", status_code=201, summary="Crear una misión (requiere API key)")
def crear(req: MisionRequest, _: str = Depends(verificar_api_key)):
    if despertar_agente(req.agente_asignado) is None:
        logger.warning(f"Misión rechazada: agente '{req.agente_asignado}' no existe.")
        raise HTTPException(status_code=404, detail=f"Agente '{req.agente_asignado}' no encontrado.")
    mision = crear_mision(
        titulo=req.titulo,
        descripcion=req.descripcion,
        agente_asignado=req.agente_asignado,
        energia_requerida=req.energia_requerida,
        prioridad=req.prioridad,
        creado_por=req.creado_por,
    )
    logger.info(f"Misión '{req.titulo}' (id={mision['id']}) creada para '{req.agente_asignado}'.")
    return mision


@app.get("/misiones/{mision_id}", summary="Obtener una misión por ID")
def obtener(mision_id: int):
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Misión {mision_id} no encontrada.")
    logger.info(f"Misión {mision_id} consultada.")
    return mision


@app.get("/agente/{nombre}/misiones", summary="Listar misiones asignadas a un agente")
def misiones_de_agente(nombre: str):
    if despertar_agente(nombre) is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")
    misiones = listar_misiones_de_agente(nombre)
    logger.info(f"Misiones de '{nombre}' consultadas: {len(misiones)} registros.")
    return misiones


@app.post("/misiones/{mision_id}/completar", summary="Completar una misión (requiere API key)")
def completar_mision(mision_id: int, _: str = Depends(verificar_api_key)):
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Misión {mision_id} no encontrada.")
    if mision["estado"] == "completada":
        raise HTTPException(status_code=409, detail="La misión ya fue completada.")

    datos = despertar_agente(mision["agente_asignado"])
    if datos is None:
        logger.error(f"Agente '{mision['agente_asignado']}' no encontrado al completar misión {mision_id}.")
        raise HTTPException(status_code=404, detail=f"Agente '{mision['agente_asignado']}' no encontrado.")

    agente = reconstruir_agente(datos)

    try:
        mensaje_energia = agente.consumir_energia(mision["energia_requerida"])
    except ValueError as e:
        logger.warning(f"Energía insuficiente para completar misión {mision_id}: {e}")
        raise HTTPException(status_code=422, detail=str(e))

    actualizar_energia(agente.nombre, agente.energia)
    cambiar_estado_mision(mision_id, "completada")

    logger.info(
        f"Misión {mision_id} completada por '{agente.nombre}' "
        f"(es_admin={isinstance(agente, AgenteAdmin)}). {mensaje_energia}"
    )
    return {
        "mensaje": f"Misión '{mision['titulo']}' completada.",
        "agente": agente.nombre,
        "es_admin": isinstance(agente, AgenteAdmin),
        "energia_restante": agente.energia,
        "detalle_energia": mensaje_energia,
    }

@app.get("/briefing/{nombre}", summary="Briefing completo del agente (datos locales + fuente externa)")
def briefing(nombre: str):
    datos = despertar_agente(nombre)
    if datos is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")

    agente = reconstruir_agente(datos)
    misiones = listar_misiones_de_agente(nombre)

    briefing_local = {
        "agente": agente.resumen(),
        "tipo_clase": type(agente).__name__,
        "total_misiones": len(misiones),
        "misiones_completadas": sum(1 for m in misiones if m["estado"] == "completada"),
        "misiones_pendientes": sum(1 for m in misiones if m["estado"] == "pendiente"),
    }

    try:
        respuesta = http_client.get(
            EXTERNAL_API_URL,
            params={"q": nombre, "limit": 1, "fields": "title,author_name,first_publish_year"},
            timeout=3,  
        )
        respuesta.raise_for_status()
        datos_ext = respuesta.json()
        libros = datos_ext.get("docs", [])
        if libros:
            libro = libros[0]
            inteligencia = {
                "lectura_recomendada": libro.get("title", "Sin título"),
                "autor": libro.get("author_name", ["Desconocido"])[0],
                "año": libro.get("first_publish_year", "?"),
            }
        else:
            inteligencia = {"lectura_recomendada": "Sin resultados para este agente."}
        fuente = EXTERNAL_API_URL
        logger.info(f"Briefing de '{nombre}' generado con datos externos.")

    except http_client.exceptions.Timeout:
        inteligencia = {"lectura_recomendada": "Fuente externa no disponible (timeout)."}
        fuente = "no disponible (timeout)"
        logger.warning(f"Timeout al consultar API externa para briefing de '{nombre}'.")

    except Exception as exc:
        inteligencia = {"lectura_recomendada": "Fuente externa no disponible."}
        fuente = "no disponible (error)"
        logger.warning(f"Error al consultar API externa para '{nombre}': {exc}")

    return {
        **briefing_local,
        "inteligencia_externa": inteligencia,
        "fuente_externa": fuente,
    }
