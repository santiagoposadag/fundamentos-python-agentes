# =========================
# Fase 1: Login con 3 intentos
# =========================
# Definimos usuarios y contraseñas
admin_user = "admin"
admin_pass = "1234"
guest_user = "invitado"
guest_pass = "0000"

# Contador de intentos para el login
intentos = 0
max_intentos = 3
logueado = False
rol = ""

# Ciclo de login: pide usuario y contraseña, máximo 3 intentos
while intentos < max_intentos:
    usuario = input("Usuario: ").lower()
    password = input("Contraseña: ").lower()
    # Si usuario y contraseña son correctos, se guarda el rol
    if usuario == admin_user and password == admin_pass:
        print("Bienvenido, administrador.")
        logueado = True
        rol = "admin"
        break
    elif usuario == guest_user and password == guest_pass:
        print("Bienvenido, invitado.")
        logueado = True
        rol = "invitado"
        break
    else:
        print("Usuario o contraseña incorrectos.")
        intentos += 1

# Si no se logra el login, se bloquea el sistema
if not logueado:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
else:
    # =========================
    # Fase 2 y 3: Menú de comandos
    # =========================
    print("Bienvenido al pseudoagente de consola. Escribe 'salir' para terminar la sesión." )
    # Banderas/Banderines - Booleanos - True/False
    sistema_activo = True
    # Ciclo principal del menú
    while sistema_activo:
        cmd = input("Agente>: ").lower()

        # Comando para salir del sistema
        if cmd == "salir":
            print("---Agente Apagado. Vuelve Pronto.-------")
            sistema_activo = False
        # Comando ping
        elif cmd == "ping":
            print("pong")
        # Comando contar: cuenta letras, vocales y consonantes
        elif cmd == "contar":
            palabra = input ("Ingresa una palabra: ").lower()
            tot_letras = len(palabra)
            tot_vocales = 0
            tot_cons = 0
            for p in palabra:
                if p in "aeiou":
                    tot_vocales +=1
                else:
                    tot_cons +=1
            print(f"Palabra ingresada: {palabra}")
            print(f"Total de letras: {tot_letras}")
            print(f"Total de vocales: {tot_vocales}")
            print(f"Total de consonantes: {tot_cons}")
        # Comando fecha_hoy: solo admin puede ver la fecha
        elif cmd == "fecha_hoy":
            if rol == "admin":
                import datetime
                print("Fecha actual:", datetime.datetime.now().strftime("%Y-%m-%d"))
            else:
                print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
        # Comando validar_pass: valida nueva contraseña
        elif cmd == "validar_pass":
            nueva = input("Propuesta de nueva contraseña: ")
            # Primero validamos que no sea igual al usuario
            if nueva == usuario:
                print("La contraseña no puede ser igual al nombre de usuario.")
            elif len(nueva) < 8:
                print("La contraseña debe tener al menos 8 caracteres.")
            else:
                print("Contraseña válida.")
        # Comando calculadora: operaciones matemáticas
        elif cmd == "calculadora":
            # Solicita los números y el operador al usuario
            n1 = input("Ingresa el primer número: ")
            op = input("Ingresa el operador (+, -, *, /): ")
            n2 = input("Ingresa el segundo número: ")
            try:
                # Convierte los inputs a float para poder operar
                n1 = float(n1)
                n2 = float(n2)
                # Evalúa el operador ingresado
                if op == "+":
                    print("Resultado:", n1 + n2)
                elif op == "-":
                    print("Resultado:", n1 - n2)
                elif op == "*":
                    print("Resultado:", n1 * n2)
                elif op == "/":
                    # Verifica si el segundo número es cero para evitar error de división
                    if n2 == 0:
                        print("No se puede dividir por cero.")
                    else:
                        print("Resultado:", n1 / n2)
                else:
                    print("Operador no válido.")
            # Si los inputs no son números válidos, muestra un mensaje de error
            except ValueError:
                print("Debes ingresar números válidos.")
        # Comando desconocido
        else:
            print("---Comando desconocido. Intente de nuevo. ------")