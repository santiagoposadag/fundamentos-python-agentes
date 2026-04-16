
"""
db.py — Funciones de acceso a la base de datos SQLite

Funciones para agentes, mensajes y misiones.
No incluye lógica de FastAPI ni clases de dominio.
"""

import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentes.db")


def crear_tablas():
    """Crea las tablas agentes, mensajes y misiones si no existen."""
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            agente_asignado TEXT,
            estado TEXT,
            energia_requerida INTEGER,
            prioridad TEXT,
            deadline TEXT,
            recompensa INTEGER,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def registrar_agente(nombre: str, rol: str, energia: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO agentes (nombre, rol, energia) VALUES (?, ?, ?)",
            (nombre, rol, energia),
        )
        conn.commit()
        resultado = f"[DB] Agente '{nombre}' registrado."
    except sqlite3.IntegrityError:
        resultado = f"[DB] El agente '{nombre}' ya existe."
    finally:
        conn.close()
    return resultado

def despertar_agente(nombre: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, rol, energia FROM agentes WHERE nombre = ?",
        (nombre,),
    )
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}

def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) VALUES (?, ?, ?, ?)",
        (remitente, destinatario, contenido, timestamp),
    )
    conn.commit()
    conn.close()
    return f"[DB] Mensaje de '{remitente}' a '{destinatario}' enviado a las {timestamp}."

def leer_mensajes(nombre_agente: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT remitente, destinatario, contenido, timestamp "
        "FROM mensajes WHERE destinatario = ? ORDER BY timestamp",
        (nombre_agente,),
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {
            "remitente": f[0],
            "destinatario": f[1],
            "contenido": f[2],
            "timestamp": f[3],
        }
        for f in filas
    ]

def listar_agentes() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": f[0], "rol": f[1], "energia": f[2]} for f in filas]

# --- Funciones para misiones ---
def registrar_mision(
    titulo: str,
    descripcion: str,
    agente_asignado: str,
    energia_requerida: int,
    prioridad: str = None,
    deadline: str = None,
    recompensa: int = None,
) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO misiones (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, deadline, recompensa, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            titulo,
            descripcion,
            agente_asignado,
            'pendiente',
            energia_requerida,
            prioridad,
            deadline,
            recompensa,
            created_at,
        ),
    )
    conn.commit()
    mision_id = cursor.lastrowid
    conn.close()
    return mision_id

def consultar_mision(id_mision: int) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM misiones WHERE id = ?", (id_mision,))
    fila = cursor.fetchone()
    columnas = [desc[0] for desc in cursor.description]
    conn.close()
    if fila is None:
        return None
    return dict(zip(columnas, fila))

def listar_misiones_agente(nombre_agente: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM misiones WHERE agente_asignado = ? ORDER BY created_at DESC",
        (nombre_agente,),
    )
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    conn.close()
    return [dict(zip(columnas, fila)) for fila in filas]

def completar_mision(id_mision: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE misiones SET estado = ? WHERE id = ?", ("completada", id_mision))
    conn.commit()
    actualizado = cursor.rowcount > 0
    conn.close()
    return actualizado

def actualizar_energia_agente(nombre: str, nueva_energia: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE agentes SET energia = ? WHERE nombre = ?", (nueva_energia, nombre))
    conn.commit()
    actualizado = cursor.rowcount > 0
    conn.close()
    return actualizado
