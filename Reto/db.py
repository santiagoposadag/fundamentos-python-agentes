import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentes.db")

def crear_tablas() -> None:
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
            estado TEXT,                -- 'pendiente' | 'en_curso' | 'completada' | 'fallida'
            energia_requerida INTEGER,
            prioridad TEXT DEFAULT 'normal', -- Decisión de ingeniería extra
            created_at TEXT             -- timestamp ISO
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
        resultado = f"[DB] Agente '{nombre}' registrado con éxito."
    except sqlite3.IntegrityError:
        resultado = f"[DB] Error: El agente '{nombre}' ya existe."
    finally:
        conn.close()
    return resultado

def despertar_agente(nombre: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}

def actualizar_energia_agente(nombre: str, nueva_energia: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE agentes SET energia = ? WHERE nombre = ?", (nueva_energia, nombre))
    conn.commit()
    conn.close()

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
    return f"[DB] Mensaje enviado de {remitente} a {destinatario}."

def leer_mensajes(nombre_agente: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT remitente, destinatario, contenido, timestamp FROM mensajes WHERE destinatario = ? ORDER BY timestamp",
        (nombre_agente,),
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {"remitente": f[0], "destinatario": f[1], "contenido": f[2], "timestamp": f[3]}
        for f in filas
    ]

def listar_agentes() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": f[0], "rol": f[1], "energia": f[2]} for f in filas]

def crear_mision(titulo: str, descripcion: str, agente: str, energia: int, prioridad: str = "normal") -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO misiones (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, created_at)
        VALUES (?, ?, ?, 'pendiente', ?, ?, ?)
    """, (titulo, descripcion, agente, energia, prioridad, created_at))
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def obtener_mision(mision_id: int) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM misiones WHERE id = ?", (mision_id,))
    fila = cursor.fetchone()
    conn.close()
    if not fila:
        return None
    # id, titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, created_at
    return {
        "id": fila[0], "titulo": fila[1], "descripcion": fila[2],
        "agente_asignado": fila[3], "estado": fila[4], "energia_requerida": fila[5],
        "prioridad": fila[6], "created_at": fila[7]
    }

def listar_misiones_agente(nombre_agente: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM misiones WHERE agente_asignado = ?", (nombre_agente,))
    filas = cursor.fetchall()
    conn.close()
    return [
        {
            "id": f[0], "titulo": f[1], "descripcion": f[2],
            "agente_asignado": f[3], "estado": f[4], "energia_requerida": f[5],
            "prioridad": f[6], "created_at": f[7]
        } for f in filas
    ]

def actualizar_estado_mision(mision_id: int, nuevo_estado: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE misiones SET estado = ? WHERE id = ?", (nuevo_estado, mision_id))
    conn.commit()
    conn.close()
