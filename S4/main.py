# Solución Taller Semana 4: Nace la Entidad (POO y Modularización)
## Andrés Felipe Chalarca Rueda.

# --- IMPORTAMOS NUESTRAS CLASES DEL ARCHIVO agente.py --- #
from agente import PseudoAgente, AgenteAdmin
import sys

# --- FUNCIÓN DE ENTRADA (LOGIN) --- #
def iniciar_sesion():
    """
    Esta función es la puerta de entrada al sistema.
    Pide el nombre del agente y lo crea, o si el nombre es "admin", crea un agente administrador.
    """
    print("===¡BIENVENIDO AL SISTEMA DE AGENTES!===")
    for intento in range(3):  # Permite hasta 3 intentos para iniciar sesión.
        u = input("Ingrese el nombre de usuario: ").strip().lower()  # Pedimos el nombre de usuario y lo normalizamos.
        p = input("Ingrese la contraseña: ").strip()  # Pedimos la contraseña (en este caso, no se valida).

        # Según el usuario, decimos qué tipo de "Entidad" crear.
        if u == "admin" and p == "1234":  # Si el usuario es "admin", creamos un AgenteAdmin.
            print("¡Bienvenido, Administrador!")
            return AgenteAdmin("Zeus"), u  # Devolvemos el agente administrador y su nombre.
        elif u == "invitado" and p == "0000":  # Si el usuario es "invitado", creamos un Pseudoagente con nombre "Athena".
            print("¡Bienvenido, Invitado!")
            return PseudoAgente("Athena"), u  # Devolvemos el agente invitado y su nombre.
        
        print(f"Intento {intento + 1}/3: Usuario o contraseña incorrectos. Intente de nuevo.\n")  # Mensaje de error.
    return None, None  # Si se agotan los intentos, devolvemos None.

# --- EJECUCION --- #
agente, nombre_usuario = iniciar_sesion()  # Iniciamos sesión y obtenemos el agente creado.

if not agente:  # Si no se pudo iniciar sesión, salimos del programa.
    print("Sistema bloqueado por seguridad. Saliendo del programa.")
    sys.exit()

print(f"\n[Sistema]¡{agente.nombre} ha ingresado al sistema con éxito! ¡Comencemos a interactuar!\n")  # Mensaje de bienvenida.

