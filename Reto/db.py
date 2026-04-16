# Este módulo se encarga de toda la interacción con la base de datos SQLite.
# Aquí definimos funciones para crear tablas, insertar datos, actualizar estados y consultar información.
# El cuerpo/memoria (Sabe guardar y recordar agentes, mensajes y misiones).

import sqlite3 # Para interactuar con la base de datos SQLite (Requisito R3)
from datetime import datetime # Para registrar timestamps en mensajes y misiones (Requisito R3)
# Importamos las clases el archivo agente.py para reconstruir los agentes
from agente import PseudoAgente, AgenteAdmin

DB_NAME = "agentes.db"

def obtener_conexion():
    """
    Establece conexión con la base de datos y permite acceder a columnas por nombre.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def inicializar_db():
    """
    Crea las tablas necesarias si no existen. 
    REQUISITO R3: Se añade la tabla de misiones.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()

    # 1. Tabla de Agentes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agentes (
        nombre TEXT PRIMARY KEY,
        rol TEXT NOT NULL,
        energia INTEGER DEFAULT 100
    )
    """)

    # 2. Tabla de Mensajes (Semana 5 - Sesión 2)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        remitente TEXT,
        destinatario TEXT,
        contenido TEXT,
        timestamp TEXT
    )
    """)

    # 3. NUEVA: Tabla de Misiones (Requisito R3)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS misiones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        agente_asignado TEXT,
        estado TEXT DEFAULT 'pendiente', -- pendiente, en_curso, completada
        energia_requerida INTEGER,
        created_at TEXT,
        FOREIGN KEY(agente_asignado) REFERENCES agentes(nombre)
    )
    """)
    
    conn.commit()
    conn.close()
    print("[DB]: Sistema de persistencia inicializado correctamente.")

# ============================================================ #
# FUNCIONES DE TRADUCCIÓN (EL PUENTE)
# ============================================================ #

def despertar_agente_clase(nombre: str):
    """
    REQUISITO R2: Esta es la función clave. 
    Busca en la DB y devuelve una INSTANCIA de la clase correcta.
    """
    conn = obtener_conexion()
    # Buscamos al agente por su nombre
    fila = conn.execute("SELECT * FROM agentes WHERE nombre = ?", (nombre,)).fetchone()
    conn.close()

    if fila:
        # Si el rol en la DB es 'admin', creamos un objeto AgenteAdmin
        if fila['rol'] == 'admin':
            return AgenteAdmin(nombre=fila['nombre'], energia=fila['energia'])
        # Si es cualquier otro rol, creamos un PseudoAgente normal
        else:
            return PseudoAgente(nombre=fila['nombre'], rol=fila['rol'], energia=fila['energia'])
    
    return None

def actualizar_energia_db(nombre: str, nueva_energia: int):
    """
    Guarda el nuevo estado de energía del agente en la base de datos.
    Esto se llama cada vez que un agente gasta energía.
    """
    conn = obtener_conexion()
    conn.execute("UPDATE agentes SET energia = ? WHERE nombre = ?", (nueva_energia, nombre))
    conn.commit()
    conn.close()

def registrar_agente(nombre: str, rol: str, energia: int):
    """
    Guarda un nuevo agente en la base de datos.
    """
    conn = obtener_conexion()
    try:
        conn.execute(
            "INSERT INTO agentes (nombre, rol, energia) VALUES (?, ?, ?)",
            (nombre, rol, energia)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # El nombre ya existe
    finally:
        conn.close()

def crear_mision(titulo: str, descripcion: str, agente: str, energia: int):
    """
    REQUISITO R3: Inserta una nueva misión.
    Registra la fecha de creación automáticamente.
    """
    conn = obtener_conexion()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        """INSERT INTO misiones 
           (titulo, descripcion, agente_asignado, energia_requerida, created_at) 
           VALUES (?, ?, ?, ?, ?)""",
        (titulo, descripcion, agente, energia, ahora)
    )
    conn.commit()
    conn.close()

def listar_misiones_agente(nombre_agente: str):
    """
    Trae todas las misiones que tiene asignadas un agente específico.
     Esto permite que el agente pueda consultar sus tareas pendientes o en curso.
    """
    conn = obtener_conexion()
    misiones = conn.execute(
        "SELECT * FROM misiones WHERE agente_asignado = ?", 
        (nombre_agente,)
    ).fetchall()
    conn.close()
    return misiones

def listar_todos_los_agentes():
    """
    Retorna una lista de todos los agentes registrados.
    """
    conn = obtener_conexion()
    agentes = conn.execute("SELECT * FROM agentes").fetchall()
    conn.close()
    return agentes

def guardar_mensaje(remitente: str, destinatario: str, contenido: str):
    """
    Guarda un mensaje en la tabla de mensajes con su timestamp.
    """
    conn = obtener_conexion()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) VALUES (?, ?, ?, ?)",
        (remitente, destinatario, contenido, ahora)
    )
    conn.commit()
    conn.close()

def listar_mensajes_agente(nombre_agente: str):
    """
    Obtiene la bandeja de entrada de un agente.
    """
    conn = obtener_conexion()
    mensajes = conn.execute(
        "SELECT * FROM mensajes WHERE destinatario = ? ORDER BY timestamp DESC", 
        (nombre_agente,)
    ).fetchall()
    conn.close()
    return mensajes