import logging
import requests as http_client

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import Literal

import config
import db
from agente import PseudoAgente, AgenteAdmin

# ──────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────
# AUDITORÍA: Se usa INFO para eventos normales del sistema (agente creado, misión completada),
# WARNING para situaciones degradadas pero recuperables (API externa lenta, fallback activado),
# y ERROR para fallos reales (excepciones inesperadas). El formato incluye timestamp y nivel
# para facilitar la auditoría y el diagnóstico de problemas en producción.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# INICIO: crear tablas si no existen
# ──────────────────────────────────────────────
db.crear_tablas()
logger.info("Tablas de la base de datos verificadas/creadas al arrancar.")

# ──────────────────────────────────────────────
# APLICACIÓN
# ──────────────────────────────────────────────
app = FastAPI(
    title="Sistema de Agentes — La Agencia",
    description=(
        "API para gestionar agentes, mensajes y misiones. "
        "Los endpoints de escritura requieren el header **X-API-KEY**."
    ),
    version="1.0.0",
)

# ──────────────────────────────────────────────
# MODELOS PYDANTIC
# ──────────────────────────────────────────────

class AgenteRequest(BaseModel):
    nombre: str
    rol: str
    energia: int = Field(default=100, gt=0, description="Energía inicial (>0)")


class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str


class MisionRequest(BaseModel):
    titulo: str
    descripcion: str = ""
    agente_asignado: str
    estado: Literal["pendiente", "en_curso", "completada", "fallida"] = "pendiente"
    energia_requerida: int = Field(..., gt=0, description="Energía requerida (>0)")
    prioridad: Literal["alta", "media", "baja"] = "media"
    recompensa: int = Field(default=0, ge=0)
    creado_por: str = ""


# ──────────────────────────────────────────────
# AUTENTICACIÓN — API KEY
# ──────────────────────────────────────────────
# AUDITORÍA: Decidí proteger TODOS los endpoints POST (escritura) con API key porque
# exponer operaciones de creación y modificación sin autenticación es un riesgo de
# seguridad real (cualquier cliente podría crear agentes fantasma o completar misiones
# ajenas). Los GET (lectura) se dejaron públicos porque la información de agentes y
# misiones no es sensible en este contexto y facilita la consulta desde Swagger UI sin
# configuración adicional. La clave se verifica contra AGENCIA_API_KEY del .env para
# evitar hardcodear secretos en el código fuente.
def verificar_api_key(x_api_key: str | None = Header(default=None, description="Clave de la Agencia")) -> str:
    # Header opcional para que FastAPI no lance 422 antes de llegar aquí;
    # la ausencia o valor incorrecto devuelve 401 tal como exige el reto.
    if not config.AGENCIA_API_KEY:
        logger.error("AGENCIA_API_KEY no está configurada en el entorno.")
        raise HTTPException(status_code=500, detail="Servidor mal configurado: API key no definida.")
    if x_api_key != config.AGENCIA_API_KEY:
        logger.warning("Intento de acceso con API key inválida o ausente.")
        raise HTTPException(status_code=401, detail="API key inválida.")
    return x_api_key


# ──────────────────────────────────────────────
# HELPER: reconstruir clase de dominio desde BD
# ──────────────────────────────────────────────

def _reconstruir_agente(datos: dict) -> PseudoAgente | AgenteAdmin:
    """
    Reconstruye la instancia de clase correcta a partir de los datos de la BD.
    Si rol == 'admin' → AgenteAdmin; cualquier otro rol → PseudoAgente.
    Verificable con isinstance().
    """
    nombre = datos["nombre"]
    rol = datos["rol"]
    energia = datos["energia"]
    if rol == "admin":
        return AgenteAdmin(nombre, energia)
    return PseudoAgente(nombre, energia)


# ──────────────────────────────────────────────
# ENDPOINTS HEREDADOS DE SEMANA 5
# ──────────────────────────────────────────────

@app.get("/", summary="Estado del servidor")
def inicio():
    return {"status": "online", "mensaje": "Bienvenido a La Agencia — Sistema de Agentes"}


@app.get("/agentes/", summary="Listar todos los agentes")
def obtener_todos_los_agentes():
    return db.listar_agentes()


@app.get("/agente/{nombre}", summary="Consultar un agente por nombre")
def obtener_agente(nombre: str):
    agente = db.despertar_agente(nombre)
    if agente is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")
    return agente


@app.post("/agentes/", status_code=201, summary="Registrar un nuevo agente")
def crear_agente(agente: AgenteRequest, _key: str = Depends(verificar_api_key)):
    resultado = db.registrar_agente(agente.nombre, agente.rol, agente.energia)
    logger.info(f"Agente registrado: '{agente.nombre}' (rol={agente.rol}).")
    return {"mensaje": resultado}


@app.post("/mensajes/", status_code=201, summary="Enviar un mensaje entre agentes")
def crear_mensaje(mensaje: MensajeRequest, _key: str = Depends(verificar_api_key)):
    resultado = db.enviar_mensaje(mensaje.remitente, mensaje.destinatario, mensaje.contenido)
    logger.info(f"Mensaje enviado de '{mensaje.remitente}' a '{mensaje.destinatario}'.")
    return {"mensaje": resultado}


@app.get("/mensajes/{nombre}", summary="Leer bandeja de entrada de un agente")
def obtener_mensajes(nombre: str):
    return db.leer_mensajes(nombre)


