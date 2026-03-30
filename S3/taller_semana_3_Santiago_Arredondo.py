
# =========================
# Adaptación Semana 3: Modularización con funciones, type hints y alias de tipo
# =========================

import datetime
from typing import List, Dict

# =========================
# Alias de tipos para la memoria del agente
# =========================
# Usar alias de tipo como 'MemoriaAgente' ayuda a que el código sea más legible y mantenible, especialmente cuando trabajamos con modelos de IA o equipos grandes. Permite cambiar la estructura de la memoria en un solo lugar y mejora la autocompletación y validación de tipos.
Historial = Dict[str, str]  # Un recuerdo individual: cada comando ejecutado
MemoriaAgente = List[Historial]  # Toda la memoria del agente: lista de recuerdos

# =========================
# Función de login
# =========================
def login(nombre_usuario: str, clave: str) -> Dict[str, str]:
    """
    Valida las credenciales del usuario y retorna un diccionario con el rol y estado de acceso.
    """
    # Definición de credenciales válidas
    admin_user = "admin"
    admin_pass = "1234"
    guest_user = "invitado"
    guest_pass = "0000"
    # Verifica si las credenciales corresponden a admin
    if nombre_usuario == admin_user and clave == admin_pass:
        return {"rol": "admin", "access": "True", "descripcion": "Bienvenido, administrador."}
    # Verifica si las credenciales corresponden a invitado
    elif nombre_usuario == guest_user and clave == guest_pass:
        return {"rol": "invitado", "access": "True", "descripcion": "Bienvenido, invitado."}
    # Si no coincide, acceso denegado
    else:
        return {"rol": "", "access": "False", "descripcion": "Usuario o contraseña incorrectos."}

# =========================
# Función para registrar en el historial
# =========================
def registrar_historial(historial: MemoriaAgente, comando: str, rol_usuario: str, descripcion: str) -> None:
    """
    Agrega un registro al historial de comandos.
    """
    # Crea un nuevo registro con la información del comando
    d_log: Historial = {
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "cmd": comando,
        "rol": rol_usuario,
        "descripcion": descripcion
    }
    # Agrega el registro al historial
    historial.append(d_log)

# =========================
# Tool A: Función para gestionar el historial (sin print, solo return)
# =========================
def gestionar_historial(accion: str, memoria: MemoriaAgente) -> str:
    """
    Gestiona la memoria del agente: muestra todo, limpia o busca coincidencias.
    No imprime nada, solo retorna el string formateado.
    """
    partes = accion.split()
    # Si la acción es 'historial all', muestra todo el historial
    if len(partes) == 2 and partes[1] == "all":
        if len(memoria) == 0:
            return "[PseudoAgente] No hay historial para mostrar."
        else:
            # Formatea cada registro del historial
            resultado = [f"{i+1}. [{d['timestamp']}] ({d['rol']}) {d['cmd']}: {d['descripcion']}" for i, d in enumerate(memoria)]
            return "[PseudoAgente] Historial completo:\n" + "\n".join(resultado)
    # Si la acción es 'historial clear', borra el historial
    elif len(partes) == 2 and partes[1] == "clear":
        memoria.clear()
        return "[PseudoAgente] Historial borrado correctamente."
    # Si solo es 'historial', busca una palabra clave
    elif len(partes) == 1:
        if len(memoria) == 0:
            return "[PseudoAgente] No hay historial para buscar."
        else:
            palabra = input("Ingresa la palabra clave a buscar: ").lower()
            # Busca coincidencias en las descripciones
            encontrados = [f"[{d['timestamp']}] ({d['rol']}) {d['cmd']}: {d['descripcion']}" for d in memoria if palabra in d["descripcion"].lower()]
            if len(encontrados) == 0:
                return "[PseudoAgente] No encontré registros que coincidan con esa palabra."
            else:
                return f"[PseudoAgente] Se encontraron {len(encontrados)} coincidencia(s):\n" + "\n".join(encontrados)
    # Opción no reconocida
    else:
        return "[PseudoAgente] Opción de historial no reconocida. Usa 'historial', 'historial all' o 'historial clear'."

# =========================
# Función para el comando contar usando list comprehensions
# =========================
def comando_contar() -> str:
    """
    Solicita una palabra y cuenta letras, vocales y consonantes usando list comprehensions.
    """
    # Solicita la palabra al usuario
    palabra = input("Ingresa una palabra: ").lower()
    # Cuenta vocales usando list comprehension
    vocales = [l for l in palabra if l in "aeiou"]
    # Cuenta consonantes usando list comprehension
    consonantes = [l for l in palabra if l not in "aeiou"]
    tot_vocales = len(vocales)
    tot_cons = len(consonantes)
    tot_letras = len(palabra)
    # Muestra los resultados
    print(f"Palabra ingresada: {palabra}")
    print(f"Total de letras: {tot_letras}")
    print(f"Total de vocales: {tot_vocales}")
    print(f"Total de consonantes: {tot_cons}")
    return f"Se solicitó el conteo de la palabra {palabra}, dando como resultados:\nVocales: {tot_vocales}\nConsonantes: {tot_cons}\nTotal: {tot_letras}"

