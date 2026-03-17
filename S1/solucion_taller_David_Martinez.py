from datetime import date

# Declaracion de las variables globales a usar
user_invitado = "invitado"
password_invitado = "123"

user_admin = "admin"
password_admin = "4dm1n"

user = ""
password = ""
sistema_activo = False

# Implementacion del login con 3 intentos usando un for y rompiendo el ciclo con break si usuario y password son correctos,
# para que no siga pidiendolos, se usa la misma variable de sistema_activo para bloquear el sistema o iniciar el agente,
# con sus respectivos mensajes de validacion
for i in range(3):
    user = input("Ingrese usuario: ")
    password = input("Ingrese contraseña: ")
    if (user_invitado == user and password_invitado == password) or (user_admin == user and password_admin == password):
        sistema_activo = True
        break
    else:
        print("\nUsuario y/o contraseña equivocado. Intente nuevamente\n")

if not sistema_activo:
    print("[Alerta] Usuario bloqueado. Cerrando sistema...")
else:
    print("\n----- Iniciando el pseudoagente estilo consola -------")

# Implementacion del Agente con 6 opciones disponibles
while sistema_activo:
    cmd = input("\nAgente>: ").lower()

    if cmd == "salir":
        print("\n------Agente apagado. Vuelve pronto------")
        sistema_activo = False
    elif cmd == "ping":
        print("pong.")
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
    # Unicamente si es admin puede ejecutar este comando
    elif cmd == "fecha_hoy":
        if user == "admin":
            print(date.today())
        else:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
    # En un solo if se validan ambas restricciones, similar al caso del login, usando parentesis y mediante los operadores (and, or)
    elif cmd == "validar_pass":
        potential_pass = input("Ingrese nueva contraseña: ")
        if len(potential_pass) >= 8 and potential_pass != user:
            print("La nueva contraseña es Valida.")
        else:
            print("La nueva contraseña NO es Valida. \n(Debe contener almenos 8 caracteres y no puede ser ser igual a su nombre de usuario)")
    # se castean a enteros los 2 numeros para poder operarlos aritmeticamente, y evitar error de unsupported operand
    # se usa int en lugar de float para facilitar el ejercicio, en el caso de la division python siempre retorna un float
    # se incluyen excepciones de division por cero y operador invalido
    elif cmd == "calculadora":
        numero1 = int(input("Ingrese el primer numero: "))
        operador = input("Ingresa el operador (+, -, *, /): ")
        numero2 = int(input("Ingresa el segundo número: "))
        if operador == "+":
            print(f"{numero1} + {numero2} = {numero1 + numero2}")
        elif operador == "-":
            print(f"{numero1} - {numero2} = {numero1 - numero2}")
        elif operador == "*":
            print(f"{numero1} * {numero2} = {numero1 * numero2}")
        elif operador == "/":
            if(numero2 == 0):
                print("No es posible dividir un numero entre cero (0)")
            else:
                print(f"{numero1} / {numero2} = {numero1 / numero2}")
        else: 
            print("Operador ingresado No es valido.")
    else:
        print("Comando desconocido, intente de nuevo.")
