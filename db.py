import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentes.db")


def crear_tablas() -> None:
    """Crea las tres tablas si no existen. Seguro de llamar múltiples veces."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agentes (
            nombre  TEXT PRIMARY KEY,
            rol     TEXT,
            energia INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            remitente    TEXT,
            destinatario TEXT,
            contenido    TEXT,
            timestamp    TEXT
        )
    """)

    # Decisión de ingeniería: columnas extra en misiones —
    #   prioridad   → clasifica urgencia (alta/media/baja) para el operador de la Agencia.
    #   recompensa  → energía que se devuelve al agente al completar (mecánica de juego).
    #   creado_por  → auditoría: qué operador registró la misión.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo           TEXT    NOT NULL,
            descripcion      TEXT,
            agente_asignado  TEXT,
            estado           TEXT,
            energia_requerida INTEGER,
            created_at       TEXT,
            prioridad        TEXT    DEFAULT 'media',
            recompensa       INTEGER DEFAULT 0,
            creado_por       TEXT
        )
    """)

    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
# AGENTES
# ──────────────────────────────────────────────

def registrar_agente(nombre: str, rol: str, energia: int) -> str:
    """Inserta un agente. Retorna mensaje de éxito o error si ya existe."""
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
        resultado = f"[DB] Error: el agente '{nombre}' ya existe en la base de datos."
    finally:
        conn.close()
    return resultado


def despertar_agente(nombre: str) -> dict | None:
    """Busca un agente por nombre. Retorna dict o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, rol, energia FROM agentes WHERE nombre = ?", (nombre,)
    )
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}


def actualizar_energia_agente(nombre: str, nueva_energia: int) -> None:
    """Persiste el nuevo valor de energía de un agente después de una misión."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE agentes SET energia = ? WHERE nombre = ?", (nueva_energia, nombre)
    )
    conn.commit()
    conn.close()


def listar_agentes() -> list[dict]:
    """Retorna todos los agentes registrados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": f[0], "rol": f[1], "energia": f[2]} for f in filas]


# ──────────────────────────────────────────────
# MENSAJES
# ──────────────────────────────────────────────

def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str:
    """Inserta un mensaje con timestamp automático."""
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
    """Lee todos los mensajes dirigidos a un agente, ordenados por timestamp."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT remitente, destinatario, contenido, timestamp
           FROM mensajes
           WHERE destinatario = ?
           ORDER BY timestamp""",
        (nombre_agente,),
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {"remitente": f[0], "destinatario": f[1], "contenido": f[2], "timestamp": f[3]}
        for f in filas
    ]


# ──────────────────────────────────────────────
# MISIONES
# ──────────────────────────────────────────────

def _fila_a_mision(fila: tuple) -> dict:
    """Convierte una fila de la tabla misiones en diccionario con nombres de campo."""
    return {
        "id": fila[0],
        "titulo": fila[1],
        "descripcion": fila[2],
        "agente_asignado": fila[3],
        "estado": fila[4],
        "energia_requerida": fila[5],
        "created_at": fila[6],
        "prioridad": fila[7],
        "recompensa": fila[8],
        "creado_por": fila[9],
    }


def crear_mision(
    titulo: str,
    descripcion: str,
    agente_asignado: str,
    estado: str,
    energia_requerida: int,
    prioridad: str = "media",
    recompensa: int = 0,
    creado_por: str = "",
) -> int:
    """Inserta una misión y retorna su ID autogenerado."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        """INSERT INTO misiones
           (titulo, descripcion, agente_asignado, estado, energia_requerida,
            created_at, prioridad, recompensa, creado_por)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (titulo, descripcion, agente_asignado, estado, energia_requerida,
         timestamp, prioridad, recompensa, creado_por),
    )
    conn.commit()
    mision_id = cursor.lastrowid
    conn.close()
    return mision_id


def obtener_mision(mision_id: int) -> dict | None:
    """Retorna una misión por ID o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, titulo, descripcion, agente_asignado, estado, energia_requerida,
                  created_at, prioridad, recompensa, creado_por
           FROM misiones WHERE id = ?""",
        (mision_id,),
    )
    fila = cursor.fetchone()
    conn.close()
    return _fila_a_mision(fila) if fila else None


def obtener_misiones_agente(nombre_agente: str) -> list[dict]:
    """Lista todas las misiones asignadas a un agente, ordenadas por fecha."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, titulo, descripcion, agente_asignado, estado, energia_requerida,
                  created_at, prioridad, recompensa, creado_por
           FROM misiones
           WHERE agente_asignado = ?
           ORDER BY created_at""",
        (nombre_agente,),
    )
    filas = cursor.fetchall()
    conn.close()
    return [_fila_a_mision(f) for f in filas]


def marcar_mision_completada(mision_id: int) -> None:
    """Cambia el estado de una misión a 'completada'."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE misiones SET estado = 'completada' WHERE id = ?", (mision_id,)
    )
    conn.commit()
    conn.close()
