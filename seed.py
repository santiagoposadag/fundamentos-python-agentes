# seed.py - Siembra la base de datos con datos iniciales para la demostración.
# Ejecutar UNA vez antes de lanzar el servidor:
#     python seed.py
#
# Idempotente para agentes (PRIMARY KEY previene duplicados).
# Para mensajes y misiones solo inserta si hay menos datos que el mínimo requerido.

import sqlite3
import db

print("[Seed] Creando tablas...")
db.crear_tablas()

# ──────────────────────────────────────────────
# AGENTES  (mínimo: 3, incluyendo uno con rol 'admin')
# ──────────────────────────────────────────────
print("\n[Seed] Registrando agentes...")
agentes = [
    ("Lyra",   "admin",       300),
    ("Nova",   "cientifica",  180),
    ("Titan",  "guardian",    250),
    ("Hermes", "mensajero",   120),
]
for nombre, rol, energia in agentes:
    resultado = db.registrar_agente(nombre, rol, energia)
    print(f"  {resultado}")

# ──────────────────────────────────────────────
# MENSAJES  (mínimo: 5)
# ──────────────────────────────────────────────
conn = sqlite3.connect(db.DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM mensajes")
total_mensajes = cursor.fetchone()[0]
conn.close()

if total_mensajes < 5:
    print("\n[Seed] Enviando mensajes...")
    mensajes = [
        ("Lyra",   "Nova",   "Iniciar análisis del artefacto recuperado."),
        ("Nova",   "Lyra",   "Análisis completado. Resultados en archivo 7-B."),
        ("Titan",  "Lyra",   "Perímetro norte asegurado. Sin amenazas."),
        ("Hermes", "Titan",  "Nueva ruta de extracción habilitada."),
        ("Nova",   "Hermes", "Necesito transporte urgente al laboratorio."),
    ]
    for remitente, destinatario, contenido in mensajes:
        resultado = db.enviar_mensaje(remitente, destinatario, contenido)
        print(f"  {resultado}")
else:
    print(f"\n[Seed] Ya existen {total_mensajes} mensajes. Se omite la siembra de mensajes.")

# ──────────────────────────────────────────────
# MISIONES  (mínimo: 3 en estados distintos)
# ──────────────────────────────────────────────
conn = sqlite3.connect(db.DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM misiones")
total_misiones = cursor.fetchone()[0]
conn.close()

if total_misiones < 3:
    print("\n[Seed] Creando misiones...")

    # Misión 1 — completada (Lyra la ejecutó, ya se descontó energía)
    id1 = db.crear_mision(
        titulo="Reconocimiento Zona Alfa",
        descripcion="Mapear el sector norte antes del amanecer.",
        agente_asignado="Lyra",
        estado="completada",
        energia_requerida=40,
        prioridad="alta",
        recompensa=15,
        creado_por="seed",
    )
    # Reflejar el descuento de energía en la BD para coherencia
    agente_lyra = db.despertar_agente("Lyra")
    if agente_lyra:
        db.actualizar_energia_agente("Lyra", agente_lyra["energia"] - 40)
    print(f"  Misión id={id1} creada (estado: completada).")

    # Misión 2 — en_curso (Titan trabajando en ello)
    id2 = db.crear_mision(
        titulo="Defensa del Núcleo",
        descripcion="Mantener el perímetro activo durante 48 horas.",
        agente_asignado="Titan",
        estado="en_curso",
        energia_requerida=80,
        prioridad="alta",
        recompensa=30,
        creado_por="seed",
    )
    print(f"  Misión id={id2} creada (estado: en_curso).")

    # Misión 3 — pendiente (Nova esperando asignación)
    id3 = db.crear_mision(
        titulo="Síntesis del Compuesto X",
        descripcion="Desarrollar el antídoto usando los datos del archivo 7-B.",
        agente_asignado="Nova",
        estado="pendiente",
        energia_requerida=60,
        prioridad="media",
        recompensa=25,
        creado_por="seed",
    )
    print(f"  Misión id={id3} creada (estado: pendiente).")
else:
    print(f"\n[Seed] Ya existen {total_misiones} misiones. Se omite la siembra de misiones.")

# ──────────────────────────────────────────────
# RESUMEN
# ──────────────────────────────────────────────
print("\n[Seed] Estado final de la base de datos:")
agentes_bd = db.listar_agentes()
print(f"  Agentes   : {len(agentes_bd)}")
for a in agentes_bd:
    print(f"    · {a['nombre']} | rol={a['rol']} | energía={a['energia']}")

conn = sqlite3.connect(db.DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM mensajes")
n_mensajes = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM misiones")
n_misiones = cursor.fetchone()[0]
cursor.execute("SELECT estado, COUNT(*) FROM misiones GROUP BY estado")
estados = cursor.fetchall()
conn.close()

print(f"  Mensajes  : {n_mensajes}")
print(f"  Misiones  : {n_misiones} {dict(estados)}")
print("\n[Seed] ¡Listo! Ahora puedes lanzar el servidor con: uvicorn main:app --reload")
