from agente import PseudoAgente, AgenteAdmin
import sys

def login(nombre_usuario: str, clave: str) -> dict:
    """
    Valida las credenciales del usuario y retorna un diccionario con el rol y estado de acceso.
    """
    admin_user = "admin"
    admin_pass = "1234"
    guest_user = "invitado"
    guest_pass = "0000"
    if nombre_usuario == admin_user and clave == admin_pass:
        return {"rol": "admin", "access": "True", "descripcion": "Bienvenido, administrador."}
    elif nombre_usuario == guest_user and clave == guest_pass:
        return {"rol": "invitado", "access": "True", "descripcion": "Bienvenido, invitado."}
    else:
        return {"rol": "", "access": "False", "descripcion": "Usuario o contraseña incorrectos."}

intentos = 0
max_intentos = 3
logueado = False
rol = ""
usuario = ""

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

if not logueado:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
    sys.exit()
else:
    if rol == "admin":
        agente = AgenteAdmin(usuario)
    else:
        agente = PseudoAgente(usuario)
    print(f"Bienvenido al pseudoagente de consola, {agente.nombre} ({rol}). Escribe 'salir' para terminar la sesión.")
    sistema_activo = True
    while sistema_activo:
        if agente.tokens <= 0:
            print("[Agente] Sin energía. Apagando sistema.")
            sistema_activo = False
            continue
        cmd = input("Agente>: ").lower()
        if cmd.startswith("historial"):
            mensaje = agente.gestionar_historial(cmd)
            print(mensaje)
        elif cmd == "salir":
            print("---Agente Apagado. Vuelve Pronto.-------")
            sistema_activo = False
            mensaje = "Se ha solicitado terminar la sesión."
        elif cmd == "ping":
            agente.tokens -= 20
            mensaje = f"Se ha enviado un ping y de respuesta se devolvió un pong.\n[Tokens restantes: {agente.tokens}]"
            print("pong")
            print(f"[Tokens restantes: {agente.tokens}]")
        elif cmd == "contar":
            mensaje = agente.contar_letras()
            print(mensaje)
        elif cmd == "fecha_hoy":
            try:
                mensaje = agente.fecha_hoy(rol)
                print(mensaje)
            except PermissionError as ex:
                mensaje = f"[PseudoAgente] {ex}"
                print(mensaje)
        elif cmd == "validar_pass":
            mensaje = agente.validar_pass(usuario)
            print(mensaje)
        elif cmd == "calculadora":
            try:
                mensaje = agente.calculadora()
                print(mensaje)
            except ValueError as ex:
                mensaje = f"[PseudoAgente] {ex}"
                print(mensaje)
        elif cmd == "dado":
            mensaje = agente.lanzar_dado()
            print(mensaje)
        else:
            mensaje = "Comando no existe. Intente de nuevo"
            print(mensaje)
        agente.registrar_log(cmd, rol, mensaje)
