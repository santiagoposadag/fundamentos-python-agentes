import datetime

print("----- Pseudoagente estilo consola -------")
print("----- Identificate -------")

user_invitado = "invitado"
invitado_pass = "1234"
user_admin = "admin"
admin_pass = "admin"
mensaje = ""
historial_chat = []

intentos = 0
rol = None

## Para el proceso de login se utiliza la variable 'intentos' y en caso de que el usuario no ingrese correctamente el usuario
## y la contraseña, se aumentará en 1 el valor de la variable, el bucle while terminará en el instante que la variable sea igual a 3
## terminará la ejecución del programa y dará el mensaje 'Demasiados intentos. Programa terminado.'
while intentos < 3:
    user_ingresado = input("Ingrese el usuario: ").lower()
    pass_ingresado = input("Ingrese el password: ")

    if user_ingresado == user_invitado and pass_ingresado == invitado_pass:
        rol = "Invitado"
        break
    elif user_ingresado == user_admin and pass_ingresado == admin_pass:
        rol = "Administrador"
        break
    else:
        if intentos == 3:
            print("[Alerta] Usuario bloqueado. Cerrando sistema.")
            break
        else:
            intentos += 1
            print(f"Usuario o contraseña incorrecto. tienes {3 - intentos} intentos")

if rol is None:
    print("Demasiados intentos. Programa terminado.")
    exit()

print(f"Login exitoso. Rol: {rol}")

print("----- Iniciando el pseudoagente estilo consola -------")

# Banderas/Banderines - Booleanos

sistema_activo = True
while sistema_activo:
    cmd = input("Agente>: ").strip().lower()
    cmd_split = cmd.split()
    # funcionalidad para salir del programa
    if cmd == "salir":
        print("------Agente apagado. Vuelve pronto.------")
        mensaje = "Se ha solicitado terminar la sesión."
        sistema_activo = False
    # Funcionalidad para que el sistema devuelva 'pong' si el usuario ingresa 'ping'
    elif cmd == "ping":
        print("pong.")
        mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
    # Funcionalidad para contar las palabras ingresadas
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
        print(
            f"Palabra ingresada: {palabra}\n Total de vocales: {tot_vocales}\n Total de consonantes: {tot_cons}\n Total de letras: {tot_letras}")
        mensaje = f"Se solicitó el conteo de la palabra {palabra}, dando como resultados: \n Vocales: {tot_vocales}\n Consonantes: {tot_cons}\n Total: {tot_letras}"
    # Funcionalidad para averiguar la fecha actual, si el usuario tiene rol invitado, el sistema rrojará un mensaje de error
    elif rol == "Invitado" and cmd == "fecha_hoy":
        mensaje = "[Acceso Denegado] Este comando requiere privilegios de administrador."
        print(mensaje)
    elif rol == "Administrador" and cmd == "fecha_hoy":
        ahora = datetime.datetime.now()
        mensaje = f"[PseudoAgente] La fecha y hora actual es: {ahora.strftime('%Y-%m-%d %H:%M:%S')}"
        print(mensaje)
    # Funcionalidad para validar el cambio de contraseña, esta se hace a través de un bucle while y hasta que no cumpla con las condiciones dadas
    # el sistema no permitirá la validación de cambio de contraseña
    elif cmd == "validar_pass":
        pass_correcta = False
        nueva_pass = ""
        while not pass_correcta:
            nueva_pass = input("Ingrese una propuesta de contraseña nueva: ")
            if len(nueva_pass) > 8 and nueva_pass != user_invitado and nueva_pass != user_admin:
                print("Propuesta de nueva contraseña aceptada")
                pass_correcta = True
            else:
                print("La contraseña debe tener mas de 8 caracteres y no debe ser igual al nombre de usuario")
        mensaje = f"Se ha solicitado validar la contraseña, contraseña ingresada {nueva_pass}"
    # Funcionalidad de calculadora, pide al usuario dos números y una operación, dada la operación que ingresa, el sistema hace el cálculo
    # de acuerdo con el operador seleccionado.
    # Los valores de los números se guardan tipo float para que en caso de división, de un cálculo más preciso. Si es una división por cero
    # el sistema imprime un mensaje de error
    elif cmd == "calculadora":
        primer_numero = float(input("Ingrese el primer numero: "))
        segundo_numero = float(input("Ingrese el segundo numero: "))
        operador = input("Ingrese el operador suma, resta, división o multiplicación: ")
        if operador == "suma":
            print(primer_numero + segundo_numero)
        elif operador == "resta":
            print(primer_numero - segundo_numero)
        elif operador == "multiplicacion":
            print(primer_numero * segundo_numero)
        elif operador == "division":
            if segundo_numero == 0:
                print("No se permite la división entre cero")
            else:
                print(f"{primer_numero / segundo_numero:.2f}")
        else:
            print("Operación no valida")
        mensaje = f"Se ha solicitado realizar la operación {operador} entre el número {primer_numero} y {segundo_numero}"
    # Funcionalidad para mirar el historial de las conversaciones con el agente, el agente analiza cual es el comando ingresado
    # si es historial all, listará todo el historial almacenado, si es historial clear, se limpiará todo el historial
    # si identifica que solo solicita el historial, se solicitará al usuario ingresar una palabra clave, el sistema buscará
    # esa palabra dentro de las descripciones almacenadas en el historial, si encuentra coincidencias, se listarán con su iteración, rol y descripción,
    # si no encuentra coincidencias, se imprimirá un mensaje de error
    elif cmd_split[0] == "historial":
        # Esta funcionalidad imprime todo el historial de las peticiones hechas al agente
        if len(cmd_split) == 2 and cmd_split[1] == "all":
            for i in historial_chat:
                print(i)
            mensaje = "Se ha solicitado mostrar el historial completo del usuario"
        # Esta funcionalidad borra todo el historial almacenado de las peticiones al agente
        elif len(cmd_split) == 2 and cmd_split[1] == "clear":
            historial_chat.clear()
            mensaje = "Se ha solicitado limpiar el historial completo del usuario"
            print(mensaje)
        else:
            contador = 0
            coincidencias = []
            datos_coincidencias = {}
            iteracion = 0
            palabra_clave = input("Ingresa la palabra clave a buscar: ").lower()
            for i in historial_chat:
                # Uso el operador "in" para verificar si una palabra está contenida dentro de otra cadena de texto.
                # Para evitar problemas con mayúsculas/minúsculas uso .lower() en ambos valores.
                if palabra_clave in i["descripción"].lower():
                    contador += 1
                    datos_coincidencias = {
                        "rol": i["rol"],
                        "descripción": i["descripción"],
                        "iteracion": iteracion + 1
                    }
                    coincidencias.append(datos_coincidencias)
                iteracion += 1
            if contador == 0:
                print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")
            else:
                print(f"La palabra clave es: {palabra_clave} y hay {contador} coincidencias.\n")
                for i in coincidencias:
                    print(f"Iteración: {i['iteracion']}")
                    print(f"Autor: {i['rol']}")
                    print(f"Mensaje: {i['descripción']}\n")
    else:
        print("------Comando desconocido. Intente de nuevo.-------")
        mensaje = "Se ha enviado un comando desconocido, el sistema no pudo reconocerlo y se solicitó intentar de nuevo."
    # De acuerdo con la petición hecha, en la variable d_log se guardan los datos de la operación
    # y posteriormente almacenarlos en el historial
    d_log = {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
             "cmd": cmd,
             "rol": rol,
             "descripción": mensaje}
    historial_chat.append(d_log)
