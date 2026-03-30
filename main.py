import datetime
from typing import Dict, List

print("----- Pseudoagente estilo consola -------")
print("----- Identificate -------")

# Aquí le damos un nombre más claro a estructuras de datos.
# En vez de escribir siempre List[Dict[str, str]], usamos MemoriaAgente.
# Esto hace que el código sea más fácil de leer y entender.
# Además, si en el futuro cambia la estructura de la memoria,
# solo debemos modificar el alias y no todo el programa.
type Recuerdo = Dict[str, str]
type MemoriaAgente = List[Recuerdo]

user_invitado = "invitado"
invitado_pass = "1234"
user_admin = "admin"
admin_pass = "admin"
mensaje = ""
historial_chat: MemoriaAgente = []
intentos = 0
rol = None

"""
   Gestiona las operaciones relacionadas con el historial del agente.

   Permite mostrar todo el historial, limpiarlo completamente
   o buscar registros que coincidan con una palabra clave.

   Args:
       list_hist (MemoriaAgente): Lista de recuerdos almacenados.
       op (str): Operación a realizar. Puede ser:
                 - "all": muestra todo el historial.
                 - "clear": elimina todos los registros.
                 - cualquier otra cadena: se interpreta como palabra clave de búsqueda.

   Returns:
       str: Texto formateado con el resultado de la operación solicitada.
   """


def gestionar_historial(list_hist: MemoriaAgente, op: str) -> str:
    resultado = ""
    if op == "all":
        if not list_hist:
            return "[PseudoAgente] El historial está vacío."
        for i, recuerdo in enumerate(historial_chat):
            resultado += (
                f"\nIteración: {i}\n"
                f"Fecha: {recuerdo['timestamp']}\n"
                f"Comando: {recuerdo['cmd']}\n"
                f"Autor: {recuerdo['rol']}\n"
                f"Mensaje: {recuerdo['descripción']}\n"
            )
        return resultado
    elif op == "clear":
        list_hist.clear()
        return "[PseudoAgente] El historial ha sido limpiado."
    else:
        contador = 0
        for i, recuerdo in enumerate(list_hist):
            if op in recuerdo["descripción"].lower():
                contador += 1
                resultado += (
                    f"\nIteración: {i}\n"
                    f"Autor: {recuerdo['rol']}\n"
                    f"Mensaje: {recuerdo['descripción']}\n"
                )
        if contador == 0:
            return "[PseudoAgente] No encontré registros que coincidan con esa palabra."
        return (
                f"La palabra clave es: {op} "
                f"y hay {contador} coincidencias.\n"
                + resultado
        )


"""
   Analiza una palabra y calcula la cantidad de vocales,
   consonantes y letras totales.

   Args:
       pal (str): Palabra ingresada por el usuario.

   Returns:
       str: Texto formateado con el resumen del conteo.
   """


def contar(pal: str) -> str:
    tot_letras = len(pal)
    tot_vocales = 0
    tot_cons = 0
    for p in pal:
        if p in "aeiou":
            tot_vocales += 1
        else:
            tot_cons += 1
    return f"Palabra ingresada: {pal}\n Total de vocales: {tot_vocales}\n Total de consonantes: {tot_cons}\n Total de letras: {tot_letras}"


"""
   Valida si una contraseña cumple las reglas del sistema.

   La contraseña debe:
   - Tener más de 8 caracteres.
   - No ser igual al nombre de los usuarios del sistema.

   Args:
       nueva_contra (str): Contraseña propuesta por el usuario.

   Returns:
       str: Mensaje indicando si la contraseña es válida o no.
   """


def validar_contrasena(nueva_contra: str) -> str:
    if len(nueva_contra) > 8 and nueva_contra != user_invitado and nueva_contra != user_admin:
        return "Propuesta de nueva contraseña aceptada"
    else:
        return "La contraseña debe tener mas de 8 caracteres y no debe ser igual al nombre de usuario"


"""
   Realiza una operación matemática básica entre dos números.

   Operaciones soportadas:
       - "suma"
       - "resta"
       - "multiplicacion"
       - "division"

   Args:
       num_uno (float): Primer número.
       num_dos (float): Segundo número.
       oper (str): Operación a realizar.

   Returns:
       float: Resultado numérico de la operación.
       str: Mensaje de error si la operación no es válida
            o si se intenta dividir entre cero.
       None: Si no se reconoce la operación.
   """

