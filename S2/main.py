from datetime import date
# Importo el módulo datetime para poder usar la fecha actual más adelante.
# Es como decirle a Python: "necesito esa caja de herramientas de fechas".

# ─── Credenciales del sistema ────────────────────────────────────────────────
# Aquí guardo los usuarios válidos del sistema en un diccionario.
# Cada usuario tiene su contraseña y su rol (invitado o admin).
# Lo pongo en MAYÚSCULAS porque es un valor fijo que no cambia durante el programa.
USUARIOS = {
    "usuario": {"password": "123456",  "rol": "invitado"},
    "admin":    {"password": "123456",  "rol": "admin"},
}

# ─── Fase 1: Login ────────────────────────────────────────────────────────────
# Lógica del contador de intentos:
# Uso un contador `intentos` que arranca en 0 y sube 1 cada vez que el usuario
# se equivoca. El while corre mientras los intentos sean menores a 3 Y el
# usuario no haya ingresado correctamente (sesion_activa = False).
# Cuando intentos llega a 3 el while se corta solo, sin necesidad de break,
# y el programa termina porque nunca se llega a la Fase 2.

print("=" * 50)
print("      SISTEMA DE AGENTE - INICIO DE SESIÓN")
print("=" * 50)

# Preparo las variables antes del bucle para tenerlas limpias desde el inicio.
intentos = 0
sesion_activa = False  # Esta bandera me dice si alguien ya entró con éxito
usuario_actual = ""    # Aquí voy a guardar el nombre del usuario que entró
rol_actual = ""        # Y aquí su rol, para usarlo en los comandos de la Fase 3

while intentos < 3 and not sesion_activa:
    usuario_input = input("Usuario: ")
    password_input = input("Contraseña: ")

    # Primero reviso si el usuario existe en el diccionario,
    # y luego comparo la contraseña. Si las dos cosas son correctas, dejo pasar.
    if usuario_input in USUARIOS and USUARIOS[usuario_input]["password"] == password_input:
        sesion_activa = True
        usuario_actual = usuario_input
        rol_actual = USUARIOS[usuario_input]["rol"]
        print(f"\n[OK] Bienvenido, {usuario_actual}. Rol: {rol_actual}\n")
    else:
        intentos += 1
        restantes = 3 - intentos
        # Solo muestro intentos restantes si aún le quedan, para no confundir al usuario
        if restantes > 0:
            print(f"[Error] Credenciales incorrectas. Intentos restantes: {restantes}")

# Si salí del while sin que sesion_activa se pusiera en True,
# significa que agotó los 3 intentos → bloqueamos y cerramos.
if not sesion_activa:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
    exit()

# ─── Fase 2 y 3: Bucle principal del agente ──────────────────────────────────
# A partir de aquí el agente ya está "despierto" y escucha comandos.
# El while corre infinitamente hasta que el usuario escriba "salir".

# Inicializo la lista del historial vacía antes del bucle.
# Cada entrada será un diccionario con "autor" y "descripcion".
historial_chat = []

print("-" * 50)
print("Comandos disponibles: ping | contar | fecha_hoy | validar_pass | calculadora | historial | salir")
print("-" * 50)

