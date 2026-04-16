import logging

import requests
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, field_validator

from agente import AgenteAdmin, PseudoAgente
from config import API_KEY, EXTERNAL_API_URL
from db import (
    actualizar_agente,
    actualizar_energia_agente,
    completar_mision,
    crear_mision,
    crear_tablas,
    despertar_agente,
    eliminar_agente,
    enviar_mensaje,
    listar_agentes,
    listar_misiones_agente,
    leer_mensajes,
    obtener_mision,
    registrar_agente,
    tiene_misiones_activas,
)

# ─── Logging ──────────────────────────────────────────────────────────────────
# Formato con fecha, nivel y mensaje — suficiente para auditar sin ruido excesivo.
# INFO para el flujo normal, WARNING para degradación (ej: API externa caída),
# ERROR para fallos que rompen operaciones (integridad SQL, excepciones inesperadas).
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="La Agencia de Agentes",
    description="API para gestionar agentes, mensajes y misiones.",
    version="1.0.0",
)

crear_tablas()
logger.info("Tablas de base de datos inicializadas.")


# ─── Modelos Pydantic ─────────────────────────────────────────────────────────

class AgenteRequest(BaseModel):
    nombre: str
    rol: str
    energia: int


class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str


ESTADOS_VALIDOS = {"pendiente", "en_curso", "completada", "fallida"}


class MisionRequest(BaseModel):
    titulo: str
    descripcion: str = ""
    agente_asignado: str
    estado: str = "pendiente"
    energia_requerida: int
    prioridad: str = "media"

    @field_validator("energia_requerida")
    @classmethod
    def energia_debe_ser_positiva(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("La energía requerida debe ser mayor a 0")
        return v

    @field_validator("estado")
    @classmethod
    def estado_debe_ser_valido(cls, v: str) -> str:
        if v not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Valores permitidos: {ESTADOS_VALIDOS}")
        return v


# ─── Autenticación ────────────────────────────────────────────────────────────
# Protejo todos los endpoints de escritura (POST /agentes/, POST /misiones/,
# POST /misiones/{id}/completar). Los GET son lectura pública — información de
# agentes no es sensible y facilita la integración con clientes sin auth.
def verificar_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida")


# ─── Endpoints base (conservados de S5) ───────────────────────────────────────

@app.get("/")
def inicio():
    return {"status": "online", "mensaje": "Bienvenido a La Agencia de Agentes"}


@app.get("/agente/{nombre}")
def obtener_agente(nombre: str):
    agente = despertar_agente(nombre)
    if agente is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    return agente


@app.get("/agentes/")
def obtener_todos_los_agentes():
    return listar_agentes()


@app.post("/agentes/", status_code=201, dependencies=[Depends(verificar_api_key)])
def crear_agente(agente: AgenteRequest):
    resultado = registrar_agente(agente.nombre, agente.rol, agente.energia)
    logger.info("Agente creado: %s (rol=%s)", agente.nombre, agente.rol)
    return {"mensaje": resultado}


@app.post("/mensajes/")
def nuevo_mensaje(mensaje: MensajeRequest):
    resultado = enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)
    logger.info("Mensaje de '%s' a '%s'", mensaje.remitente, mensaje.destinatario)
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}")
def bandeja_entrada(nombre: str):
    return leer_mensajes(nombre)


# ─── Endpoints de misiones ────────────────────────────────────────────────────

@app.post("/misiones/", status_code=201, dependencies=[Depends(verificar_api_key)])
def nueva_mision(mision: MisionRequest):
    if despertar_agente(mision.agente_asignado) is None:
        raise HTTPException(
            status_code=404,
            detail=f"El agente '{mision.agente_asignado}' no existe. Registralo primero.",
        )
    id_mision = crear_mision(
        titulo=mision.titulo,
        descripcion=mision.descripcion,
        agente_asignado=mision.agente_asignado,
        estado=mision.estado,
        energia_requerida=mision.energia_requerida,
        prioridad=mision.prioridad,
    )
    logger.info("Misión #%d creada: '%s' → agente '%s'", id_mision, mision.titulo, mision.agente_asignado)
    return {"id": id_mision, "mensaje": f"Misión '{mision.titulo}' creada correctamente."}


