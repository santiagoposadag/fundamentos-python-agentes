import datetime

print("----- Pseudoagente estilo consola -------")
print("----- Identificate -------")

user_invitado = "invitado"
invitado_pass = "1234"
user_admin = "admin"
admin_pass = "admin"

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
    cmd = input("Agente>: ").lower()
#funcionalidad para salir del programa
    if cmd == "salir":
        print("------Agente apagado. Vuelve pronto.------")
        sistema_activo = False
#Funcionalidad para que el sistema devuelva 'pong' si el usuario ingresa 'ping'
    elif cmd == "ping":
        print("pong.")
#Funcionalidad para contar las palabras ingresadas
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
#Funcionalidad para averiguar la fecha actual, si el usuario tiene rol invitado, el sistema rrojará un mensaje de error
    elif rol == "Invitado" and cmd == "fecha_hoy":
        print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
    elif rol == "Administrador" and cmd == "fecha_hoy":
        ahora = datetime.datetime.now()
        print(ahora)
#Funcionalidad para validar el cambio de contraseña, esta se hace a través de un bucle while y hasta que no cumpla con las condiciones dadas
#el sistema no permitirá la validación de cambio de contraseña
    elif cmd == "validar_pass":
        pass_correcta = False
        while not pass_correcta:
            nueva_pass = input("Ingrese una propuesta de contraseña nueva: ")
            if len(nueva_pass)>8 and nueva_pass != user_invitado and nueva_pass != user_admin:
                print("Propuesta de nueva contraseña aceptada")
                pass_correcta = True
            else:
                print("La contraseña debe tener mas de 8 caracteres y no debe ser igual al nombre de usuario")
#Funcionalidad de calculadora, pide al usuario dos números y una operación, dada la operación que ingresa, el sistema hace el cálculo
#de acuerdo con el operador seleccionado.
#Los valores de los números se guardan tipo float para que en caso de división, de un cálculo más preciso. Si es una división por cero
#el sistema imprime un mensaje de error
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

    else:
        print("------Comando desconocido. Intente de nuevo.-------")