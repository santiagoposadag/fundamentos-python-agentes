import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentes.db")

def crear_tablas() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agentes (
            nombre   TEXT PRIMARY KEY,
            rol      TEXT NOT NULL,
            energia  INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            remitente    TEXT NOT NULL,
            destinatario TEXT NOT NULL,
            contenido    TEXT NOT NULL,
            timestamp    TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misiones (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo           TEXT NOT NULL,
            descripcion      TEXT,
            agente_asignado  TEXT,
            estado           TEXT NOT NULL DEFAULT 'pendiente',
            energia_requerida INTEGER NOT NULL DEFAULT 10,
            prioridad        INTEGER NOT NULL DEFAULT 1,
            creado_por       TEXT,
            created_at       TEXT NOT NULL
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
        return f"Agente '{nombre}' registrado con éxito."
    except sqlite3.IntegrityError:
        return f"Error: el agente '{nombre}' ya existe."
    finally:
        conn.close()


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


def listar_agentes() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes ORDER BY nombre")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": f[0], "rol": f[1], "energia": f[2]} for f in filas]


def actualizar_energia(nombre: str, nueva_energia: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE agentes SET energia = ? WHERE nombre = ?",
        (nueva_energia, nombre),
    )
    conn.commit()
    filas_afectadas = cursor.rowcount
    conn.close()
    return filas_afectadas > 0

def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) "
        "VALUES (?, ?, ?, ?)",
        (remitente, destinatario, contenido, timestamp),
    )
    conn.commit()
    conn.close()
    return f"Mensaje de '{remitente}' a '{destinatario}' enviado a las {timestamp}."


def leer_mensajes(destinatario: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, remitente, destinatario, contenido, timestamp "
        "FROM mensajes WHERE destinatario = ? ORDER BY timestamp",
        (destinatario,),
    )
    filas = cursor.fetchall()
    conn.close()
    return [
        {
            "id": f[0],
            "remitente": f[1],
            "destinatario": f[2],
            "contenido": f[3],
            "timestamp": f[4],
        }
        for f in filas
    ]


def crear_mision(
    titulo: str,
    descripcion: str,
    agente_asignado: str,
    energia_requerida: int,
    prioridad: int = 1,
    creado_por: str = "sistema",
) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO misiones
            (titulo, descripcion, agente_asignado, estado,
             energia_requerida, prioridad, creado_por, created_at)
        VALUES (?, ?, ?, 'pendiente', ?, ?, ?, ?)
        """,
        (titulo, descripcion, agente_asignado, energia_requerida,
         prioridad, creado_por, created_at),
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return {
        "id": nuevo_id,
        "titulo": titulo,
        "descripcion": descripcion,
        "agente_asignado": agente_asignado,
        "estado": "pendiente",
        "energia_requerida": energia_requerida,
        "prioridad": prioridad,
        "creado_por": creado_por,
        "created_at": created_at,
    }


def obtener_mision(mision_id: int) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titulo, descripcion, agente_asignado, estado, "
        "energia_requerida, prioridad, creado_por, created_at "
        "FROM misiones WHERE id = ?",
        (mision_id,),
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
        "created_at": fila[8],
    }


def listar_misiones_de_agente(nombre_agente: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titulo, descripcion, agente_asignado, estado, "
        "energia_requerida, prioridad, creado_por, created_at "
        "FROM misiones WHERE agente_asignado = ? ORDER BY prioridad DESC, created_at",
        (nombre_agente,),
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
            "created_at": f[8],
        }
        for f in filas
    ]


def cambiar_estado_mision(mision_id: int, nuevo_estado: str) -> bool:
    estados_validos = {"pendiente", "en_curso", "completada", "fallida"}
    if nuevo_estado not in estados_validos:
        raise ValueError(f"Estado inválido: '{nuevo_estado}'. Válidos: {estados_validos}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE misiones SET estado = ? WHERE id = ?",
        (nuevo_estado, mision_id),
    )
    conn.commit()
    filas_afectadas = cursor.rowcount
    conn.close()
    return filas_afectadas > 0