# ──────────────────────────────────────────────
# NUEVOS ENDPOINTS: MISIONES
# ──────────────────────────────────────────────

@app.post("/misiones/", status_code=201, summary="Crear una nueva misión (protegido)")
def crear_mision(mision: MisionRequest, _key: str = Depends(verificar_api_key)):
    # Verificar que el agente asignado existe antes de crear la misión.
    if db.despertar_agente(mision.agente_asignado) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Agente '{mision.agente_asignado}' no encontrado. Registra al agente primero.",
        )
    mision_id = db.crear_mision(
        titulo=mision.titulo,
        descripcion=mision.descripcion,
        agente_asignado=mision.agente_asignado,
        estado=mision.estado,
        energia_requerida=mision.energia_requerida,
        prioridad=mision.prioridad,
        recompensa=mision.recompensa,
        creado_por=mision.creado_por,
    )
    logger.info(f"Misión creada: id={mision_id}, título='{mision.titulo}', agente='{mision.agente_asignado}'.")
    return {"id": mision_id, "mensaje": f"Misión '{mision.titulo}' creada con id {mision_id}."}


@app.get("/misiones/{mision_id}", summary="Consultar una misión por ID")
def obtener_mision(mision_id: int):
    mision = db.obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Misión con id {mision_id} no encontrada.")
    return mision


@app.get("/agente/{nombre}/misiones", summary="Listar misiones asignadas a un agente")
def obtener_misiones_agente(nombre: str):
    if db.despertar_agente(nombre) is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")
    return db.obtener_misiones_agente(nombre)


@app.post("/misiones/{mision_id}/completar", summary="Completar una misión (protegido)")
def completar_mision(mision_id: int, _key: str = Depends(verificar_api_key)):
    # 1. Obtener la misión
    mision = db.obtener_mision(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail=f"Misión con id {mision_id} no encontrada.")
    if mision["estado"] == "completada":
        raise HTTPException(status_code=400, detail="La misión ya fue completada anteriormente.")

    # 2. Obtener y reconstruir el agente como objeto de dominio
    datos_agente = db.despertar_agente(mision["agente_asignado"])
    if datos_agente is None:
        raise HTTPException(
            status_code=404,
            detail=f"Agente '{mision['agente_asignado']}' asignado a la misión no existe.",
        )

    agente = _reconstruir_agente(datos_agente)
    es_admin = isinstance(agente, AgenteAdmin)

    # 3. La clase controla el descuento de energía, no el endpoint
    try:
        resultado = agente.usar_energia(mision["energia_requerida"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 4. Persistir nuevo estado del agente y de la misión
    db.actualizar_energia_agente(agente.nombre, agente.tokens)
    db.marcar_mision_completada(mision_id)

    logger.info(
        f"Misión id={mision_id} completada. Agente='{agente.nombre}' "
        f"(AgenteAdmin={es_admin}), energía restante={agente.tokens}."
    )
    return {
        "mensaje": f"Misión '{mision['titulo']}' completada con éxito.",
        "agente": agente.nombre,
        "es_admin": es_admin,
        "resultado_clase": resultado,
        "energia_restante": agente.tokens,
    }


# ──────────────────────────────────────────────
# BRIEFING: datos locales + inteligencia externa
# ──────────────────────────────────────────────
# AUDITORÍA: Elegí la API pública "Advice Slip" (adviceslip.com) porque retorna consejos
# estratégicos en JSON sin autenticación, encajando con la narrativa de agentes que reciben
# inteligencia del mundo exterior antes de una misión. Plan de contingencia: si la API falla
# o tarda más de 5 segundos, el endpoint retorna los datos locales del agente con un mensaje
# de fallback en "inteligencia_externa" y fuente_externa="fallback". El servidor nunca se
# bloquea esperando una respuesta de un tercero.

@app.get("/briefing/{nombre}", summary="Briefing completo del agente (local + externo)")
def obtener_briefing(nombre: str):
    agente_datos = db.despertar_agente(nombre)
    if agente_datos is None:
        raise HTTPException(status_code=404, detail=f"Agente '{nombre}' no encontrado.")

    misiones = db.obtener_misiones_agente(nombre)

    inteligencia_externa: str
    fuente_externa: str

    try:
        resp = http_client.get(
            config.EXTERNAL_API_URL,
            timeout=5,
            headers={"Accept": "application/json"},
        )
        resp.raise_for_status()
        data = resp.json()
        inteligencia_externa = data["slip"]["advice"]
        fuente_externa = config.EXTERNAL_API_URL
        logger.info(f"Briefing de '{nombre}': inteligencia externa obtenida correctamente.")
    except http_client.exceptions.Timeout:
        logger.warning(f"API externa tardó demasiado al obtener briefing de '{nombre}'. Activando fallback.")
        inteligencia_externa = "Inteligencia exterior no disponible. Procede con los datos locales."
        fuente_externa = "fallback"
    except Exception as exc:
        logger.error(f"Error al consultar API externa para briefing de '{nombre}': {exc}")
        inteligencia_externa = "Inteligencia exterior no disponible. Procede con los datos locales."
        fuente_externa = "fallback"

    return {
        "agente": agente_datos,
        "misiones_asignadas": len(misiones),
        "inteligencia_externa": inteligencia_externa,
        "fuente_externa": fuente_externa,
    }
