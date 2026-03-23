import datetime
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
    historial_chat = []  # Lista para almacenar el historial de comandos y respuestas
    sistema_activo = True
    mensaje = ""
    # Ciclo principal del menú
    while sistema_activo:
        cmd = input("Agente>: ").lower()
        # =========================
        # Comando historial: búsqueda y gestión de memoria
        # =========================
        if cmd.startswith("historial"):
            partes = cmd.split()  # Uso de .split() para separar el comando y manejar variantes como 'historial all' o 'historial clear'.
            # Si el usuario ingresa 'historial all', muestra todo el historial
            if len(partes) == 2 and partes[1] == "all":  # Aquí se identifica la variante 'historial all' usando el resultado de .split().
                if len(historial_chat) == 0:
                    print("[PseudoAgente] No hay historial para mostrar.")
                else:
                    print("[PseudoAgente] Historial completo:")
                    for i, d in enumerate(historial_chat, 1):
                        print(f"{i}. [{d['timestamp']}] ({d['rol']}) {d['cmd']}: {d['descripcion']}")
                mensaje = "Se ha mostrado todo el historial."
            # Si el usuario ingresa 'historial clear', borra el historial
            elif len(partes) == 2 and partes[1] == "clear":  # Aquí se identifica la variante 'historial clear' usando el resultado de .split().
                historial_chat.clear()
                print("[PseudoAgente] Historial borrado correctamente.")
                mensaje = "Se ha borrado el historial."
            # Si solo ingresa 'historial', entra en modo búsqueda
            elif len(partes) == 1:
                if len(historial_chat) == 0:
                    print("[PseudoAgente] No hay historial para buscar.")
                else:
                    palabra = input("Ingresa la palabra clave a buscar: ").lower()
                    coincidencias = 0
                    # Uso 'in' para saber si la palabra clave está "dentro" de la descripción (respuesta a la primera pregunta).
                    # Aplico .lower() a ambos para que la búsqueda no distinga mayúsculas/minúsculas.
                    for d in historial_chat:
                        if palabra in d["descripcion"].lower():  # Aquí se verifica si una palabra está dentro de otra usando 'in'.
                            coincidencias += 1
                            print(f"[{d['timestamp']}] ({d['rol']}) {d['cmd']}: {d['descripcion']}")
                    if coincidencias == 0:
                        print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")
                    else:
                        print(f"[PseudoAgente] Se encontraron {coincidencias} coincidencia(s).")
                mensaje = f"Se realizó una búsqueda en el historial con la palabra clave." 
            else:
                print("[PseudoAgente] Opción de historial no reconocida. Usa 'historial', 'historial all' o 'historial clear'.")
                mensaje = "Opción de historial no reconocida."
        # =========================
        # Fin comando historial
        # =========================
        # Comando para salir del sistema
        # Comando para salir del sistema
        elif cmd == "salir":
            print("---Agente Apagado. Vuelve Pronto.-------")
            sistema_activo = False
            mensaje = "Se ha solicitado terminar la sesión."
        # Comando ping
        elif cmd == "ping":
            print("pong")
            mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
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
            mensaje = f"""Se solicitó el conteo de la palabra {palabra}, dando como resultados:
            Vocales: {tot_vocales}
            Consonantes: {tot_cons}
            Total: {tot_letras}"""
        # Comando fecha_hoy: solo admin puede ver la fecha
        elif cmd == "fecha_hoy":
            if rol == "admin":
                import datetime
                mensaje = f"Se ha consultado la fecha actual: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                print(mensaje)
            else:
                mensaje = "[Acceso Denegado] Este comando requiere privilegios de administrador."
                print(mensaje)
        # Comando validar_pass: valida nueva contraseña
        elif cmd == "validar_pass":
            nueva = input("Propuesta de nueva contraseña: ")
            # Primero validamos que no sea igual al usuario
            if nueva == usuario:
                print("La contraseña no puede ser igual al nombre de usuario.")
                mensaje = "Intento fallido: la contraseña es igual al nombre de usuario."
            elif len(nueva) < 8:
                print("La contraseña debe tener al menos 8 caracteres.")
                mensaje = "Intento fallido: la contraseña tiene menos de 8 caracteres."
            else:
                print("Contraseña válida.")
                mensaje = "Contraseña propuesta válida."
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
                    resultado = n1 + n2
                    print("Resultado:", resultado)
                    mensaje = f"Se realizó una suma: {n1} + {n2} = {resultado}"
                elif op == "-":
                    resultado = n1 - n2
                    print("Resultado:", resultado)
                    mensaje = f"Se realizó una resta: {n1} - {n2} = {resultado}"
                elif op == "*":
                    resultado = n1 * n2
                    print("Resultado:", resultado)
                    mensaje = f"Se realizó una multiplicación: {n1} * {n2} = {resultado}"
                elif op == "/":
                    if n2 == 0:
                        print("No se puede dividir por cero.")
                        mensaje = "Intento fallido: división por cero."
                    else:
                        resultado = n1 / n2
                        print("Resultado:", resultado)
                        mensaje = f"Se realizó una división: {n1} / {n2} = {resultado}"
                else:
                    print("Operador no válido.")
                    mensaje = "Operador no válido en la calculadora."
            except ValueError:
                print("Debes ingresar números válidos.")
                mensaje = "Error: se ingresaron valores no numéricos en la calculadora."
        # Comando desconocido
        else:            
            mensaje = "Comando no existe. Intente de nuevo"
            print(mensaje)
        # TO-DO: Taller de la semana2 - Búsqueda de memoria
        d_log = {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "cmd": cmd,
                "rol": rol,
                "descripcion": mensaje}
        historial_chat.append(d_log)
        # El historial solo se imprime en los comandos 'historial' o 'historial all'.