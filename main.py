# main.py - Sistema de login y menú principal del pseudoagente

from agente import PseudoAgente, AgenteAdmin

roles = ["invitado", "admin"]
contrasenias = ["123thonpy", "py456thon"]

login_usuario = True
intentos = 0
max_intentos = 3

while login_usuario:
    usuario = input("Ingrese el rol de usuario (invitado/admin): ").lower()
    if usuario in roles:
        login_contrasenia = True
        while login_contrasenia:
            indice_rol = roles.index(usuario)
            contrasenia = input("Ingrese la contraseña: ")
            if contrasenia == contrasenias[indice_rol]:
                print(f"Bienvenido, {usuario}. Acceso concedido.\n")
                print("----- Iniciando el pseudoagente estilo consola -----")

                if usuario == "admin":
                    agente = AgenteAdmin(nombre=usuario)
                else:
                    agente = PseudoAgente(nombre=usuario)

                sistema_activo = True
                mensaje = ""

                while sistema_activo and agente.tokens > 0:
                    print(f"[Tokens restantes: {agente.tokens}]")
                    cmd = input("Agente>: ").strip().lower().split()
                    try:
                        if cmd[0] == "salir":
                            print("-----Agente apagado. Vuelve pronto. -----")
                            sistema_activo = False
                            login_contrasenia = False
                            login_usuario = False
                            mensaje = "Se ha solicitado terminar la sesión."
                        elif cmd[0] == "ping":
                            mensaje = agente.ping()
                            print(mensaje)
                        elif cmd[0] == "contar":
                            palabra = input("Ingrese una palabra: ").lower()
                            mensaje = agente.contar_letras(palabra)
                            print(mensaje)
                        elif cmd[0] == "fecha_hoy":
                            try:
                                mensaje = agente.fecha_hoy(usuario)
                                print(mensaje)
                            except PermissionError as e:
                                print(f"[Alerta] {e}")
                                mensaje = str(e)
                        elif cmd[0] == "validar_pass":
                            nueva_contrasenia = input("Ingrese una nueva contraseña: ")
                            mensaje = agente.validar_password(usuario, nueva_contrasenia)
                            print(mensaje)
                        elif cmd[0] == "calculadora":
                            try:
                                num1 = float(input("Ingresa el primer número: "))
                                operador = input("Ingresa el operador (+, -, *, /): ")
                                num2 = float(input("Ingresa el segundo número: "))
                                mensaje = agente.calculadora(num1, operador, num2)
                                print(mensaje)
                            except ValueError as ve:
                                print(f"[Error] {ve}")
                                mensaje = str(ve)
                        elif cmd[0] == "dado":
                            mensaje = agente.lanzar_dado()
                            print(mensaje)
                        elif cmd[0] == "historial":
                            if len(cmd) > 1 and cmd[1] in ("all", "clear"):
                                resultado = agente.gestionar_historial(cmd[1])
                                print(resultado)
                                mensaje = resultado
                            else:
                                clave = input("Ingrese la palabra clave a buscar: ").lower()
                                resultado = agente.gestionar_historial(clave)
                                print(resultado)
                                mensaje = resultado
                        else:
                            mensaje = "-----Comando desconocido. Intente de nuevo. -----"
                            print(mensaje)
                    except IndexError:
                        print("[Error] Debe ingresar un comando.")
                        mensaje = "Comando vacío."
                    agente.registrar_log(cmd, mensaje, usuario)

                if agente.tokens <= 0:
                    print("[Alerta] El agente se ha quedado sin batería. Sesión terminada.")
                    login_contrasenia = False
            else:
                print("Contraseña incorrecta. Intente de nuevo.")
                intentos += 1
            if intentos >= max_intentos:
                login_contrasenia = False
        login_usuario = False
    else:
        print("Usuario no reconocido. Intente de nuevo.")
        intentos += 1
    if intentos >= max_intentos:
        print("[Alerta] Usuario bloqueado. Cerrando sistema.")
        login_usuario = False
