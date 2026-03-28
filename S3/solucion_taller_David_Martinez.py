from datetime import date, datetime

# Declaracion de las variables globales a usar
user_invitado = "invitado"
password_invitado = "123"

user_admin = "admin"
password_admin = "4dm1n"

user = ""
password = ""
sistema_activo = False

# definicion de types y alias para hacer explicita la estructura del contexto, lo cual es muy importante en IA
Recuerdo = dict[str, str]
MemoriaAgente = list[Recuerdo]

# la memoria del agente es una lista de recuerdos
memoria: MemoriaAgente = []

# definicion de funciones (tools)
def guardarRecuerdo(cmd: str, user: str, descripcion: str) -> None:
    """
    Crea un recuerdo con información del comando ejecutado y lo almacena en la memoria global

    Args:
        cmd (str): comando ejecutado por el usuario
        user (str): usuario logeado
        descripcion (str): resultado del comando ejecutado

    Returns:
        None
    """
    recuerdo: Recuerdo = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cmd": cmd,
        "rol": user,
        "descripcion": descripcion,
    }
    memoria.append(recuerdo)


def contar(palabra: str) -> str:
    """
    Cuenta la cantidad de vocales, consonantes y letras de una palabra
    se transforma todo a minusculas

    Args:
        palabra (str): Palabra a analizar

    Returns:
        str: Resumen con el total de vocales, consonantes y letras
    """
    tot_letras = len(palabra)
    tot_vocales = 0
    tot_cons = 0

    for p in palabra:
        if p in "aeiou":
            tot_vocales += 1
        else:
            tot_cons += 1

    resultado = f"""Palabra ingresada: {palabra}
        Total de vocales: {tot_vocales}
        Total de consonantes: {tot_cons}
        Total de letras: {tot_letras}"""

    return resultado


def validar_password(potential_pass: str, user: str) -> str:
    """
    Valida si una contraseña cumple con los requisitos mínimos de seguridad
    ebe tener al menos 8 caracteres y no puede ser igual al usuario

    Args:
        potential_pass (str): Contraseña a validar

    Returns:
        str: Mensaje indicando si la contraseña es válida o no
    """
    if len(potential_pass) >= 8 and potential_pass != user:
        resultado = "La nueva contraseña es Valida."
    else:
        resultado = "La nueva contraseña NO es Valida. \n(Debe contener almenos 8 caracteres y no puede ser ser igual a su nombre de usuario)"
    
    return resultado


def get_fecha_actual(user: str) -> str:
    """
    Obtiene la fecha actual si el usuario tiene permisos de administrador

    Returns:
        str: Fecha actual en formato YYYY-MM-DD

    Raises:
        PermissionError: Si el usuario no tiene privilegios suficientes
    """
    if user == "admin":
        resultado = f"La fecha actual es: {date.today()}"
    else:
        raise PermissionError("[Acceso Denegado] Privilegios insuficientes")

    return resultado


def calcular(numero1: int, numero2: int, operador: str) -> str:
    """
    Realiza las 4 operaciones basicas aritmeticas de una calculadora entre dos números enteros

    Args:
        numero1 (int): Primer número
        numero2 (int): Segundo número
        operador (str): Operador matemático (+, -, *, /)

    Returns:
        str: Resultado de la operación en formato texto

    Raises:
        ZeroDivisionError: Si se intenta dividir por cero
        ValueError: Si el operador no es válido
    """
    if operador == "+":
        resultado = f"{numero1} + {numero2} = {numero1 + numero2}"
    elif operador == "-":
        resultado = f"{numero1} - {numero2} = {numero1 - numero2}"
    elif operador == "*":
        resultado = f"{numero1} * {numero2} = {numero1 * numero2}"
    elif operador == "/":
        try:
            resultado = f"{numero1} / {numero2} = {numero1 / numero2}"
        except ZeroDivisionError as ex:
            raise ex
    else:
        raise ValueError("El Operador ingresado No es valido.")
    
    return resultado


