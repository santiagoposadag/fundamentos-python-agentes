"""
db.py - Capa de Infraestructura (Persistencia)

Este módulo gestiona la conexión con SQLite y realiza las operaciones CRUD.
No contiene lógica de negocio, solo persistencia de datos.
"""

import sqlite3
from typing import Any, Dict, List, Optional
from datetime import datetime

DATABASE_NAME = "agentes.db"

def obtener_conexion():
    """Crea una conexión a la base de datos con soporte para diccionarios."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Permite acceder por nombre de columna
    return conn

def inicializar_db():
    """Crea las tablas necesarias si no existen."""
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        
        # Tabla de Agentes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agentes (
                nombre TEXT PRIMARY KEY,
                tokens INTEGER DEFAULT 100,
                rol TEXT DEFAULT 'invitado'
            )
        """)
        
        # Tabla de Mensajes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remitente TEXT,
                destinatario TEXT,
                contenido TEXT,
                timestamp TEXT,
                FOREIGN KEY(remitente) REFERENCES agentes(nombre),
                FOREIGN KEY(destinatario) REFERENCES agentes(nombre)
            )
        """)
        
        # Tabla de Misiones (Requerimiento R3)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS misiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                agente_asignado TEXT,
                estado TEXT DEFAULT 'pendiente',
                energia_requerida INTEGER DEFAULT 10,
                created_at TEXT,
                FOREIGN KEY(agente_asignado) REFERENCES agentes(nombre)
            )
        """)
        conn.commit()

# --- Operaciones para Agentes ---

def upsert_agente(nombre: str, tokens: int, rol: str):
    with obtener_conexion() as conn:
        conn.execute("""
            INSERT INTO agentes (nombre, tokens, rol)
            VALUES (?, ?, ?)
            ON CONFLICT(nombre) DO UPDATE SET
                tokens = excluded.tokens,
                rol = excluded.rol
        """, (nombre, tokens, rol))

def obtener_agente(nombre: str) -> Optional[Dict[str, Any]]:
    with obtener_conexion() as conn:
        row = conn.execute("SELECT * FROM agentes WHERE nombre = ?", (nombre,)).fetchone()
        return dict(row) if row else None

def listar_agentes() -> List[Dict[str, Any]]:
    with obtener_conexion() as conn:
        rows = conn.execute("SELECT * FROM agentes").fetchall()
        return [dict(r) for r in rows]

# --- Operaciones para Mensajes ---

def registrar_mensaje(remitente: str, destinatario: str, contenido: str):
    with obtener_conexion() as conn:
        conn.execute("""
            INSERT INTO mensajes (remitente, destinatario, contenido, timestamp)
            VALUES (?, ?, ?, ?)
        """, (remitente, destinatario, contenido, datetime.now().isoformat()))

def listar_mensajes_agente(nombre: str) -> List[Dict[str, Any]]:
    with obtener_conexion() as conn:
        rows = conn.execute("""
            SELECT * FROM mensajes 
            WHERE remitente = ? OR destinatario = ?
            ORDER BY timestamp DESC
        """, (nombre, nombre)).fetchall()
        return [dict(r) for r in rows]

# --- Operaciones para Misiones (Requerimiento R4) ---

def crear_mision(titulo: str, descripcion: str, agente_asignado: str, energia: int):
    with obtener_conexion() as conn:
        cursor = conn.execute("""
            INSERT INTO misiones (titulo, descripcion, agente_asignado, energia_requerida, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (titulo, descripcion, agente_asignado, energia, datetime.now().isoformat()))
        return cursor.lastrowid

def obtener_mision(mision_id: int) -> Optional[Dict[str, Any]]:
    with obtener_conexion() as conn:
        row = conn.execute("SELECT * FROM misiones WHERE id = ?", (mision_id,)).fetchone()
        return dict(row) if row else None

def listar_misiones_agente(nombre: str) -> List[Dict[str, Any]]:
    with obtener_conexion() as conn:
        rows = conn.execute("SELECT * FROM misiones WHERE agente_asignado = ?", (nombre,)).fetchall()
        return [dict(r) for r in rows]

def actualizar_estado_mision(mision_id: int, estado: str):
    with obtener_conexion() as conn:
        conn.execute("UPDATE misiones SET estado = ? WHERE id = ?", (estado, mision_id))
