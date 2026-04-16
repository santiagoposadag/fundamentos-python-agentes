# Este archivo se encarga de cargar datos semilla en la base de datos para tener un entorno de prueba listo.

import db  # Importamos nuestro módulo de base de datos para interactuar con SQLite
import logging # Para el registro de eventos durante la carga de datos

# Configuración básica para ver qué pasa en la consola
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Semillas")

def cargar_datos_semilla():
    logger.info("Iniciando carga de datos semilla...")
    
    # 1. Aseguramos que la DB esté inicializada
    db.inicializar_db()

    # 2. Insertar 3 Agentes 
    agentes = [
        ("Andres_Admin", "admin", 200),
        ("Agente_Bot", "explorer", 100),
        ("Sofia_Spy", "explorer", 120)
    ]
    for nombre, rol, energia in agentes:
        if db.registrar_agente(nombre, rol, energia):
            logger.info(f"✅ Agente creado: {nombre}")
        else:
            logger.warning(f"⚠️ Agente {nombre} ya existía.")

    # 3. Insertar 5 Mensajes 
    mensajes = [
        ("Andres_Admin", "Agente_Bot", "Bienvenido a la agencia, recluta."),
        ("Agente_Bot", "Andres_Admin", "Gracias, señor. Listo para la acción."),
        ("Sofia_Spy", "Andres_Admin", "Informe de inteligencia enviado."),
        ("Andres_Admin", "Sofia_Spy", "Recibido Sofia, mantente en posición."),
        ("Agente_Bot", "Sofia_Spy", "¿Alguien sabe dónde está el café?")
    ]
    for rem, dest, cont in mensajes:
        db.guardar_mensaje(rem, dest, cont)
    logger.info("✅ 5 Mensajes de prueba insertados.")

    # 4. Insertar 3 Misiones en estados distintos 
    # Estados: 'pendiente', 'completada', 'en_curso'
    conn = db.obtener_conexion()
    try:
        # Misión 1: Pendiente
        conn.execute("""
            INSERT INTO misiones (titulo, descripcion, agente_asignado, energia_requerida, estado)
            VALUES (?, ?, ?, ?, ?)
        """, ("Infiltración Alpha", "Entrar en la base enemiga.", "Sofia_Spy", 40, "pendiente"))
        
        # Misión 2: Completada
        conn.execute("""
            INSERT INTO misiones (titulo, descripcion, agente_asignado, energia_requerida, estado)
            VALUES (?, ?, ?, ?, ?)
        """, ("Escaneo de Red", "Verificar vulnerabilidades.", "Agente_Bot", 20, "completada"))
        
        # Misión 3: Pendiente
        conn.execute("""
            INSERT INTO misiones (titulo, descripcion, agente_asignado, energia_requerida, estado)
            VALUES (?, ?, ?, ?, ?)
        """, ("Mantenimiento Core", "Actualizar el núcleo de IA.", "Andres_Admin", 60, "en_curso"))
        
        conn.commit()
        logger.info("3 Misiones de prueba insertadas.")
    except Exception as e:
        logger.error(f"[Error]: Al insertar misiones: {e}")
    finally:
        conn.close()

    logger.info("Carga finalizada con éxito.")

if __name__ == "__main__":
    cargar_datos_semilla()