sistema_activo = True
while sistema_activo:
    # .strip() quita espacios en blanco al inicio/final (si el usuario le pega espacio sin querer)
    # .lower() convierte a minúsculas para que "Ping", "PING" o "ping" sean lo mismo
    cmd = input("Agente> ").strip().lower()

    # ── ping ──────────────────────────────────────────────────────────────────
    # Comando de prueba básico: si el agente responde, significa que está vivo
    if cmd == "ping":
        print("pong!")
        historial_chat.append({"autor": usuario_actual, "descripcion": "Ejecutó comando ping"})

    # ── contar ────────────────────────────────────────────────────────────────
    elif cmd == "contar":
        frase = input("Ingresa una frase: ").lower()
        # Inicio los contadores en 0 antes del for, si no, Python no sabe de dónde partir
        tot_vocales = 0
        tot_cons = 0
        # Recorro letra por letra con el for
        for letra in frase:
            if letra in "aeiouáéíóú":
                tot_vocales += 1
            elif letra.isalpha():
                # .isalpha() me asegura que solo cuente letras reales,
                # ignorando espacios, comas, números, etc.
                tot_cons += 1
        print(f"Vocales: {tot_vocales} | Consonantes: {tot_cons} | Total letras: {tot_vocales + tot_cons}")
        historial_chat.append({"autor": usuario_actual, "descripcion": f"Contó letras de la frase: {frase}"})

    # ── fecha_hoy (solo admin) ────────────────────────────────────────────────
    # Aquí uso el rol que guardé en el login para decidir si mostrar la fecha o no.
    # Es el control de acceso: misma función, distinto resultado según quién entra.
    elif cmd == "fecha_hoy":
        if rol_actual == "admin":
            # date.today() viene del módulo que importé al principio
            print(f"Fecha de hoy: {date.today()}")
            historial_chat.append({"autor": usuario_actual, "descripcion": f"Consultó la fecha de hoy: {date.today()}"})
        else:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
            historial_chat.append({"autor": usuario_actual, "descripcion": "Intentó consultar fecha_hoy sin permisos de admin"})

    # ── validar_pass ──────────────────────────────────────────────────────────
    # Valido la contraseña en dos pasos: primero longitud, luego que no sea igual al usuario.
    # Los hago por separado para poder decirle exactamente qué está mal.
    elif cmd == "validar_pass":
        nueva = input("Propón una nueva contraseña: ")
        if len(nueva) < 8:
            # len() cuenta la cantidad de caracteres del string
            print("[Rechazada] La contraseña debe tener al menos 8 caracteres.")
            historial_chat.append({"autor": usuario_actual, "descripcion": "Validó contraseña: rechazada por longitud insuficiente"})
        elif nueva == usuario_actual:
            # Comparo con la variable que guardé en el login
            print("[Rechazada] La contraseña no puede ser igual a tu nombre de usuario.")
            historial_chat.append({"autor": usuario_actual, "descripcion": "Validó contraseña: rechazada por ser igual al usuario"})
        else:
            print("[OK] Contraseña válida.")
            historial_chat.append({"autor": usuario_actual, "descripcion": "Validó contraseña: aprobada"})

    # ── calculadora ───────────────────────────────────────────────────────────
    # Por qué uso float():
    # Todo lo que el usuario escribe con input() llega como texto (string).
    # Si no convierto, Python no puede hacer matemáticas: "5" + "3" sería "53"
    # (pega los textos), no 8. float() me permite trabajar con decimales también.
    # Si el usuario escribe letras en vez de un número, Python lanzaría un error
    # llamado ValueError, por eso uso try/except para atraparlo limpiamente.
    elif cmd == "calculadora":
        try:
            num1 = float(input("Primer número: "))
            operador = input("Operador (+, -, *, /): ").strip()
            num2 = float(input("Segundo número: "))

            if operador == "+":
                resultado = num1 + num2
            elif operador == "-":
                resultado = num1 - num2
            elif operador == "*":
                resultado = num1 * num2
            elif operador == "/":
                # Caso especial: dividir entre 0 es matemáticamente imposible,
                # si no lo controlo Python lanza un ZeroDivisionError y el programa explota
                if num2 == 0:
                    print("[Error] No se puede dividir entre cero.")
                    resultado = None
                else:
                    resultado = num1 / num2
            else:
                print("[Error] Operador no reconocido.")
                resultado = None

            # Solo imprimo si el resultado tiene un valor válido
            if resultado is not None:
                print(f"Resultado: {resultado}")
                historial_chat.append({"autor": usuario_actual, "descripcion": f"Calculó: {num1} {operador} {num2} = {resultado}"})

        except ValueError:
            # Llego aquí si el usuario escribió algo que no es número, como "abc"
            print("[Error] Debes ingresar números válidos.")
            historial_chat.append({"autor": usuario_actual, "descripcion": "Intentó usar calculadora con valores no numéricos"})

    # ── historial ─────────────────────────────────────────────────────────────
    # Uso .split() para separar el comando en partes: "historial all" → ["historial", "all"]
    # Así puedo detectar si viene un subcomando (all, clear) o solo "historial".
    # split() divide el string por espacios y devuelve una lista de palabras.
    elif cmd.startswith("historial"):
        partes = cmd.split()

        if len(partes) > 1 and partes[1] == "all":
            if not historial_chat:
                print("[PseudoAgente] El historial está vacío.")
            else:
                for entrada in historial_chat:
                    print(f"[{entrada['autor']}]: {entrada['descripcion']}")

        elif len(partes) > 1 and partes[1] == "clear":
            historial_chat.clear()
            print("[PseudoAgente] Historial eliminado.")

        else:
            palabra_clave = input("Ingresa la palabra clave a buscar: ").lower()
            coincidencias = 0
            for entrada in historial_chat:
                # Uso el operador "in" para verificar si una palabra está contenida dentro de otra.
                # En Python, "in" sobre strings funciona como una búsqueda de subcadena:
                # "arroz" in "Cocinar Arroz".lower() → True
                # Aplico .lower() a ambos lados para que la búsqueda sea insensible a mayúsculas.
                if palabra_clave in entrada["descripcion"].lower():
                    print(f"[{entrada['autor']}]: {entrada['descripcion']}")
                    coincidencias += 1
            if coincidencias == 0:
                print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")

    # ── salir ─────────────────────────────────────────────────────────────────
    # Cambio la bandera a False para que el while deje de correr y el programa termine
    elif cmd == "salir":
        print("Agente apagado. Vuelve pronto.")
        sistema_activo = False

    # ── comando desconocido ───────────────────────────────────────────────────
    # Si ningún elif coincidió, el usuario escribió algo que el agente no conoce
    else:
        print("Comando desconocido. Intenta de nuevo.")