def geationar_historial(action: str, historial: MemoriaAgente, search_word: str = "") -> str:
    """
    Gestiona el historial de la memoria del agente según la acción indicada

    Args:
        action (str): Acción a ejecutar:
            - "all": Retorna todo el historial
            - "clear": Limpia el historial
            - cualquier otro valor: Busca coincidencias.
        historial (MemoriaAgente): Lista de recuerdos del agente.
        search_word (str, optional): Palabra a buscar en las descripciones

    Returns:
        str: Resultado de la acción (historial completo, mensaje de historial limpiado o coincidencias encontradas)
    """
    if action == "all":
        return str(historial)
    elif action == "clear":
        historial.clear()
        return "[PseudoAgente] Historial eliminado"
    else:
        coincidencias = []
        for item in historial:
            descripcion = str(item["descripcion"])
            if search_word.lower() in descripcion.lower():
                coincidencias.append(item)
        if len(coincidencias) > 0:
            resultado = f"Se encontro {len(coincidencias)} coincidencia(s)\n{coincidencias}"
        else:
            resultado = "[PseudoAgente] No encontré registros que coincidan con esa palabra."
    
    return resultado

print("\n----- Iniciando el pseudoagente estilo consola -------")

# Implementacion del login con 3 intentos
for i in range(3):
    user = input("Ingrese usuario: ")
    password = input("Ingrese contraseña: ")
    if (user_invitado == user and password_invitado == password) or (
        user_admin == user and password_admin == password
    ):
        sistema_activo = True
        break
    else:
        print("\nUsuario y/o contraseña equivocado. Intente nuevamente\n")

if not sistema_activo:
    print("[Alerta] Usuario bloqueado. Cerrando sistema...")
else:
    print(f"[Sistema] Acceso concedido. Modo {user}")

# Implementacion del Agente con 6 opciones disponibles
while sistema_activo:
    cmd = input("\nAgente>: ").lower()

    if cmd == "salir":
        sistema_activo = False
        print("\n------Agente apagado. Vuelve pronto------")
        guardarRecuerdo(cmd, user, "Se ha solicitado terminar la sesión.")
    elif cmd == "ping":
        print("pong.")
        guardarRecuerdo(cmd, user, "Se ha enviado un ping y de respuesta se devolvió un pong.")
    elif cmd == "contar":
        palabra = input("Ingrese una palabra: ").lower()
        result = contar(palabra)
        print(result)
        guardarRecuerdo(cmd, user, result)
    elif cmd == "fecha_hoy":
        try:
            result = get_fecha_actual(user)
            print(result)
            guardarRecuerdo(cmd, user, result)
        except PermissionError as ex:
            print(ex)
    elif cmd == "validar_pass":
        potential_pass = input("Ingrese nueva contraseña: ")
        result = validar_password(potential_pass, user)
        print(result)
        guardarRecuerdo(cmd, user, result)
    elif cmd == "calculadora":
        numero1 = int(input("Ingrese el primer numero: "))
        operador = input("Ingresa el operador (+, -, *, /): ")
        numero2 = int(input("Ingresa el segundo número: "))
        try:
            result = calcular(numero1, numero2, operador)
            print(result)
            guardarRecuerdo(cmd, user, result)
        except (ZeroDivisionError, ValueError) as ex:
            print(ex)
    # No se agregan los comandos de historial de la memoria, para evitar que se vuelva muy redundante en las busquedas
    elif cmd == "historial all":
        result = geationar_historial("all", memoria)
        print(result)
    elif cmd == "historial clear":
        result = geationar_historial("clear", memoria)
        print(result)
    elif cmd == "historial":
        word = input("Ingrese la palabra clave a buscar: ")
        result = geationar_historial("", memoria, word)
        print(result)
    else:
        print("Comando desconocido, intente de nuevo.")
