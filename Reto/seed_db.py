import sqlite3
from datetime import datetime
from pathlib import Path

# Conexión a la base de datos
DB_PATH = Path(__file__).resolve().parent / "agentes.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Crear tablas si no existen
c.execute('''CREATE TABLE IF NOT EXISTS agentes (
    nombre TEXT PRIMARY KEY,
    rol TEXT NOT NULL,
    energia INTEGER NOT NULL
)''')
c.execute('''CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    remitente TEXT,
    destinatario TEXT,
    contenido TEXT,
    timestamp TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS misiones (
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
)''')

# Insertar agentes
agentes = [
    ("AgenteX", "operativo", 100),
    ("AgenteY", "operativo", 80),
    ("Admin1", "admin", 200)
]
c.executemany("INSERT OR IGNORE INTO agentes (nombre, rol, energia) VALUES (?, ?, ?)", agentes)

# Insertar mensajes
mensajes = [
    ("AgenteX", "AgenteY", "Mensaje 1", datetime.now().isoformat()),
    ("AgenteY", "AgenteX", "Mensaje 2", datetime.now().isoformat()),
    ("Admin1", "AgenteX", "Mensaje 3", datetime.now().isoformat()),
    ("AgenteX", "Admin1", "Mensaje 4", datetime.now().isoformat()),
    ("AgenteY", "Admin1", "Mensaje 5", datetime.now().isoformat()),
]
c.executemany("INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) VALUES (?, ?, ?, ?)", mensajes)

# Insertar misiones
misiones = [
    ("Misión 1", "Desc. 1", "AgenteX", "pendiente", 10, "alta", "2026-04-20", 100, datetime.now().isoformat()),
    ("Misión 2", "Desc. 2", "AgenteY", "en_curso", 20, "media", "2026-04-22", 150, datetime.now().isoformat()),
    ("Misión 3", "Desc. 3", "Admin1", "completada", 30, "baja", "2026-04-25", 200, datetime.now().isoformat()),
]
c.executemany("""
    INSERT INTO misiones (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, deadline, recompensa, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", misiones)

conn.commit()
conn.close()
print("Datos semilla insertados correctamente en", DB_PATH)
