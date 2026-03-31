from datetime import datetime
from typing import Dict, List

# Los alias de tipo permiten que el código sea más legible y mantenible, ya que explícitamente
# definimos la estructura de la memoria del agente. Para que así entiendan rápidamente qué forma tiene cada dato sin analizar toda la lógica.
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


def contar_letras(palabra: str) -> str:
    tot_letras = len(palabra)
    tot_vocales = 0
    tot_cons = 0

    for letra in palabra:
        if letra in "aeiou":
            tot_vocales += 1
        else:
            tot_cons += 1

    return (
        f"Palabra ingresada: {palabra}\n"
        f"Total de vocales: {tot_vocales}\n"
        f"Total de consonantes: {tot_cons}\n"
        f"Total de letras: {tot_letras}"
    )


def obtener_fecha_actual(rol_usuario_func: str) -> str:
    if rol_usuario_func == "invitado":
        # Se lanza el error con raise y Python detiene la ejecución. El error viaja hasta el bloque try/except en el menú principal donde se atrapa
        # con except PermissionError para mostrar un mensaje bonito sin que el programa se rompa.
        raise PermissionError("Privilegios insuficientes")
    return datetime.now().strftime("%Y-%m-%d")


def validar_password(nueva_pass: str, rol_usuario_func: str) -> bool:
    return not (len(nueva_pass) < 8 or nueva_pass == rol_usuario_func)


def calculadora(num1_func: float, num2_func: float, operacion_func: str) -> float:
    if operacion_func == "+":
        return num1_func + num2_func
    if operacion_func == "-":
        return num1_func - num2_func
    if operacion_func == "*":
        return num1_func * num2_func
    if operacion_func == "/":
        if num2_func == 0:
            raise ValueError("No se puede dividir por cero.")
        return num1_func / num2_func
    raise ValueError("Operación no válida.")


def gestionar_historial(accion: str, memoria: MemoriaAgente) -> str:
    if accion == "all":
        if not memoria:
            return "[PseudoAgente] La memoria está vacía."

        lineas: List[str] = []
        for recuerdo in memoria:
            lineas.append(f"Autor: {recuerdo['autor']} | Acción: {recuerdo['descripcion']}")
        return "\n".join(lineas)

    if accion == "clear":
        memoria.clear()
        return "[PseudoAgente] Memoria borrada con éxito."

    coincidencias: List[str] = []
    for recuerdo in memoria:
        descripcion_min = recuerdo["descripcion"].lower()
        if accion in descripcion_min:
            coincidencias.append(
                f"-> Encontrado: [Autor: {recuerdo['autor']}] Mensaje: {recuerdo['descripcion']}"
            )

    if not coincidencias:
        return "[PseudoAgente] No encontré registros que coincidan con esa palabra."

    coincidencias.append(f"[PseudoAgente] Se encontraron {len(coincidencias)} coincidencias.")
    return "\n".join(coincidencias)

print("----- Iniciando el pseudoagente estilo consola -------")

user_admin = "admin"
pass_admin = "12345"

user_invitado = "invitado"
pass_invitado = "abcde"

intentos_maximos = 3
intentos_actuales = 0
autenticado = False
rol_usuario = ""
historial_chat: MemoriaAgente = []


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
    sistema_activo = True


sistema_activo = True
while sistema_activo:
    cmd = input("Agente>: ").lower()

    if cmd == "salir":
        print("------Agente apagado. Vuelve pronto.------")
        sistema_activo = False
    elif cmd == "ping":
        print("pong.")
        # Guardamos el recuerdo del comando ping ejecutado
        historial_chat.append({"autor": rol_usuario, "descripcion": "El usuario ejecuto el comando ping"})
    elif cmd =="contar":
        palabra_ingresada = input("Ingrese una palabra: ").lower()
        print(contar_letras(palabra_ingresada))
        # Guardamos el recuerdo con la palabra usada
        historial_chat.append({"autor": rol_usuario, "descripcion": f"Contó letras en la palabra: {palabra_ingresada}"})
    elif cmd == "fecha_hoy":
        try:
            fecha_actual = obtener_fecha_actual(rol_usuario)
            print(f"Fecha actual: {fecha_actual}")
            historial_chat.append({"autor": rol_usuario, "descripcion": f"Consultó la fecha actual: {fecha_actual}"})
        except PermissionError:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
            historial_chat.append({"autor": rol_usuario, "descripcion": "Intento fallido de ver fecha (Acceso denegado)"})

    elif cmd == "validar_pass":
        nueva_pass_ingresada = input("Ingrese la nueva contraseña: ")
        if validar_password(nueva_pass_ingresada, rol_usuario):
            print("Contraseña válida. Se ha actualizado correctamente.")
            historial_chat.append({"autor": rol_usuario, "descripcion": "Validó una nueva contraseña exitosamente"})
        else:
            print("La contraseña no cumple con las políticas de seguridad.")
            historial_chat.append({"autor": rol_usuario, "descripcion": "Intento de cambio de pass inválido"})

    elif cmd == "calculadora":
        try:
            num1 = float(input("Ingrese el primer número: "))
            num2 = float(input("Ingrese el segundo número: "))
            operacion = input("Ingrese la operación (+, -, *, /): ")

            resultado = calculadora(num1, num2, operacion)
            print(f"Resultado: {resultado}")
            historial_chat.append({"autor": rol_usuario, "descripcion": f"Realizó una operación: {num1} {operacion} {num2} = {resultado}"})
        except ValueError as error:
            if str(error) == "No se puede dividir por cero." or str(error) == "Operación no válida.":
                print(f"Error: {error}")
            else:
                print("Error: Debe ingresar valores numéricos válidos.")

    elif cmd.startswith("historial"):
        partes = cmd.split() 
        if len(partes) > 1 and partes[1] == "all":
            print(gestionar_historial("all", historial_chat))

        elif len(partes) > 1 and partes[1] == "clear":
            print(gestionar_historial("clear", historial_chat))
        else:
            busqueda = input("Ingresa la palabra clave a buscar: ").lower()
            print(gestionar_historial(busqueda, historial_chat))
    else:
        print("------Comando desconocido. Intente de nuevo.-------")