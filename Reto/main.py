# El "Director de la Agencia". Recibirá las peticiones de la web (FastAPI) y usará db.py para guardar y agente.py para procesar.

from fastapi import FastAPI, HTTPException, Depends, Header # FastAPI para crear la API, HTTPException para manejar errores, Depends y Header para proteger endpoints con API Key (Requisito 5.1)
from fastapi.security import APIKeyHeader # Para definir un esquema de seguridad basado en API Key (Requisito 5.1)
from pydantic import BaseModel # Para validar que los datos que llegan en las peticiones tengan el formato correcto (Requisito 5.3)
from typing import List, Optional # Para definir tipos de datos más complejos en las respuestas (Requisito 5.3)
from datetime import datetime # Para mostrar la fecha y hora del briefing (Requisito 5.2)
import config # Importamos la configuración de variables de entorno
import logging # Para el registro de eventos (Requisito 5.4)
import requests # Para hacer peticiones a la API externa (Requisito 5.2)

# Importamos nuestro motor de base de datos y nuestras clases
import db
from agente import PseudoAgente, AgenteAdmin

# 1. Configuración del Logger (Requisito 5.4)
# Usamos logging en lugar de print para tener registros profesionales 
# con fecha, hora y nivel de importancia (INFO, ERROR, etc.)
# Aseguramos que cualquier evento desde el arranque quede registrado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 2. Configuración de Seguridad para Swagger
# Para crear el botón "Authorize" con el candado arriba a la derecha
api_key_scheme = APIKeyHeader(name="X-API-KEY")

# Inicializamos FastAPI y la base de datos
app = FastAPI(title="La Agencia de Agentes - API")
db.inicializar_db()

# ============================================================ #
# MODELOS DE PYDANTIC (Validación de datos)
# ============================================================ #

class AgenteRequest(BaseModel):
    """
    Modelo para crear o actualizar agentes.
    """
    nombre: str
    rol: str
    energia: int = 100

class MensajeRequest(BaseModel):
    """
    Modelo para crear mensajes.
    """
    remitente: str
    destinatario: str
    contenido: str

class MisionRequest(BaseModel):
    """
    Modelo para crear misiones (Requisito R3).
    Asegura que nadie intente crear una misión sin título o con energía que no sea un número.
    """
    titulo: str
    descripcion: str
    agente_asignado: str
    energia_requerida: int

# La lógica de seguridad le pregunta a la "caja fuerte" (config)

def verificar_api_key(x_api_key: str = Depends(api_key_scheme)):
    """
    Verifica que la API Key sea correcta. 
    Usa 'Depends(api_key_scheme)' para activar el candado en la web.
    """
    if x_api_key != config.API_KEY:
        logger.warning(f"Intento de acceso fallido con API Key: {x_api_key}")
        raise HTTPException(status_code=401, detail="API Key inválida o ausente")
    return x_api_key

# ============================================================ #
# ENDPOINTS BÁSICOS (Lectura y Registro)
# ============================================================ #

@app.get("/")
def inicio():
    logger.info("Consulta al endpoint de inicio")
    return {"mensaje": "Bienvenido a la Central de la Agencia de Agentes"}

@app.post("/agentes/")
def crear_agente(datos: AgenteRequest, api_key: str = Depends(verificar_api_key)): # Si alguien intenta crear un agente sin la llave en el header, FastAPI le dirá automáticamente: "401 Unauthorized".
    """
    Crea un nuevo agente. 
    Protegido con API KEY (Requisito 5.1)
    """
    exito = db.registrar_agente(datos.nombre, datos.rol, datos.energia)
    if not exito:
        logger.error(f"Error al crear agente: {datos.nombre} ya existe.")
        raise HTTPException(status_code=400, detail="El agente ya existe")
    
    logger.info(f"Agente creado exitosamente: {datos.nombre}")
    return {"mensaje": f"Agente {datos.nombre} registrado en la agencia"}

@app.get("/agentes/")
def listar_agentes():
    """
    Lista todos los agentes (No requiere API Key según R4).
    """
    return db.listar_todos_los_agentes()

@app.post("/mensajes/")
def enviar_mensaje(datos: MensajeRequest):
    """
    Envía un mensaje entre agentes.
    """
    db.guardar_mensaje(datos.remitente, datos.destinatario, datos.contenido)
    logger.info(f"Mensaje enviado de {datos.remitente} a {datos.destinatario}")
    return {"mensaje": "Mensaje entregado"}

# ============================================================ #
# ENDPOINTS DE MISIONES (Requisito R3 y R4)
# ============================================================ #