@app.get("/misiones/{id}")
def detalle_mision(id: int):
    mision = obtener_mision(id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Misión #{id} no encontrada")
    return mision


@app.get("/agente/{nombre}/misiones")
def misiones_del_agente(nombre: str):
    if despertar_agente(nombre) is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    return listar_misiones_agente(nombre)


@app.post("/misiones/{id}/completar", dependencies=[Depends(verificar_api_key)])
def completar(id: int):
    mision = obtener_mision(id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Misión #{id} no encontrada")
    if mision["estado"] == "completada":
        raise HTTPException(status_code=400, detail="La misión ya fue completada.")

    datos_db = despertar_agente(mision["agente_asignado"])
    if datos_db is None:
        raise HTTPException(status_code=404, detail=f"Agente '{mision['agente_asignado']}' no encontrado en la base de datos.")

    # Reconstruimos la instancia correcta según el rol — el objeto de dominio decide
    # cómo se descuenta la energía, no el endpoint.
    if datos_db["rol"] == "admin":
        agente = AgenteAdmin(datos_db["nombre"], datos_db["energia"])
    else:
        agente = PseudoAgente(datos_db["nombre"], datos_db["energia"])

    agente.usar_energia(mision["energia_requerida"])
    actualizar_energia_agente(agente.nombre, agente.energia)
    completar_mision(id)

    logger.info(
        "Misión #%d completada por '%s'. Energía restante: %d",
        id, agente.nombre, agente.energia,
    )
    return {
        "mensaje": f"Misión '{mision['titulo']}' completada.",
        "agente": agente.nombre,
        "es_admin": isinstance(agente, AgenteAdmin),
        "energia_restante": agente.energia,
    }


# ─── CRUD Eutagógico ──────────────────────────────────────────────────────────

class AgenteUpdateRequest(BaseModel):
    energia: int
    rol: str


@app.put("/agentes/{nombre}", dependencies=[Depends(verificar_api_key)])
def actualizar(nombre: str, datos: AgenteUpdateRequest):
    if despertar_agente(nombre) is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    try:
        actualizar_agente(nombre, datos.energia, datos.rol)
        logger.info("Agente '%s' actualizado: energia=%d, rol=%s", nombre, datos.energia, datos.rol)
        return despertar_agente(nombre)
    except Exception as e:
        logger.error("Error al actualizar agente '%s': %s", nombre, str(e))
        raise HTTPException(status_code=500, detail="Error interno al actualizar el agente")


@app.delete("/agentes/{nombre}", dependencies=[Depends(verificar_api_key)])
def eliminar(nombre: str):
    if despertar_agente(nombre) is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")
    # Decisión: bloqueamos el delete si tiene misiones activas (pendiente o en_curso)
    # para no dejar misiones huérfanas sin responsable.
    if tiene_misiones_activas(nombre):
        raise HTTPException(
            status_code=400,
            detail=f"El agente '{nombre}' tiene misiones activas. Completalas o cancelalas antes de eliminar.",
        )
    try:
        eliminar_agente(nombre)
        logger.info("Agente '%s' eliminado.", nombre)
        return {"mensaje": f"Agente '{nombre}' eliminado correctamente."}
    except Exception as e:
        logger.error("Error al eliminar agente '%s': %s", nombre, str(e))
        raise HTTPException(status_code=500, detail="Error interno al eliminar el agente")


@app.get("/briefing/{nombre}")
def briefing(nombre: str):
    # Elijo api.adviceslip.com: retorna consejos en JSON sin auth ni API key.
    # Plan de contingencia: timeout de 3s + except amplio. Si la API externa falla,
    # devuelvo un fallback string y log de WARNING — el endpoint nunca se rompe.
    datos = despertar_agente(nombre)
    if datos is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado")

    try:
        respuesta = requests.get(EXTERNAL_API_URL, timeout=3)
        consejo = respuesta.json()["slip"]["advice"]
        fuente_externa = EXTERNAL_API_URL
    except Exception:
        logger.warning("API externa no disponible. Activando fallback para briefing de '%s'.", nombre)
        consejo = "Sin datos externos disponibles en este momento."
        fuente_externa = "fallback"

    return {
        "agente": datos,
        "consejo_de_mision": consejo,
        "fuente_externa": fuente_externa,
    }
