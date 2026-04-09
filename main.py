import datetime
from typing import Dict, List
from agente import PseudoAgente, AgenteAdmin

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

# Crear instancia del agente
if rol == "Administrador":
    agente = AgenteAdmin("AgenteAdmin")
else:
    agente = PseudoAgente("PseudoAgente")

print("----- Iniciando el pseudoagente estilo consola -------")

# Banderas/Banderines - Booleanos
sistema_activo = True
agente_vivo = True
while sistema_activo and agente_vivo:
    try:
        cmd = input("Agente>: ").strip().lower()
        cmd_split = cmd.split()
        # funcionalidad para salir del programa
        if cmd == "salir":
            print("------Agente apagado. Vuelve pronto.------")
            sistema_activo = False
        # Funcionalidad para que el sistema devuelva 'pong' si el usuario ingresa 'ping'
        elif cmd == "ping":
            resultado = agente.ping(rol)
            print(resultado)
        # Funcionalidad para lanzar un dado virtual
        elif cmd == "lanzar_dado":
            resultado = agente.lanzar_dado(rol)
            print(resultado)
        # Funcionalidad para contar las palabras ingresadas
        elif cmd == "contar":
            palabra = input("Ingrese una palabra: ").lower()
            resultado = agente.contar(palabra, rol)
            print(resultado)
        # Funcionalidad para averiguar la fecha actual, si el usuario tiene rol invitado, el sistema arrojará un mensaje de error
        elif cmd == "fecha_hoy":
            resultado = agente.fecha_hoy_rol(rol)
            print(resultado)
        elif cmd == "validar_pass":
            pass_correcta = False
            nueva_pass = ""
            while not pass_correcta:
                nueva_pass = input("Ingrese una propuesta de contraseña nueva: ")
                resultado_validacion = agente.validar_contrasena(nueva_pass, rol)
                print(resultado_validacion + f"\ncontraseña ingresada: {nueva_pass}")
                if resultado_validacion == "Propuesta de nueva contraseña aceptada":
                    pass_correcta = True
        # Funcionalidad de calculadora, pide al usuario dos números y una operación, dada la operación que ingresa, el sistema hace el cálculo
        # de acuerdo con el operador seleccionado.
        # Los valores de los números se guardan tipo float para que en caso de división, de un cálculo más preciso. Si es una división por cero
        # el sistema imprime un mensaje de error
        elif cmd == "calculadora":
            # Usamos try/except para evitar que el programa se cierre
            # si el usuario comete un error (por ejemplo, escribir letras
            # donde se espera un número).
            # Si ocurre un error, lo capturamos y mostramos un mensaje claro.
            # Así el programa continúa funcionando normalmente.
            try:
                primer_numero = float(input("Ingrese el primer numero: "))
                segundo_numero = float(input("Ingrese el segundo numero: "))
                operador = input("Ingrese el operador suma, resta, división o multiplicación: ").lower()
                resultado_operacion = agente.calcular(primer_numero, segundo_numero, operador, rol)
                print(f"Resultado: {resultado_operacion}")
            except ValueError as e:
                print(f"[ERROR] {e}")
        # Funcionalidad para mirar el historial de las conversaciones con el agente, el agente analiza cual es el comando ingresado
        # si es historial all, listará todo el historial almacenado, si es historial clear, se limpiará todo el historial
        # si identifica que solo solicita el historial, se solicitará al usuario ingresar una palabra clave, el sistema buscará
        # esa palabra dentro de las descripciones almacenadas en el historial, si encuentra coincidencias, se listarán con su iteración, rol y descripción,
        # si no encuentra coincidencias, se imprimirá un mensaje de error
        elif cmd_split[0] == "historial":
            if len(cmd_split) == 2:
                op = cmd_split[1]
                resultado_historial = agente.gestionar_historial(op, rol)
                print(resultado_historial)
            else:
                palabra_clave = input("Ingresa la palabra clave a buscar: ").lower()
                resultado_historial = agente.gestionar_historial(palabra_clave, rol)
                print(resultado_historial)
        else:
            print("------Comando desconocido. Intente de nuevo.-------")

        print(f"Tokens disponibles: {agente.obtener_tokens()}")
    
    except RuntimeError as e:
        print(f"[ALERTA CRÍTICA] {e}")
        agente_vivo = False
    except ValueError as e:
        print(f"[ERROR] {e}")
    except PermissionError as e:
        print(f"[ERROR] {e}")

if not agente_vivo:
    print("------El Agente ha agotado su energía. Sesión terminada.------")
else:
    print("------Agente apagado. Vuelve pronto.------")