# =========================
# Función para el comando fecha_hoy
# =========================
# =========================
# Tool B: Función para fecha_hoy con raise PermissionError
# =========================
def comando_fecha_hoy(rol_usuario: str) -> str:
    """
    Muestra la fecha y hora actual solo si el usuario es admin.
    Si el usuario no es admin, lanza una excepción PermissionError.
    """
    # El siguiente raise lanza una excepción que viaja hasta el bucle principal, donde será atrapada por un bloque except específico.
    # Si el usuario no es admin, lanza un error de permisos
    if rol_usuario != "admin":
        raise PermissionError("Privilegios insuficientes")
    # Si es admin, retorna la fecha y hora actual
    mensaje_fecha = f"Se ha consultado la fecha actual: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    return mensaje_fecha

# =========================
# Función para el comando validar_pass
# =========================
def comando_validar_pass(nombre_usuario: str) -> str:
    """
    Valida una nueva contraseña propuesta por el usuario.
    """
    # Solicita la nueva contraseña
    nueva = input("Propuesta de nueva contraseña: ")
    # No puede ser igual al usuario
    if nueva == nombre_usuario:
        print("La contraseña no puede ser igual al nombre de usuario.")
        return "Intento fallido: la contraseña es igual al nombre de usuario."
    # Debe tener al menos 8 caracteres
    elif len(nueva) < 8:
        print("La contraseña debe tener al menos 8 caracteres.")
        return "Intento fallido: la contraseña tiene menos de 8 caracteres."
    # Si pasa las validaciones
    else:
        print("Contraseña válida.")
        return "Contraseña propuesta válida."

# =========================
# Función para el comando calculadora
# =========================
# =========================
# Tool B: Calculadora con manejo robusto de errores
# =========================
def comando_calculadora() -> str:
    """
    Realiza operaciones matemáticas básicas entre dos números. Lanza ValueError si el input no es válido.
    """
    # Solicita los números y el operador
    n1 = input("Ingresa el primer número: ")
    op = input("Ingresa el operador (+, -, *, /): ")
    n2 = input("Ingresa el segundo número: ")
    try:
        # Intenta convertir los inputs a float
        n1 = float(n1)
        n2 = float(n2)
    except ValueError as exc:
        # Si falla la conversión, relanza el error personalizado y mantiene el traceback original
        raise ValueError("Debes ingresar números válidos.") from exc
    # Realiza la operación según el operador
    if op == "+":
        resultado = n1 + n2
        return f"Se realizó una suma: {n1} + {n2} = {resultado}"
    elif op == "-":
        resultado = n1 - n2
        return f"Se realizó una resta: {n1} - {n2} = {resultado}"
    elif op == "*":
        resultado = n1 * n2
        return f"Se realizó una multiplicación: {n1} * {n2} = {resultado}"
    elif op == "/":
        # Verifica división por cero
        if n2 == 0:
            raise ValueError("No se puede dividir por cero.")
        resultado = n1 / n2
        return f"Se realizó una división: {n1} / {n2} = {resultado}"
    else:
        # Operador no válido
        raise ValueError("Operador no válido en la calculadora.")

# =========================
# Ejecución principal 
# =========================
# Inicialización de variables de control
intentos = 0
max_intentos = 3
logueado = False
rol = ""
usuario = ""
# Bucle de login con máximo 3 intentos
while intentos < max_intentos:
    usuario = input("Usuario: ").lower()
    password = input("Contraseña: ").lower()
    resultado_login = login(usuario, password)
    if resultado_login["access"] == "True":
        print(resultado_login["descripcion"])
        logueado = True
        rol = resultado_login["rol"]
        break
    else:
        print(resultado_login["descripcion"])
        intentos += 1
# Si no logra loguearse, termina el programa
if not logueado:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
else:
    # Mensaje de bienvenida y preparación de historial
    print("Bienvenido al pseudoagente de consola. Escribe 'salir' para terminar la sesión.")
    historial_chat: MemoriaAgente = []
    sistema_activo = True
    # Bucle principal del menú de comandos
    while sistema_activo:
        cmd = input("Agente>: ").lower()
        # Comando para gestionar el historial
        if cmd.startswith("historial"):
            mensaje = gestionar_historial(cmd, historial_chat)
            print(mensaje)
        # Comando para salir del sistema
        elif cmd == "salir":
            print("---Agente Apagado. Vuelve Pronto.-------")
            sistema_activo = False
            mensaje = "Se ha solicitado terminar la sesión."
        # Comando ping
        elif cmd == "ping":
            print("pong")
            mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
        # Comando contar letras, vocales y consonantes
        elif cmd == "contar":
            mensaje = comando_contar()
            print(mensaje)
        # Comando para mostrar la fecha (solo admin)
        elif cmd == "fecha_hoy":
            # Captura el error de permisos si el usuario no es admin
            try:
                mensaje = comando_fecha_hoy(rol)
                print(mensaje)
            except PermissionError as ex:
                mensaje = f"[PseudoAgente] {ex}"
                print(mensaje)
        # Comando para validar contraseña
        elif cmd == "validar_pass":
            mensaje = comando_validar_pass(usuario)
            print(mensaje)
        # Comando calculadora con manejo de errores
        elif cmd == "calculadora":
            try:
                mensaje = comando_calculadora()
                print(mensaje)
            except ValueError as ex:
                mensaje = f"[PseudoAgente] {ex}"
                print(mensaje)
        # Comando no reconocido
        else:
            mensaje = "Comando no existe. Intente de nuevo"
            print(mensaje)
        # Registra cada acción en el historial
        registrar_historial(historial_chat, cmd, rol, mensaje)