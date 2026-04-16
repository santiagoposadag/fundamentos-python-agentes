# db.py
# Aqui estan todas las funciones que hablan con SQLite.
# Ninguna otra parte del proyecto escribe SQL directo, solo este archivo.

import sqlite3
import datetime
from config import DB_PATH


def crear_tablas():
    """Crea las tablas si no existen. Se puede llamar varias veces sin problemas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agentes (
            nombre TEXT PRIMARY KEY,
            rol TEXT,
            energia INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remitente TEXT,
            destinatario TEXT,
            contenido TEXT,
            timestamp TEXT
        )
    """)

    # La tabla misiones tiene prioridad y creado_por para saber urgencia y trazabilidad
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            agente_asignado TEXT,
            estado TEXT,
            energia_requerida INTEGER,
            prioridad TEXT,
            creado_por TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# --- AGENTES ---

def registrar_agente(nombre: str, rol: str, energia: int) -> str:
    """Inserta un agente nuevo. Si ya existe retorna un mensaje de error."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Usamos ? en vez de f-string para evitar inyeccion SQL
        cursor.execute(
            "INSERT INTO agentes (nombre, rol, energia) VALUES (?, ?, ?)",
            (nombre, rol, energia)
        )
        conn.commit()
        resultado = f"[DB] Agente '{nombre}' registrado con exito."
    except sqlite3.IntegrityError:
        resultado = f"[DB] Error: El agente '{nombre}' ya existe en la base de datos."
    finally:
        conn.close()
    return resultado


def despertar_agente(nombre: str):
    """Busca un agente por nombre. Retorna un dict con sus datos o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, rol, energia FROM agentes WHERE nombre = ?",
        (nombre,)
    )
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}


def listar_agentes():
    """Retorna una lista con todos los agentes registrados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": f[0], "rol": f[1], "energia": f[2]} for f in filas]


def actualizar_energia(nombre: str, nueva_energia: int) -> None:
    """Actualiza la energia de un agente en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE agentes SET energia = ? WHERE nombre = ?",
        (nueva_energia, nombre)
    )
    conn.commit()
    conn.close()


# --- MENSAJES ---

def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str:
    """Inserta un mensaje con timestamp automatico."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) VALUES (?, ?, ?, ?)",
        (remitente, destinatario, contenido, timestamp)
    )
    conn.commit()
    conn.close()
    return f"[DB] Mensaje de '{remitente}' a '{destinatario}' enviado a las {timestamp}."


def leer_mensajes(nombre_agente: str):
    """Retorna todos los mensajes dirigidos a un agente, ordenados por fecha."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT remitente, destinatario, contenido, timestamp FROM mensajes WHERE destinatario = ? ORDER BY timestamp",
        (nombre_agente,)
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {"remitente": f[0], "destinatario": f[1], "contenido": f[2], "timestamp": f[3]}
        for f in filas
    ]


# --- MISIONES ---

def crear_mision(titulo: str, descripcion: str, agente_asignado: str,
                 energia_requerida: int, prioridad: str = "media",
                 creado_por: str = "sistema") -> int:
    """Inserta una mision nueva con estado 'pendiente'. Retorna el ID creado."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        """INSERT INTO misiones
           (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, creado_por, created_at)
           VALUES (?, ?, ?, 'pendiente', ?, ?, ?, ?)""",
        (titulo, descripcion, agente_asignado, energia_requerida, prioridad, creado_por, timestamp)
    )
    conn.commit()
    mision_id = cursor.lastrowid  # el ID que SQLite le asigno automaticamente
    conn.close()
    return mision_id


def obtener_mision(mision_id: int):
    """Busca una mision por ID. Retorna dict o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, titulo, descripcion, agente_asignado, estado,
                  energia_requerida, prioridad, creado_por, created_at
           FROM misiones WHERE id = ?""",
        (mision_id,)
    )
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {
        "id": fila[0],
        "titulo": fila[1],
        "descripcion": fila[2],
        "agente_asignado": fila[3],
        "estado": fila[4],
        "energia_requerida": fila[5],
        "prioridad": fila[6],
        "creado_por": fila[7],
        "created_at": fila[8]
    }


def listar_misiones_agente(nombre_agente: str):
    """Retorna todas las misiones asignadas a un agente."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, titulo, descripcion, agente_asignado, estado,
                  energia_requerida, prioridad, creado_por, created_at
           FROM misiones WHERE agente_asignado = ? ORDER BY created_at""",
        (nombre_agente,)
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {
            "id": f[0],
            "titulo": f[1],
            "descripcion": f[2],
            "agente_asignado": f[3],
            "estado": f[4],
            "energia_requerida": f[5],
            "prioridad": f[6],
            "creado_por": f[7],
            "created_at": f[8]
        }
        for f in filas
    ]


def marcar_mision_completada(mision_id: int) -> None:
    """Cambia el estado de una mision a 'completada'."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE misiones SET estado = 'completada' WHERE id = ?",
        (mision_id,)
    )
    conn.commit()
    conn.close()
