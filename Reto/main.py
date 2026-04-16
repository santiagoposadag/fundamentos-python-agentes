# main.py
# Archivo principal de la API. Aqui viven todos los endpoints.
# Las clases de dominio estan en agente.py y las consultas a la DB en db.py.

import logging
import random
import requests

from fastapi import FastAPI, HTTPException, Header, Depends
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
    listar_misiones_agente,
    marcar_mision_completada,
)
from config import AGENCIA_API_KEY, EXTERNAL_API_URL

# Configuramos el logger para ver los eventos importantes en la consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Creamos las tablas al arrancar. Si ya existen no pasa nada.
crear_tablas()
logger.info("Base de datos lista. Servidor iniciando.")

app = FastAPI(
    title="Agencia de Agentes",
    description="API para gestionar agentes, mensajes y misiones de la Agencia.",
    version="1.0.0",
)


# Modelos Pydantic: definen la estructura del body que esperamos en los POST
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
    prioridad: str = "media"
    creado_por: str = "operador"


# Funcion que verifica el header X-API-KEY en los endpoints protegidos
# Usamos default=None para poder devolver 401 nosotros mismos en vez de que FastAPI devuelva 422
def verificar_api_key(x_api_key: str = Header(default=None)):
    if x_api_key is None or x_api_key != AGENCIA_API_KEY:
        logger.warning("Intento de acceso con API key invalida.")
        raise HTTPException(status_code=401, detail="API key invalida")


@app.get("/")
def inicio():
    """Verifica que el servidor esta en linea."""
    logger.info("Health check solicitado.")
    return {"status": "online", "mensaje": "Bienvenidos a la Agencia de Agentes"}


@app.get("/agente/{nombre}")
def obtener_agente(nombre: str):
    """Devuelve los datos de un agente por nombre."""
    datos = despertar_agente(nombre)
    if datos is None:
        logger.warning(f"Agente '{nombre}' no encontrado.")
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    return datos


@app.get("/agentes/")
def obtener_todos_los_agentes():
    """Lista todos los agentes registrados."""
    return listar_agentes()


@app.post("/agentes/")
def crear_agente(agente: AgenteRequest, _=Depends(verificar_api_key)):
    """Registra un agente nuevo. Requiere API key."""
    resultado = registrar_agente(agente.nombre, agente.rol, agente.energia)
    logger.info(f"Agente creado: {agente.nombre} | rol: {agente.rol}")
    return {"mensaje": resultado}


@app.post("/mensajes/")
def crear_mensaje(mensaje: MensajeRequest):
    """Envia un mensaje de un agente a otro."""
    resultado = enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)
    logger.info(f"Mensaje enviado de '{mensaje.remitente}' a '{mensaje.destinatario}'")
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}")
def obtener_mensajes(nombre: str):
    """Devuelve todos los mensajes recibidos por un agente."""
    return leer_mensajes(nombre)


@app.post("/misiones/")
def crear_nueva_mision(mision: MisionRequest, _=Depends(verificar_api_key)):
    """Crea una mision nueva. Requiere API key."""
    # Verificamos que el agente exista antes de asignarle la mision
    agente_datos = despertar_agente(mision.agente_asignado)
    if agente_datos is None:
        logger.warning(f"Mision no creada: agente '{mision.agente_asignado}' no existe.")
        raise HTTPException(
            status_code=404,
            detail=f"El agente '{mision.agente_asignado}' no existe. Registralo primero."
        )

    mision_id = crear_mision(
        titulo=mision.titulo,
        descripcion=mision.descripcion,
        agente_asignado=mision.agente_asignado,
        energia_requerida=mision.energia_requerida,
        prioridad=mision.prioridad,
        creado_por=mision.creado_por,
    )
    logger.info(f"Mision #{mision_id} creada: '{mision.titulo}' para {mision.agente_asignado}")
    return {"mensaje": "Mision creada con exito.", "id": mision_id}


@app.get("/misiones/{mision_id}")
def obtener_una_mision(mision_id: int):
    """Devuelve los detalles de una mision por ID."""
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Mision #{mision_id} no encontrada")
    return mision


@app.get("/agente/{nombre}/misiones")
def obtener_misiones_del_agente(nombre: str):
    """Lista todas las misiones asignadas a un agente."""
    agente_datos = despertar_agente(nombre)
    if agente_datos is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    return listar_misiones_agente(nombre)


