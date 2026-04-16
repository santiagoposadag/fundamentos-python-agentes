# seed.py
# Pobla la base de datos con datos de ejemplo para el reto.
# Ejecutar una sola vez: python seed.py
# Si se vuelve a ejecutar, los agentes duplicados se ignoran (PRIMARY KEY).

from db import crear_tablas, registrar_agente, enviar_mensaje, crear_mision
import sqlite3
from config import DB_PATH

print("[Seed] Iniciando carga de datos de ejemplo...")

crear_tablas()

# --- 3 agentes ---
print("\n[Seed] Registrando agentes...")

print(registrar_agente("Atlas", "explorador", 200))
print(registrar_agente("Nova", "cientifica", 150))
print(registrar_agente("Titan", "admin", 300))

# --- 5 mensajes ---
print("\n[Seed] Enviando mensajes...")

print(enviar_mensaje("Atlas", "Nova", "Encontre una senal extrania en el sector 7. Podrias analizarla?"))
print(enviar_mensaje("Nova", "Atlas", "Recibido. Analizando la senal. Resultados en 2 horas."))
print(enviar_mensaje("Titan", "Atlas", "Atlas, mantente en posicion. El perimetro no esta asegurado."))
print(enviar_mensaje("Titan", "Nova", "Nova, necesito el analisis de la senal antes de las 18:00."))
print(enviar_mensaje("Nova", "Titan", "Entendido. El analisis revela una frecuencia de comunicacion enemiga."))

# --- 3 misiones en estados distintos ---
print("\n[Seed] Creando misiones...")

# Mision 1: pendiente
id_m1 = crear_mision(
    titulo="Reconocimiento sector norte",
    descripcion="Mapear y documentar instalaciones en el sector norte sin ser detectado.",
    agente_asignado="Atlas",
    energia_requerida=40,
    prioridad="alta",
    creado_por="Titan"
)
print(f"  Mision #{id_m1} creada: pendiente")

# Mision 2: la creamos y la marcamos como completada directamente
id_m2 = crear_mision(
    titulo="Analisis de senal enemiga",
    descripcion="Decodificar la frecuencia de comunicacion detectada en el sector 7.",
    agente_asignado="Nova",
    energia_requerida=50,
    prioridad="media",
    creado_por="Titan"
)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("UPDATE misiones SET estado = 'completada' WHERE id = ?", (id_m2,))
cursor.execute("UPDATE agentes SET energia = energia - 50 WHERE nombre = 'Nova'")
conn.commit()
conn.close()
print(f"  Mision #{id_m2} creada: completada")

# Mision 3: fallida
id_m3 = crear_mision(
    titulo="Intercepcion de convoy",
    descripcion="Interceptar el convoy enemigo en el punto de control Delta.",
    agente_asignado="Atlas",
    energia_requerida=80,
    prioridad="baja",
    creado_por="Titan"
)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("UPDATE misiones SET estado = 'fallida' WHERE id = ?", (id_m3,))
conn.commit()
conn.close()
print(f"  Mision #{id_m3} creada: fallida")

print("\n[Seed] Listo. Base de datos poblada.")
print(f"  - 3 agentes: Atlas, Nova, Titan")
print(f"  - 5 mensajes entre agentes")
print(f"  - 3 misiones: pendiente, completada, fallida")
