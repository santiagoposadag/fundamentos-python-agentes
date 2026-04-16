import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentes.db")


# ─── Inicialización ───────────────────────────────────────────────────────────

def crear_tablas() -> None:
    """Crea todas las tablas necesarias si no existen."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agentes (
                nombre TEXT PRIMARY KEY,
                rol TEXT,
                energia INTEGER
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remitente TEXT,
                destinatario TEXT,
                contenido TEXT,
                timestamp TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS misiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                agente_asignado TEXT,
                estado TEXT,
                energia_requerida INTEGER,
                prioridad TEXT DEFAULT 'media',
                completada_at TEXT,
                created_at TEXT
            )
        """)
        conn.commit()


# ─── Agentes ──────────────────────────────────────────────────────────────────

def registrar_agente(nombre: str, rol: str, energia: int) -> str:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO agentes (nombre, rol, energia) VALUES (?, ?, ?)",
                (nombre, rol, energia),
            )
            conn.commit()
        return f"Agente '{nombre}' registrado correctamente."
    except sqlite3.IntegrityError:
        return f"El agente '{nombre}' ya existe."


def despertar_agente(nombre: str) -> dict | None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT nombre, rol, energia FROM agentes WHERE nombre = ?", (nombre,)
        )
        fila = cursor.fetchone()
    if fila is None:
        return None
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}


def listar_agentes() -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT nombre, rol, energia FROM agentes")
        filas = cursor.fetchall()
    return [{"nombre": f[0], "rol": f[1], "energia": f[2]} for f in filas]


def actualizar_energia_agente(nombre: str, nueva_energia: int) -> None:
    """Persiste la energía del agente tras completar una misión."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE agentes SET energia = ? WHERE nombre = ?", (nueva_energia, nombre)
        )
        conn.commit()


# ─── Mensajes ─────────────────────────────────────────────────────────────────

def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str:
    timestamp = datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) VALUES (?, ?, ?, ?)",
            (remitente, destinatario, contenido, timestamp),
        )
        conn.commit()
    return f"Mensaje enviado a '{destinatario}' a las {timestamp}."


def leer_mensajes(nombre_agente: str) -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT remitente, destinatario, contenido, timestamp FROM mensajes WHERE destinatario = ? ORDER BY timestamp",
            (nombre_agente,),
        )
        filas = cursor.fetchall()
    return [
        {"remitente": f[0], "destinatario": f[1], "contenido": f[2], "timestamp": f[3]}
        for f in filas
    ]


# ─── Misiones ─────────────────────────────────────────────────────────────────

def crear_mision(
    titulo: str,
    descripcion: str,
    agente_asignado: str,
    estado: str,
    energia_requerida: int,
    prioridad: str = "media",
) -> int:
    """Inserta una misión y retorna su id."""
    created_at = datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """INSERT INTO misiones
               (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, created_at),
        )
        conn.commit()
        return cursor.lastrowid


def obtener_mision(id: int) -> dict | None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT id, titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, completada_at, created_at FROM misiones WHERE id = ?",
            (id,),
        )
        fila = cursor.fetchone()
    if fila is None:
        return None
    keys = ["id", "titulo", "descripcion", "agente_asignado", "estado", "energia_requerida", "prioridad", "completada_at", "created_at"]
    return dict(zip(keys, fila))


def listar_misiones_agente(nombre_agente: str) -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT id, titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, completada_at, created_at FROM misiones WHERE agente_asignado = ?",
            (nombre_agente,),
        )
        filas = cursor.fetchall()
    keys = ["id", "titulo", "descripcion", "agente_asignado", "estado", "energia_requerida", "prioridad", "completada_at", "created_at"]
    return [dict(zip(keys, f)) for f in filas]


def completar_mision(id: int) -> bool:
    """Marca la misión como completada. Retorna False si no existe."""
    completada_at = datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "UPDATE misiones SET estado = 'completada', completada_at = ? WHERE id = ?",
            (completada_at, id),
        )
        conn.commit()
        return cursor.rowcount > 0


def actualizar_agente(nombre: str, energia: int, rol: str) -> bool:
    """Actualiza energía y rol de un agente. Retorna False si no existe."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "UPDATE agentes SET energia = ?, rol = ? WHERE nombre = ?",
            (energia, rol, nombre),
        )
        conn.commit()
        return cursor.rowcount > 0


def eliminar_agente(nombre: str) -> bool:
    """Elimina un agente. Retorna False si no existe."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "DELETE FROM agentes WHERE nombre = ?", (nombre,)
        )
        conn.commit()
        return cursor.rowcount > 0


def tiene_misiones_activas(nombre: str) -> bool:
    """Verifica si un agente tiene misiones en estado pendiente o en_curso."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT COUNT(*) FROM misiones WHERE agente_asignado = ? AND estado IN ('pendiente', 'en_curso')",
            (nombre,),
        )
        return cursor.fetchone()[0] > 0
