from agente import PseudoAgente, AgenteAdmin

print("----- Iniciando el pseudoagente estilo consola -------")

user_admin = "admin"
pass_admin = "12345"

user_invitado = "invitado"
pass_invitado = "abcde"

intentos_maximos = 3
intentos_actuales = 0
autenticado = False
rol_usuario = ""


while intentos_actuales < intentos_maximos and not autenticado:
    username = input("Ingrese su nombre de usuario: ").lower()
    password = input("Ingrese su contraseña: ").lower()

    if (username == user_admin and password == pass_admin):
        autenticado = True
        rol_usuario = "admin"
        print("Bienvenido, admin. Tienes acceso completo al sistema.")
    elif (username == user_invitado and password == pass_invitado):
        autenticado = True
        rol_usuario = "invitado"
        print("Bienvenido, invitado. Tienes acceso limitado al sistema.")
#Primero se crea una variable que almacena el número máximo de intentos permitidos,
# luego se inicializa un contador de intentos actuales y una bandera de autenticación. 
# El bucle que se ejecuta mientras el número de intentos actuales sea menor que el máximo permitido y el usuario no esté autenticado. 

    else:
        intentos_actuales += 1
        print(f"Credenciales incorrectas. Intentos restantes: {intentos_maximos - intentos_actuales}")

if not autenticado:
    print("Has excedido el número máximo de intentos. El sistema se bloqueará.")
else:
    if rol_usuario == "admin":
        agente = AgenteAdmin("Athena")
    else:
        agente = PseudoAgente("Athena")

    sistema_activo = True
    while sistema_activo and agente.tokens > 0:
        cmd = input("Agente>: ").lower()

        if cmd == "salir":
            print("------Agente apagado. Vuelve pronto.------")
            sistema_activo = False
        elif cmd == "ping":
            print("pong.")
            agente.tokens -= 2
            # Guardamos el recuerdo del comando ping ejecutado
            agente.registrar_log(rol_usuario, "El usuario ejecuto el comando ping")
        elif cmd =="contar":
            palabra_ingresada = input("Ingrese una palabra: ").lower()
            print(agente.contar_letras(palabra_ingresada))
            # Guardamos el recuerdo con la palabra usada
            agente.registrar_log(rol_usuario, f"Contó letras en la palabra: {palabra_ingresada}")
        elif cmd == "fecha_hoy":
            try:
                fecha_actual = agente.obtener_fecha_actual(rol_usuario)
                print(f"Fecha actual: {fecha_actual}")
                agente.registrar_log(rol_usuario, f"Consultó la fecha actual: {fecha_actual}")
            except PermissionError:
                print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
                agente.registrar_log(rol_usuario, "Intento fallido de ver fecha (Acceso denegado)")

        elif cmd == "validar_pass":
            nueva_pass_ingresada = input("Ingrese la nueva contraseña: ")
            if agente.validar_password(nueva_pass_ingresada, rol_usuario):
                print("Contraseña válida. Se ha actualizado correctamente.")
                agente.registrar_log(rol_usuario, "Validó una nueva contraseña exitosamente")
            else:
                print("La contraseña no cumple con las políticas de seguridad.")
                agente.registrar_log(rol_usuario, "Intento de cambio de pass inválido")

        elif cmd == "calculadora":
            try:
                num1 = float(input("Ingrese el primer número: "))
                num2 = float(input("Ingrese el segundo número: "))
                operacion = input("Ingrese la operación (+, -, *, /): ")

                resultado = agente.calculadora(num1, num2, operacion)
                print(f"Resultado: {resultado}")
                agente.registrar_log(rol_usuario, f"Realizó una operación: {num1} {operacion} {num2} = {resultado}")
            except ValueError as error:
                if str(error) == "No se puede dividir por cero." or str(error) == "Operación no válida.":
                    print(f"Error: {error}")
                else:
                    print("Error: Debe ingresar valores numéricos válidos.")

        elif cmd.startswith("historial"):
            partes = cmd.split() 
            if len(partes) > 1 and partes[1] == "all":
                print(agente.gestionar_historial("all"))

            elif len(partes) > 1 and partes[1] == "clear":
                print(agente.gestionar_historial("clear"))
            else:
                busqueda = input("Ingresa la palabra clave a buscar: ").lower()
                print(agente.gestionar_historial(busqueda))

        elif cmd == "dado":
            print(agente.lanzar_dado())
            agente.registrar_log(rol_usuario, "Lanzó un dado")

        else:
            print("------Comando desconocido. Intente de nuevo.-------")

    if agente.tokens <= 0:
        print(f"[{agente.nombre}] Batería agotada. El agente se ha apagado.")
