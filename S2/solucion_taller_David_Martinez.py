from datetime import date, datetime

# Declaracion de las variables globales a usar
user_invitado = "invitado"
password_invitado = "123"

user_admin = "admin"
password_admin = "4dm1n"

user = ""
password = ""
historial_chat = []
sistema_activo = False

print("\n----- Iniciando el pseudoagente estilo consola -------")

# Implementacion del login con 3 intentos usando un for y rompiendo el ciclo con break si usuario y password son correctos,
# para que no siga pidiendolos, se usa la misma variable de sistema_activo para bloquear el sistema o iniciar el agente,
# con sus respectivos mensajes de validacion
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
    mensaje = ""
    cmd = input("\nAgente>: ").lower()

    if cmd == "salir":
        sistema_activo = False
        print("\n------Agente apagado. Vuelve pronto------")
        mensaje = "Se ha solicitado terminar la sesión."
    elif cmd == "ping":
        print("pong.")
        mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
    elif cmd == "contar":
        palabra = input("Ingrese una palabra: ").lower()
        tot_letras = len(palabra)
        tot_vocales = 0
        tot_cons = 0

        for p in palabra:
            if p in "aeiou":
                tot_vocales += 1
            else:
                tot_cons += 1

        print(f"Palabra ingresada: {palabra}")
        print(f"Total de vocales: {tot_vocales}")
        print(f"Total de consonantes: {tot_cons}")
        print(f"Total de letras: {tot_letras}")
        mensaje = f"""Se solicitó el conteo de la palabra {palabra}, dando como resultados:
            Vocales: {tot_vocales}
            Consonantes: {tot_cons}
            Total: {tot_letras}"""
    # Unicamente si es admin puede ejecutar este comando
    elif cmd == "fecha_hoy":
        if user == "admin":
            mensaje = f"La fecha actual es: {date.today()}"
            print(mensaje)
        else:
            mensaje = (
                "[Acceso Denegado] Este comando requiere privilegios de administrador."
            )
            print(mensaje)
    # En un solo if se validan ambas restricciones, similar al caso del login, usando parentesis y mediante los operadores (and, or)
    elif cmd == "validar_pass":
        potential_pass = input("Ingrese nueva contraseña: ")
        if len(potential_pass) >= 8 and potential_pass != user:
            mensaje = "La nueva contraseña es Valida."
            print(mensaje)
        else:
            mensaje = "La nueva contraseña NO es Valida. \n(Debe contener almenos 8 caracteres y no puede ser ser igual a su nombre de usuario)"
            print(mensaje)
    # se castean a enteros los 2 numeros para poder operarlos aritmeticamente, y evitar error de unsupported operand
    # se usa int en lugar de float para facilitar el ejercicio, en el caso de la division python siempre retorna un float
    # se incluyen excepciones de division por cero y operador invalido
    elif cmd == "calculadora":
        numero1 = int(input("Ingrese el primer numero: "))
        operador = input("Ingresa el operador (+, -, *, /): ")
        numero2 = int(input("Ingresa el segundo número: "))
        if operador == "+":
            mensaje = f"{numero1} + {numero2} = {numero1 + numero2}"
        elif operador == "-":
            mensaje = f"{numero1} - {numero2} = {numero1 - numero2}"
        elif operador == "*":
            mensaje = f"{numero1} * {numero2} = {numero1 * numero2}"
        elif operador == "/":
            if numero2 == 0:
                mensaje = "No es posible dividir un numero entre cero (0)"
            else:
                mensaje = f"{numero1} / {numero2} = {numero1 / numero2}"
        else:
            mensaje = "Operador ingresado No es valido."
        print(mensaje)
    elif cmd == "historial all":
        print(historial_chat)
    elif cmd == "historial clear":
        historial_chat.clear()
        print("[PseudoAgente] Historial eliminado")
    elif cmd == "historial":
        word_search = input("Ingrese la palabra clave a buscar: ")
        coincidencias = []
        for item in historial_chat:
            # Mediante el uso del operador in hago la comparacion de la palabra ingresada con cada descripcion almacenada en el historial
            # como el historial es una lista de diccionarios accedo a la descripcion y uso la funcion lower para ignorar mayusculas
            # guardo las coincidencias encontradas en una nueva lista, que luego uso para el mensaje a imprimir
            descripcion = str(item["descripcion"])
            if word_search.lower() in descripcion.lower():
                coincidencias.append(item)
        if len(coincidencias) > 0:
            mensaje = f"Se encontro {len(coincidencias)} coincidencia(s)\n{coincidencias}"
        else:
            mensaje = "[PseudoAgente] No encontré registros que coincidan con esa palabra."
        print(mensaje)
    else:
        mensaje = "Comando desconocido, intente de nuevo."
        print(mensaje)

    # Estoy excluyendo todos los comandos de historial del almacenamiento, para evitar que se vuelve muy redundante en las busquedas
    if "historial" not in cmd:
        d_log = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cmd": cmd,
            "rol": user,
            "descripcion": mensaje,
        }
        historial_chat.append(d_log)