# Usamos raise para lanzar un error cuando algo no es válido.
# En este caso, si el usuario intenta dividir entre cero,
# detenemos la función y enviamos una señal de que ocurrió un problema.
# La función no imprime el error, solo lo "lanza".
# El menú principal es quien se encarga de atraparlo y mostrar
# un mensaje bonito sin que el programa se cierre.
def calcular(num_uno: float, num_dos: float, oper: str) -> float:
    if oper == "suma":
        return num_uno + num_dos
    elif oper == "resta":
        return num_uno - num_dos
    elif oper == "multiplicacion":
        return num_uno * num_dos
    elif oper == "division":
        if num_dos == 0:
            raise ValueError("No se permite la división entre cero.")
        return round(num_uno / num_dos, 2)
    else:
        raise ValueError("No se permite la división entre cero.")


"""
    Devuelve la fecha actual si el rol es Administrador.
    Lanza PermissionError si no tiene permisos.
    """


def fecha_hoy_rol(rol_sesion: str) -> str:
    if rol_sesion != "Administrador":
        raise PermissionError("Acceso denegado. Se requiere rol Administrador.")

    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
        contar_palabras = contar(palabra)
        print(contar_palabras)
        mensaje = f"Se solicitó el conteo de la palabra {palabra}\n" + contar_palabras
    # Funcionalidad para averiguar la fecha actual, si el usuario tiene rol invitado, el sistema rrojará un mensaje de error
    elif cmd == "fecha_hoy":
        try:
            fecha = fecha_hoy_rol(rol)
            mensaje = f"[PseudoAgente] La fecha y hora actual es: {fecha}"
            print(mensaje)
        except PermissionError as e:
            mensaje = str(e)
            print(mensaje)
    elif cmd == "validar_pass":
        pass_correcta = False
        nueva_pass = ""
        while not pass_correcta:
            nueva_pass = input("Ingrese una propuesta de contraseña nueva: ")
            resultado_validacion = validar_contrasena(nueva_pass)
            print(resultado_validacion + f"\ncontraseña ingresada: {nueva_pass}")
            if resultado_validacion == "Propuesta de nueva contraseña aceptada":
                pass_correcta = True
        mensaje = f"Se ha solicitado validar la contraseña, contraseña ingresada {nueva_pass}"
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
            resultado_operacion = calcular(primer_numero, segundo_numero, operador)
            mensaje = f"Se ha solicitado realizar la operación {operador} entre el número {primer_numero} y {segundo_numero}"
        except ValueError as e:
            mensaje = str(e)
        print(mensaje)
    # Funcionalidad para mirar el historial de las conversaciones con el agente, el agente analiza cual es el comando ingresado
    # si es historial all, listará todo el historial almacenado, si es historial clear, se limpiará todo el historial
    # si identifica que solo solicita el historial, se solicitará al usuario ingresar una palabra clave, el sistema buscará
    # esa palabra dentro de las descripciones almacenadas en el historial, si encuentra coincidencias, se listarán con su iteración, rol y descripción,
    # si no encuentra coincidencias, se imprimirá un mensaje de error
    elif cmd_split[0] == "historial":
        if len(cmd_split) == 2:
            op = cmd_split[1]
            resultado_historial = gestionar_historial(historial_chat, op)
            mensaje = resultado_historial
            print(resultado_historial)
        else:
            palabra_clave = input("Ingresa la palabra clave a buscar: ").lower()
            resultado_historial = mensaje = gestionar_historial(historial_chat, palabra_clave)
            print(resultado_historial)
    else:
        print("------Comando desconocido. Intente de nuevo.-------")
        mensaje = "Se ha enviado un comando desconocido, el sistema no pudo reconocerlo y se solicitó intentar de nuevo."
    # De acuerdo con la petición hecha, en la variable d_log se guardan los datos de la operación
    # y posteriormente almacenarlos en el historial
    d_log: Recuerdo = {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       "cmd": cmd,
                       "rol": rol,
                       "descripción": mensaje}
    historial_chat.append(d_log)
