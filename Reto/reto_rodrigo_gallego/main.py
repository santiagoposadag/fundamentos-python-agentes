"""
main.py - Punto de Entrada de la API

Gestiona los endpoints de FastAPI, la autenticación y la orquestación
entre el Dominio y la Persistencia.
"""

import logging
import requests
from typing import List, Dict, Any, Union
from fastapi import FastAPI, HTTPException, Depends, Header, status
from pydantic import BaseModel

# Importamos arquitectura propia
from agente import PseudoAgente, AgenteAdmin
from db import (
    inicializar_db, upsert_agente, obtener_agente, listar_agentes,
    registrar_mensaje, listar_mensajes_agente,
    crear_mision, obtener_mision, listar_misiones_agente, 
    actualizar_estado_mision
)
from config import settings

# --- Configuración de Logging (Salto 5.4) ---
# Elegimos INFO como nivel base para registrar eventos operativos normales.
# Evitamos DEBUG en producción para no saturar los logs.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("AgenciaAPI")

app = FastAPI(title="Agencia de Agentes 🕶️")

# Inicializar base de datos al arrancar
@app.on_event("startup")
def startup_event():
    logger.info("Iniciando servidor y base de datos...")
    inicializar_db()

# --- Modelos Pydantic (V2) ---

class AgenteRequest(BaseModel):
    nombre: str
    tokens: int = 100
    rol: str = "invitado"

class MensajeRequest(BaseModel):
    remitente: str
    destinatario: str
    contenido: str

class MisionRequest(BaseModel):
    titulo: str
    descripcion: str
    agente_asignado: str
    energia_requerida: int = 10

# --- Seguridad: Dependencia de API Key (Salto 5.1) ---
# Se decidió proteger solo POST/PUT para permitir la consulta pública (GET).
async def verificar_api_key(x_api_key: str = Header(...)):
    """Verifica que el header X-API-KEY coincida con el configurado."""
    if x_api_key != settings.API_KEY:
        logger.warning(f"Intento de acceso fallido con X-API-KEY: {x_api_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida o ausente"
        )
    return x_api_key

# --- Utilidades de Arquitectura (R2) ---

def reconstruir_agente(datos: dict) -> Union[PseudoAgente, AgenteAdmin]:
    """Fabrica la instancia de clase correcta según el rol recuperado de la DB."""
    if datos["rol"] == "admin":
        return AgenteAdmin(nombre=datos["nombre"], tokens=datos["tokens"])
    return PseudoAgente(nombre=datos["nombre"], tokens=datos["tokens"], rol=datos["rol"])

# --- Endpoints ---

@app.get("/")
def home():
    return {"status": "alive", "msg": "Bienvenido a la Central de la Agencia 🛰️"}

@app.get("/agente/{nombre}")
def get_agente(nombre: str):
    agente_db = obtener_agente(nombre)
    if not agente_db:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    return agente_db

@app.get("/agantes/") # Typo en repo original, corregido en Swagger si se prefiere
def get_all_agentes():
    return listar_agentes()

@app.post("/agentes/", status_code=status.HTTP_201_CREATED)
def post_agente(req: AgenteRequest, _=Depends(verificar_api_key)):
    upsert_agente(req.nombre, req.tokens, req.rol)
    logger.info(f"Agente {req.nombre} ({req.rol}) registrado/actualizado.")
    return {"msg": "Agente guardado exitosamente"}

@app.post("/mensajes/")
def post_mensaje(req: MensajeRequest):
    # Verificamos existencia
    if not obtener_agente(req.remitente) or not obtener_agente(req.destinatario):
        raise HTTPException(status_code=404, detail="Remitente o destinatario no existe")
    registrar_mensaje(req.remitente, req.destinatario, req.contenido)
    logger.info(f"Mensaje enviado de {req.remitente} a {req.destinatario}")
    return {"msg": "Mensaje enviado"}

@app.get("/mensajes/{nombre}")
def get_mensajes_agente(nombre: str):
    return listar_mensajes_agente(nombre)

# --- Endpoints de Misiones (R4) ---

@app.post("/misiones/")
def post_mision(req: MisionRequest, _=Depends(verificar_api_key)):
    if not obtener_agente(req.agente_asignado):
        logger.error(f"Error al crear misión: Agente {req.agente_asignado} no existe.")
        raise HTTPException(status_code=404, detail="Agente asignado no existe")
    mid = crear_mision(req.titulo, req.descripcion, req.agente_asignado, req.energia_requerida)
    logger.info(f"Misión {mid} ('{req.titulo}') creada para {req.agente_asignado}")
    return {"id": mid, "status": "pendiente"}

@app.get("/misiones/{id}")
def get_mision(id: int):
    mision = obtener_mision(id)
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    return mision

@app.get("/agente/{nombre}/misiones")
def get_misiones_agente(nombre: str):
    return listar_misiones_agente(nombre)

@app.post("/misiones/{id}/completar")
def post_completar_mision(id: int, _=Depends(verificar_api_key)):
    mision_db = obtener_mision(id)
    if not mision_db:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    
    if mision_db["estado"] == "completada":
        return {"msg": "La misión ya estaba completada"}

    # --- Reconstrucción de Dominio (R2) ---
    agente_db = obtener_agente(mision_db["agente_asignado"])
    agente_instancia = reconstruir_agente(agente_db)
    
    # Aplicamos lógica de dominio
    if agente_instancia.descontar_energia(mision_db["energia_requerida"]):
        # Persistimos cambios
        actualizar_estado_mision(id, "completada")
        upsert_agente(agente_instancia.nombre, agente_instancia.tokens, agente_instancia.rol)
        logger.info(f"Misión {id} completada por {agente_instancia.nombre}. Energía restante: {agente_instancia.tokens}")
        return {"id": id, "estado": "completada", "tokens_restantes": agente_instancia.tokens}
    else:
        logger.warning(f"Agente {agente_instancia.nombre} no tiene energía para misión {id}")
        raise HTTPException(status_code=400, detail="Energía insuficiente para completar la misión")

# --- Inteligencia Externa (Salto 5.2) ---

@app.get("/briefing/{nombre}")
def get_agente_briefing(nombre: str):
    """Combina datos locales con una API externa."""
    agente_db = obtener_agente(nombre)
    if not agente_db:
        raise HTTPException(status_code=404, detail="Agente no encontrado")
    
    # Intento de llamada a API externa
    # Plan de contingencia: si la API falla o tarda, respondemos con datos locales únicamente.
    external_fact = "La Agencia no pudo conectar con el satélite de inteligencia externa."
    try:
        response = requests.get(settings.EXTERNAL_API_URL, timeout=3.0)
        if response.status_code == 200:
            external_fact = response.json().get("fact", "Sin datos disponibles.")
    except Exception as e:
        logger.warning(f"Fallo en API externa ({settings.EXTERNAL_API_URL}): {e}")

    return {
        "agente": agente_db,
        "intel_externa": external_fact,
        "fuente_externa": settings.EXTERNAL_API_URL
    }