@app.post("/misiones/") # REQUISITO R3: Endpoint para crear misiones, protegido con API Key (R5.1)
def crear_nueva_mision(datos: MisionRequest, api_key: str = Depends(verificar_api_key)):
    """
    Crea una misión y la asigna a un agente (Protegido con API Key).
    """
    # Verificamos si el agente asignado existe primero
    agente_existe = db.despertar_agente_clase(datos.agente_asignado)
    if not agente_existe:
        logger.warning(f"Intento de asignar misión a agente inexistente: {datos.agente_asignado}")
        raise HTTPException(status_code=404, detail="El agente asignado no existe")
    
    db.crear_mision(datos.titulo, datos.descripcion, datos.agente_asignado, datos.energia_requerida)
    logger.info(f"Misión '{datos.titulo}' creada y asignada a {datos.agente_asignado}")
    return {"mensaje": "Misión creada exitosamente"}

@app.post("/misiones/{mision_id}/completar") # REQUISITO R4: Endpoint para completar misiones, protegido con API Key (R5.1)
def completar_mision(mision_id: int, api_key: str = Depends(verificar_api_key)):
    """
    EL CORAZÓN DEL RETO (R2):
    Aquí reconstruimos al agente y usamos su lógica de clase.
    """
    conn = db.obtener_conexion()
    mision = conn.execute("SELECT * FROM misiones WHERE id = ?", (mision_id,)).fetchone()
    
    if not mision:
        conn.close()
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    
    if mision['estado'] == 'completada':
        conn.close()
        return {"mensaje": "La misión ya estaba completada anteriormente"}

    # 1. DESPERTAR: Traemos al agente desde la DB convertido en OBJETO DE CLASE
    agente_obj = db.despertar_agente_clase(mision['agente_asignado'])
    
    # 2. ACCIÓN: Usamos la habilidad del objeto (él decide cuánto gasta según su rol)
    # Si el agente es un Admin, ¡gastará la mitad automáticamente!
    # Si es un Explorer, gastará el total.
    costo = mision['energia_requerida']
    agente_obj.gastar_energia(costo)
    
    # 3. PERSISTENCIA: Guardamos el nuevo estado en la DB
    db.actualizar_energia_db(agente_obj.nombre, agente_obj.energia)
    conn.execute("UPDATE misiones SET estado = 'completada' WHERE id = ?", (mision_id,))
    conn.commit()
    conn.close()

    logger.info(f"Misión {mision_id} completada por {agente_obj.nombre}. Energía restante: {agente_obj.energia}")
    return {
        "mensaje": f"Misión '{mision['titulo']}' completada",
        "agente": agente_obj.nombre,
        "energia_restante": agente_obj.energia
    }

@app.get("/briefing/{nombre}") # REQUISITO 5.2: Endpoint que combina datos locales con una API externa
def obtener_briefing(nombre: str):
    """
    REQUISITO 5.2: Combina datos de la DB con una API externa.
    Maneja fallos de conexión con un plan de contingencia.
    """
    # 1. Buscamos al agente localmente
    agente = db.despertar_agente_clase(nombre)
    if not agente:
        raise HTTPException(status_code=404, detail="Agente no encontrado")

    # 2. Consultamos la inteligencia externa (API de Facts)
    dato_externo = "No se pudo obtener información externa en este momento."
    fuente = "Sistema Local (Fallback)"
    
    try:
        # Ponemos un timeout de 2 segundos para no colgar nuestro servidor
        respuesta = requests.get(config.API_URL, timeout=2)
        
        if respuesta.status_code == 200:
            info_json = respuesta.json()
            # En esta API el dato viene en la clave 'fact'
            dato_externo = info_json.get("fact", "Sin datos disponibles")
            fuente = "CatFact Public API"
            logger.info(f"Briefing externo obtenido para {nombre}")
        else:
            logger.warning(f"API Externa respondió con error {respuesta.status_code}")

    except Exception as e:
        # Si la API externa está caída, el servidor NO debe morir
        logger.error(f"Error de conexión con API externa: {e}")
    
    # 3. Combinamos todo en una respuesta única
    return {
        "agente": {
            "nombre": agente.nombre,
            "rol": agente.rol,
            "energia_actual": agente.energia,
            "estado_vital": "Óptimo" if agente.energia > 20 else "Crítico"
        },
        "misiones_asignadas": db.listar_misiones_agente(nombre),
        "inteligencia_adicional": {
            "dato_curioso": dato_externo,
            "fuente": fuente,
            "timestamp_briefing": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
