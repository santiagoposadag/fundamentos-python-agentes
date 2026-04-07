# Taller Semana 4 - Nace la Entidad (POO y Modularización)
# La lógica del agente ahora vive en agente.py. Aquí solo están el login y el menú.

from agente import PseudoAgente, AgenteAdmin


def login():
    admin_user = "admin"
    admin_pass = "admin123"
    invitado_user = "invitado"
    invitado_pass = "invitado"

    intentos = 0
    max_intentos = 3

    # Máximo 3 intentos antes de bloquear
    while intentos < max_intentos:
        usuario = input("Usuario: ").strip()
        contrasena = input("Contraseña: ").strip()

        if usuario == admin_user and contrasena == admin_pass:
            print("[OK] Acceso concedido como administrador.")
            return usuario, "admin"
        elif usuario == invitado_user and contrasena == invitado_pass:
            print("[OK] Acceso concedido como invitado.")
            return usuario, "invitado"
        else:
            intentos += 1
            print(f"[Error] Credenciales incorrectas. Intento {intentos} de {max_intentos}.")

    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
    return None, None


def main():
    usuario, role = login()
    if usuario is None:
        return

    # Si es admin instanciamos AgenteAdmin (no consume tokens en historial),
    # si es invitado instanciamos PseudoAgente normal.
    if role == "admin":
        mi_agente = AgenteAdmin("Athena")
    else:
        mi_agente = PseudoAgente("Athena")

    def print_menu():
        print(f"\n===== MENU ===== [{mi_agente.nombre}] Tokens: {mi_agente.tokens}")
        print(" - ping           : Responde 'pong!'")
        print(" - contar         : Cuenta vocales y consonantes")
        print(" - fecha_hoy      : Muestra fecha (solo admin)")
        print(" - validar_pass   : Valida una nueva contraseña propuesta")
        print(" - calculadora    : Realiza operaciones aritméticas")
        print(" - dado           : Lanza un dado de 6 caras")
        print(" - historial      : Buscar en historial (usa 'historial all' o 'historial clear')")
        print(" - salir          : Cierra el agente")
        print("=================")

    print_menu()

    pseudo_activo = True

    # El while se apaga si el usuario escribe 'salir' (pseudo_activo = False)
    # o si los tokens llegan a 0 (sin usar break)
    while pseudo_activo and mi_agente.tokens > 0:
        cmd = input("-> ").strip().lower()
        mensaje = ""

        try:
            if cmd == "ping":
                mensaje = mi_agente.comando_ping()

            elif cmd == "contar":
                mensaje = mi_agente.contar_letras()

            elif cmd == "fecha_hoy":
                mensaje = mi_agente.comando_fecha_hoy(role)  # lanza PermissionError si es invitado

            elif cmd == "validar_pass":
                mensaje = mi_agente.validar_password(usuario)

            elif cmd == "calculadora":
                mensaje = mi_agente.calculadora()

            elif cmd == "dado":
                mensaje = mi_agente.lanzar_dado()
                print(mensaje)

            elif cmd.startswith("historial"):
                partes = cmd.split()
                subcmd = partes[1] if len(partes) > 1 else None

                if subcmd == "all":
                    resultado = mi_agente.gestionar_historial("all")
                    print(resultado)
                    mensaje = "[PseudoAgente] Mostrado historial completo."

                elif subcmd == "clear":
                    resultado = mi_agente.gestionar_historial("clear")
                    print(resultado)
                    mensaje = "[PseudoAgente] Historial eliminado."

                else:
                    keyword = input("Ingresa la palabra clave a buscar: ").strip()
                    resultado = mi_agente.gestionar_historial("search", keyword)
                    print(resultado)
                    mensaje = resultado

            elif cmd == "salir":
                mensaje = "Se ha solicitado terminar la sesión."
                mi_agente.registrar_log(cmd, role, mensaje)
                print("Apagando agente. ¡Hasta luego!")
                pseudo_activo = False
                continue  # salta el registro duplicado al final del bucle

            else:
                print("Comando no reconocido. Intenta una de las opciones del menú.")
                mensaje = "Comando no reconocido."

        except PermissionError as e:
            print(f"[Acceso Denegado] {e}")
            mensaje = f"[Acceso Denegado] {e}"

        except ValueError as e:
            print(f"[Error] Entrada inválida: {e}")
            mensaje = f"[Error] Entrada inválida: {e}"

        mi_agente.registrar_log(cmd, role, mensaje)

        if pseudo_activo:
            print_menu()

    # Mensaje si el bucle terminó por tokens agotados
    if mi_agente.tokens <= 0:
        print(f"[{mi_agente.nombre}] Tokens agotados. Apagando...")


if __name__ == "__main__":
    main()
