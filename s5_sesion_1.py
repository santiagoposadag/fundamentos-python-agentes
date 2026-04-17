# -----------------------------------------------------------#
# Semana 5 - Sesion 1: Persistencia con SQLite
# -----------------------------------------------------------#
# Hasta ahora, cada vez que cierras Python, todo desaparece.
# Los agentes, los mensajes, los datos... se pierden en la RAM.
# Hoy aprenderemos a darle MEMORIA PERMANENTE a nuestros agentes
# usando SQLite: una base de datos que vive en un solo archivo.
#
# Instrucciones:
# 1. Lee cada capitulo de arriba hacia abajo
# 2. Descomenta el bloque de codigo indicado
# 3. Ejecuta el script completo: python S5_sesion_1.py
# 4. Observa la salida, experimenta, y escribe tu CONCLUSION
# 5. Avanza al siguiente capitulo
# -----------------------------------------------------------#

import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentes.db")

# -----------------------------------------------------------#
# SECCION A: Funciones del modulo (siempre disponibles)
# -----------------------------------------------------------#
# Estas funciones NO estan comentadas porque otros archivos
# las importan. No las modifiques a menos que se indique.
# -----------------------------------------------------------#


def crear_tablas() -> None:
    """Crea las tablas agentes y mensajes si no existen."""
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
    conn.commit()
    conn.close()


def registrar_agente(nombre: str, rol: str, energia: int) -> str:
    """Registra un agente en la base de datos. Retorna mensaje de exito o error."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO agentes (nombre, rol, energia) VALUES (?, ?, ?)",
            (nombre, rol, energia),
        )
        conn.commit()
        resultado = f"[DB] Agente '{nombre}' registrado con exito."
    except sqlite3.IntegrityError:
        resultado = f"[DB] Error: El agente '{nombre}' ya existe en la base de datos."
    finally:
        conn.close()
    return resultado


def despertar_agente(nombre: str) -> dict | None:
    """Busca un agente por nombre. Retorna dict o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return {"nombre": fila[0], "rol": fila[1], "energia": fila[2]}


def enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str:
    """Inserta un mensaje en la tabla mensajes con timestamp automatico."""
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
    """Retorna una lista con todos los agentes registrados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol, energia FROM agentes")
    filas = cursor.fetchall()
    conn.close()
    return [
        {"nombre": f[0], "rol": f[1], "energia": f[2]}
        for f in filas
    ]


# -----------------------------------------------------------#
# SECCION B: Ejercicios guiados (descomenta capitulo a capitulo)
# -----------------------------------------------------------#

if __name__ == "__main__":

    # ======================================================
    # CAPITULO 1: El problema de la amnesia (5 min)
    # ======================================================
    # Cada vez que ejecutas un script de Python, las variables
    # viven en la RAM. Cuando el script termina, la RAM se libera
    # y todo desaparece. Observa:

    agente = {"nombre": "Atlas", "rol": "explorador", "energia": 100}
    print(f"Agente creado: {agente}")
    print("Script terminado. ¿Donde quedo el agente Atlas? En ningun lado. La RAM se borro.")

    # PRUEBA: Vuelve a ejecutar el script. Atlas nace de cero cada vez. Eso es amnesia.
    # CONCLUSION: Se comprobó que las variables en Python viven únicamente en la memoria RAM.
    # Cada vez que el programa termina, la memoria se libera y los datos desaparecen.
    # Esto demuestra que sin un mecanismo de persistencia, la información no se conserva
    # entre ejecuciones del programa.

    # ======================================================
    # CAPITULO 2: SQL en 5 minutos (10 min)
    # ======================================================
    # SQLite es una base de datos que vive en UN SOLO ARCHIVO.
    # No necesitas instalar nada: Python ya lo trae incluido.
    # CREATE TABLE IF NOT EXISTS crea la tabla solo si no existe.
    # Esto significa que puedes ejecutar este codigo muchas veces
    # sin que se rompa nada.

    # --- Descomenta el siguiente bloque, ejecuta y observa ---
    crear_tablas()
    print(f"[Sistema] Tablas creadas. ¿Existe el archivo? {os.path.exists(DB_PATH)}")
    print(f"[Sistema] Archivo de base de datos: {DB_PATH}")

    # PRUEBA: Busca el archivo agentes.db en tu carpeta S5/. Abrelo con un editor de texto. ¿Que ves? (Nada legible, es binario.)
    # CONCLUSION: Se comprobó que SQLite crea un archivo físico que almacena la base de datos. Este archivo permanece en el sistema
    # incluso después de cerrar el programa. Además, el uso de CREATE TABLE IF NOT EXISTS permite ejecutar el script múltiples
    # veces sin generar errores, garantizando que la estructura de la base de datos exista sin duplicarse.

    # ======================================================
    # CAPITULO 3: Registrar un agente (10 min)
    # ======================================================
    # INSERT INTO agentes ... inserta una fila nueva.
    # El ? es un PARAMETRO: SQLite reemplaza cada ? por el valor
    # correspondiente de la tupla. NUNCA uses f-strings en SQL
    # porque es vulnerable a inyeccion SQL.
    # Si el nombre ya existe (PRIMARY KEY), salta IntegrityError.

    # --- Descomenta el siguiente bloque, ejecuta y observa ---
    print(registrar_agente("Atlas", "explorador", 100))
    print(registrar_agente("Nova", "cientifica", 150))
    print(registrar_agente("Titan", "guardian", 200))
    print(registrar_agente("Hermes", "Mensajero", 250))

    # PRUEBA: Intenta registrar 'Atlas' dos veces. ¿Que mensaje recibes? ¿Por que?
    # CONCLUSION: Se verificó que la clave primaria (PRIMARY KEY) impide duplicar registros con el mismo nombre.
    # Al intentar registrar un agente existente, SQLite lanza una excepción (IntegrityError), lo que confirma que
    # la base de datos protege la integridad de los datos.

    # ======================================================
    # CAPITULO 4: Despertar un agente (10 min)
    # ======================================================
    # SELECT busca datos en la tabla. fetchone() retorna UNA fila
    # como tupla, o None si no hay resultados.
    # Convertimos la tupla a dict para que sea mas facil de usar.
    # Lo importante: los datos PERSISTEN entre ejecuciones.

    # --- Descomenta el siguiente bloque, ejecuta y observa ---
    datos_atlas = despertar_agente("Atlas")
    print(f"Agente encontrado: {datos_atlas}")
    print("Ahora cierra Python (Ctrl+C o cierra la terminal).")
    print("Vuelve a abrir y ejecuta SOLO este capitulo. El agente sigue ahi.")

    datos_fantasma = despertar_agente("NoExisto")
    print(f"Agente inexistente: {datos_fantasma}")

    # PRUEBA: Cierra Python completamente. Vuelve a abrir. Ejecuta despertar_agente('Atlas'). ¿Sigue vivo?
    # CONCLUSION: Se confirmó que los datos almacenados en SQLite persisten entre ejecuciones del programa.
    # A diferencia de las variables en RAM, los registros guardados en la base de datos permanecen disponibles
    # incluso después de cerrar el entorno. Esto demuestra el concepto de persistencia de datos.

    # ======================================================
    # CAPITULO 5: La tabla de mensajes (10 min)
    # ======================================================
    # La tabla mensajes tiene un id autoincrementable: cada mensaje
    # recibe un numero unico automaticamente. El timestamp se genera
    # con datetime.now().isoformat() al momento de enviar.
    # Esto permite tener un historial ordenado de comunicaciones.

    # --- Descomenta el siguiente bloque, ejecuta y observa ---
    print(enviar_mensaje("Atlas", "Nova", "Encontre un artefacto en la cueva norte."))
    print(enviar_mensaje("Nova", "Atlas", "Excelente. Enviare un drone de analisis."))
    print(enviar_mensaje("Titan", "Nova", "Perimetro asegurado. Sin amenazas detectadas."))
    print(enviar_mensaje("Atlas", "Atlas", "Hola, soy Atlas"))
    print(enviar_mensaje("Atlas", "Hermes", "Hermes,  envía este mensaje a Nova: 'El artefacto es una fuente de energia desconocida.'"))
    print(enviar_mensaje("Nova", "Hermes", "Hermes, envía este mensaje a Atlas: 'Recibido, mantente alerta. Investigaré el artefacto desde aquí.'"))

    # PRUEBA: Envia un mensaje de Atlas a si mismo. ¿Funciona? ¿Deberia?
    # CONCLUSION: Se comprobó que la tabla de mensajes permite almacenar un historial completo de comunicaciones.
    # El campo id autoincrementable garantiza unicidad, y el timestamp permite registrar el momento exacto del envío.
    # El sistema no impide que un agente se envíe mensajes a sí mismo, lo cual es válido desde el punto de vista técnico,
    # aunque podría regularse según reglas de negocio.

    # ======================================================
    # CAPITULO 6: Bandeja de entrada (10 min)
    # ======================================================
    # SELECT ... WHERE destinatario = ? filtra los mensajes
    # dirigidos a un agente especifico. ORDER BY timestamp los
    # ordena cronologicamente. fetchall() retorna TODAS las filas.

    # --- Descomenta el siguiente bloque, ejecuta y observa ---
    mensajes_nova = leer_mensajes("Nova")
    print(f"\n--- Bandeja de entrada de Nova ({len(mensajes_nova)} mensajes) ---")
    for msg in mensajes_nova:
        print(f"  [{msg['timestamp']}] {msg['remitente']} -> {msg['contenido']}")

    mensajes_nova = leer_mensajes("Hermes")
    print(f"\n--- Bandeja de entrada de Hermes ({len(mensajes_nova)} mensajes) ---")
    for msg in mensajes_nova:
        print(f"  [{msg['timestamp']}] {msg['remitente']} -> {msg['contenido']}")

    # PRUEBA: Crea un tercer agente 'Hermes'. Envia mensajes desde Atlas y Nova a Hermes. Lee la bandeja de Hermes.
    # CONCLUSION: Se verificó que la consulta con WHERE destinatario = ?, filtra correctamente los mensajes dirigidos a un agente específico.
    # La cláusula ORDER BY timestamp permite organizar los mensajes cronológicamente, construyendo una bandeja
    # de entrada funcional basada en datos persistentes.

    # ======================================================
    # CAPITULO 7: Experimentacion libre (5 min)
    # ======================================================
    # Ahora que conoces las funciones, crea tu propio escenario.
    # Aqui tienes un mini-script de ejemplo que combina todo:

    # --- Descomenta el siguiente bloque, ejecuta y observa ---
    crear_tablas()
    print(registrar_agente("Hermes", "mensajero", 120))
    print(registrar_agente("Lyra", "diplomata", 90))

    print(enviar_mensaje("Hermes", "Lyra", "Tienes un mensaje del consejo."))
    print(enviar_mensaje("Lyra", "Hermes", "Recibido. Preparare la respuesta."))
    print(enviar_mensaje("Atlas", "Hermes", "Necesito que lleves esto a Lyra."))

    print("\n--- Todos los agentes registrados ---")
    for agente in listar_agentes():
        print(f"  {agente['nombre']} | Rol: {agente['rol']} | Energia: {agente['energia']}")

    print("\n--- Bandeja de Hermes ---")
    for msg in leer_mensajes("Hermes"):
        print(f"  [{msg['timestamp']}] {msg['remitente']} -> {msg['contenido']}")

    # PRUEBA: Cierra Python. Vuelve a abrir. ¿Siguen los mensajes? ¿Y los agentes?
    # CONCLUSION: Se confirmó que el sistema completo funciona de manera integrada. Los agentes registrados y los mensajes
    # enviados permanecen almacenados en la base de datos incluso después de cerrar el programa. Esto demuestra que
    # SQLite permite construir aplicaciones con memoria permanente y estructura organizada.

    # -----------------------------------------------------------#
    # Felicidades! Ya sabes persistir datos con SQLite.
    # En la proxima sesion conectaremos estas funciones a una API
    # web con FastAPI para que otros programas puedan hablar con
    # nuestros agentes a traves de HTTP.
    # -----------------------------------------------------------#