# --- BUCLE PRINCIPAL: Mientras el agente tenga energía (tokens > 0) --- #
while agente.tokens > 0:
    try:
        # Mostramos los tokens actuales en el prompt para que el usuario sepa cuánta energía le queda al agente.
        entrada = input(f"\n{agente.nombre} (Tokens: {agente.tokens})> ").strip().lower()  # Pedimos un comando al usuario.
        if not entrada:  # Si el usuario no ingresa nada, lo ignoramos.
            continue

        partes = entrada.split()  # Separamos el comando en partes para analizarlo.
        cmd = partes[0]  # El primer elemento es el comando principal.
        respuesta_agente = ""  # Variable para almacenar la respuesta del agente.

        if cmd == "salir":  # Comando para salir del programa.
            print("¡Hasta luego! Gracias por usar el sistema de agentes.")
            break

        elif cmd == "ping":  # Comando para ejecutar la habilidad "ping".
            respuesta_agente = agente.ejecutar_ping()  # Ejecutamos la habilidad y obtenemos la respuesta.
            print(respuesta_agente)  # Mostramos la respuesta del agente.

        elif cmd == "fecha":  # Comando para obtener la fecha y hora actual.
            # Si falla por permisos, el 'except' de abajo lo atrapa y mostrará un mensaje de error.
            respuesta_agente = agente.obtener_fecha_sistema(nombre_usuario)  # Ejecutamos la habilidad y obtenemos la respuesta.
            print(respuesta_agente)  # Mostramos la respuesta del agente.

        elif cmd == "dado":  # Comando para lanzar un dado.
            respuesta_agente = agente.lanzar_dado()  # Ejecutamos la habilidad y obtenemos la respuesta.
            print(respuesta_agente)  # Mostramos la respuesta del agente.

        elif cmd == "historial":  # Comando para gestionar el historial de chat.
            # Si se escribe 'historial all', partes[1] será 'all', si se escribe 'historial clear', partes[1] será 'clear', etc.
            sub = partes[1] if len(partes) > 1 else "search"  # Si no se especifica subcomando, por defecto es "search".
            busqueda = input("Palabra clave: ").strip() if sub == "search" else None  # Si es búsqueda, pedimos la palabra clave.
            respuesta_agente = agente.gestionar_historial(sub, busqueda)  # Ejecutamos la habilidad de gestionar historial y obtenemos la respuesta.
            print(respuesta_agente)  # Mostramos la respuesta del agente.

        elif cmd == "calcular":  # Comando para realizar cálculos matemáticos.
            try:
                # Capturamos los datos para enviárselos al método del agente.
                num1 = float(input("Primer número: ").strip())  # Pedimos el primer número y lo convertimos a float.
                op = input("Operación (+, -, *, /): ").strip()  # Pedimos la operación y la normalizamos.
                num2 = float(input("Segundo número: ").strip())  # Pedimos el segundo número y lo convertimos a float.

                #Llamamos a la habilidad del agente para realizar el cálculo y obtenemos la respuesta.
                respuesta_agente = agente.realizar_calculo(num1, op, num2)
                print(respuesta_agente)  # Mostramos la respuesta del agente.
            except ValueError:  # Si el usuario ingresa algo que no es un número, lo atrapamos aquí.
                respuesta_agente = "[Error]: Entrada inválida para cálculo. Debes ingresar números válidos."  # Respuesta del agente en caso de error de entrada.
                print(respuesta_agente)  # Mostramos la respuesta del agente.

        elif cmd == "validar_pass":  # Comando para validar una contraseña.
            p_nueva = input("Ingrese una nueva contraseña: ").strip()  # Pedimos la nueva contraseña al usuario.
            # Le pasasamos la clave y el nombre de usuario actual.
            respuesta_agente = agente.validar_seguridad_clave(p_nueva, nombre_usuario)  # Ejecutamos la habilidad de validar contraseña y obtenemos la respuesta.
            print(respuesta_agente)  # Mostramos la respuesta del agente.

        elif cmd == "contar":  # Comando para contar letras en una frase.
            frase = input("Ingrese una frase: ").strip()  # Pedimos la frase al usuario.
            respuesta_agente = agente.contador_letras(frase)  # Ejecutamos la habilidad de contar letras y obtenemos la respuesta.
            print(respuesta_agente)  # Mostramos la respuesta del agente.

        else:  # Si el comando no es reconocido, mostramos un mensaje de error.
            respuesta_agente = f"Comando desconocido: '{cmd}'. Por favor, intente con 'ping', 'fecha', 'dado', 'historial', 'calcular', 'validar_pass' o 'salir'."  # Mensaje de error para comando desconocido.
            print(respuesta_agente)  # Mostramos el mensaje de error.

        # SIEMPRE registramos lo que pasó en la memoria del agente, sin importar si el comando fue exitoso o no.
        agente.registrar_log(cmd, nombre_usuario, respuesta_agente)  # Registramos el comando, el rol y la respuesta en el historial del agente.

    except PermissionError as e:  # Si ocurre un error de permisos, lo atrapamos aquí.
        # Aquí capturamos el 'raise' que pusimos en el método 'obtener_fecha_sistema' cuando el rol no es 'admin'.
        print(f"Error de permisos: {e}")  # Mostramos el mensaje de error de permisos.
        agente.registrar_log("SEGURIDAD", nombre_usuario, f"Intento fallido: {e}")  # Registramos el error de permisos en el historial del agente.
    except Exception as e:  # Capturamos cualquier otro error inesperado.
        print(f"Ocurrió un error inesperado: {e}")  # Mostramos el mensaje de error inesperado.
        agente.registrar_log("ERROR", nombre_usuario, f"Error inesperado: {e}")  # Registramos el error inesperado en el historial del agente.

# Si el bucle termina porque el agente se quedó sin tokens, mostramos un mensaje final.
if agente.tokens <= 0:
    print(f"\n¡{agente.nombre} se ha quedado sin energía (tokens)! Por favor, reinicie el programa para volver a intentarlo.")