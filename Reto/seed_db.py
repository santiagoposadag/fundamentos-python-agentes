import sqlite3
import datetime

DB_PATH = "agentes.db"

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS agentes")
    cursor.execute("DROP TABLE IF EXISTS mensajes")
    cursor.execute("DROP TABLE IF EXISTS misiones")
    
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
            prioridad TEXT DEFAULT 'normal',
            created_at TEXT
        )
    """)

    agentes = [
        ("Athena", "admin", 150),
        ("Mars", "explorador", 100),
        ("Apollo", "diplomata", 80)
    ]
    cursor.executemany("INSERT INTO agentes VALUES (?, ?, ?)", agentes)

    mensajes = [
        ("Athena", "Mars", "Explora la zona norte, se detectó actividad.", datetime.datetime.now().isoformat()),
        ("Mars", "Athena", "En camino. El terreno se ve estable.", datetime.datetime.now().isoformat()),
        ("Apollo", "Athena", "La reunión con el consejo fue exitosa.", datetime.datetime.now().isoformat()),
        ("Athena", "Apollo", "Excelente. Prepárate para el siguiente briefing.", datetime.datetime.now().isoformat()),
        ("Mars", "Apollo", "¿Tienes suministros extra?", datetime.datetime.now().isoformat())
    ]
    cursor.executemany("INSERT INTO mensajes (remitente, destinatario, contenido, timestamp) VALUES (?, ?, ?, ?)", mensajes)
    misiones = [
        ("Exploración Glaciar", "Mapear el sector G-12", "Mars", "en_curso", 40, "alta", datetime.datetime.now().isoformat()),
        ("Protocolo Paz", "Entregar documento al consejo", "Apollo", "pendiente", 20, "media", datetime.datetime.now().isoformat()),
        ("Auditoría de Sistemas", "Verificar logs de energía", "Athena", "completada", 0, "baja", datetime.datetime.now().isoformat())
    ]
    cursor.executemany("""
        INSERT INTO misiones (titulo, descripcion, agente_asignado, estado, energia_requerida, prioridad, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, misiones)

    conn.commit()
    conn.close()
    print("Base de datos sembrada con éxito.")

if __name__ == "__main__":
    seed()