@app.post("/misiones/{mision_id}/completar")
def completar_mision(mision_id: int, _=Depends(verificar_api_key)):
    """
    Marca una mision como completada. Requiere API key.
    Reconstruye el objeto del agente desde la DB para descontar energia usando la clase.
    """
    mision = obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Mision #{mision_id} no encontrada")

    if mision["estado"] == "completada":
        raise HTTPException(status_code=400, detail="Esta mision ya fue completada.")

    agente_datos = despertar_agente(mision["agente_asignado"])
    if agente_datos is None:
        raise HTTPException(
            status_code=404,
            detail=f"El agente '{mision['agente_asignado']}' no existe en la base de datos."
        )

    # Reconstruimos la clase correcta segun el rol: admin o agente normal
    if agente_datos["rol"] == "admin":
        agente_obj = AgenteAdmin(nombre=agente_datos["nombre"], energia=agente_datos["energia"])
    else:
        agente_obj = PseudoAgente(nombre=agente_datos["nombre"], energia=agente_datos["energia"])

    # Intentamos descontar la energia usando el metodo de la clase
    resultado_energia = agente_obj.descontar_energia(mision["energia_requerida"])

    if resultado_energia.startswith("[Error]"):
        logger.warning(f"Mision #{mision_id} no completada: {resultado_energia}")
        raise HTTPException(
            status_code=400,
            detail=f"El agente no tiene energia suficiente. {resultado_energia}"
        )

    # Guardamos la nueva energia y marcamos la mision
    actualizar_energia(agente_obj.nombre, agente_obj.tokens)
    marcar_mision_completada(mision_id)

    logger.info(
        f"Mision #{mision_id} completada por '{agente_obj.nombre}'. "
        f"Energia restante: {agente_obj.tokens}."
    )

    return {
        "mensaje": f"Mision '{mision['titulo']}' completada.",
        "agente": agente_obj.nombre,
        "es_admin": isinstance(agente_obj, AgenteAdmin),
        "energia_restante": agente_obj.tokens,
    }


@app.get("/briefing/{nombre}")
def obtener_briefing(nombre: str, pais: str = None, capital: str = None):
    """
    Devuelve un briefing del agente combinando datos locales con info de un pais real.

    Parametros opcionales:
    - pais: busca ese pais especifico (ej. ?pais=Colombia)
    - capital: busca por la capital (ej. ?capital=Bogota)
    - si no se pasa ninguno, elige un pais de America al azar

    Elegi restcountries.com porque encaja bien con la narrativa de agentes que operan
    en distintos paises. Si la API falla, devolvemos igual el briefing local.
    """
    agente_datos = despertar_agente(nombre)
    if agente_datos is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")

    # Armamos la URL segun lo que nos pidieron
    campos = "?fields=name,capital,flags,region,population"

    if pais:
        url_externa = f"{EXTERNAL_API_URL}/name/{pais}{campos}"
        modo_busqueda = f"por nombre: {pais}"
    elif capital:
        url_externa = f"{EXTERNAL_API_URL}/capital/{capital}{campos}"
        modo_busqueda = f"por capital: {capital}"
    else:
        url_externa = f"{EXTERNAL_API_URL}/region/americas{campos}"
        modo_busqueda = "aleatorio de America"

    zona_operaciones = None
    fuente_externa = EXTERNAL_API_URL

    try:
        respuesta = requests.get(url_externa, timeout=3)

        if respuesta.status_code == 200:
            paises = respuesta.json()

            # Si buscamos uno especifico tomamos el primero, si es aleatorio elegimos al azar
            if pais or capital:
                pais_datos = paises[0]
            else:
                pais_datos = random.choice(paises)

            nombre_pais = pais_datos.get("name", {}).get("common", "Desconocido")
            capital_pais = pais_datos.get("capital", ["Desconocida"])
            capital_pais = capital_pais[0] if capital_pais else "Desconocida"
            region = pais_datos.get("region", "Desconocida")
            poblacion = pais_datos.get("population", 0)
            bandera = pais_datos.get("flags", {}).get("png", "")

            zona_operaciones = {
                "pais": nombre_pais,
                "capital": capital_pais,
                "region": region,
                "poblacion": poblacion,
                "bandera_url": bandera,
            }
            logger.info(f"Briefing de '{nombre}' ({modo_busqueda}): {nombre_pais}")

        elif respuesta.status_code == 404:
            logger.warning(f"Pais no encontrado en la API ({modo_busqueda}).")
            fuente_externa = f"no disponible (pais no encontrado)"
        else:
            logger.warning(f"API externa respondio con status {respuesta.status_code}.")
            fuente_externa = "no disponible"

    except requests.exceptions.Timeout:
        logger.warning("La API externa tardo demasiado. Retornando briefing sin zona.")
        fuente_externa = "no disponible (timeout)"
    except requests.exceptions.ConnectionError:
        logger.warning("No se pudo conectar a la API externa.")
        fuente_externa = "no disponible (sin conexion)"
    except Exception as e:
        logger.error(f"Error inesperado al consultar API externa: {e}")
        fuente_externa = "no disponible (error interno)"

    return {
        "agente": agente_datos,
        "zona_de_operaciones": zona_operaciones,
        "fuente_externa": fuente_externa,
    }
