from datetime import datetime

print("----- Iniciando el pseudoagente estilo consola -------")

user_admin = "admin"
pass_admin = "12345"

user_invitado = "invitado"
pass_invitado = "abcde"

intentos_maximos = 3
intentos_actuales = 0
autenticado = False
rol_usuario = ""
historial_chat = []


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
        palabra = input("Ingrese una palabra: ").lower()
        tot_letras = len(palabra)
        tot_vocales = 0
        tot_cons = 0
        
        for p in palabra:
            if p in "aeiou":
                tot_vocales +=1
            else:
                tot_cons +=1
        
        print(f"Palabra ingresada: {palabra}")
        print(f"Total de vocales: {tot_vocales}")
        print(f"Total de consonantes: {tot_cons}")
        print(f"Total de letras: {tot_letras}")
        # Guardamos el recuerdo con la palabra usada
        historial_chat.append({"autor": rol_usuario, "descripcion": f"Contó letras en la palabra: {palabra}"})
    elif cmd == "fecha_hoy":
        if rol_usuario == "invitado":
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
            historial_chat.append({"autor": rol_usuario, "descripcion": "Intento fallido de ver fecha (Acceso denegado)"})
            continue

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        print(f"Fecha actual: {fecha_actual}")
        historial_chat.append({"autor": rol_usuario, "descripcion": f"Consultó la fecha actual: {fecha_actual}"})

    elif cmd == "validar_pass":
        nueva_pass = input("Ingrese la nueva contraseña: ")
        if len(nueva_pass) < 8 or nueva_pass == rol_usuario:
            print("La contraseña no cumple con las políticas de seguridad.")
            historial_chat.append({"autor": rol_usuario, "descripcion": "Intento de cambio de pass inválido"})
        else:
            print("Contraseña válida. Se ha actualizado correctamente.")
            historial_chat.append({"autor": rol_usuario, "descripcion": "Validó una nueva contraseña exitosamente"})

    elif cmd == "calculadora":
#Se hace necesario convertir a float los valores de los input para poder permitir las operaciones matemáticas que se realizarán sobre ellos. 
        num1 = float(input("Ingrese el primer número: "))
        num2 = float(input("Ingrese el segundo número: "))
        operacion = input("Ingrese la operación (+, -, *, /): ")

        if operacion == "+":
            resultado = num1 + num2
        elif operacion == "-":
            resultado = num1 - num2
        elif operacion == "*":
            resultado = num1 * num2
        elif operacion == "/":
            if num2 != 0:
                resultado = num1 / num2
            else:
                print("Error: No se puede dividir por cero.")
                continue
        else:
            print("Operación no válida.")
            continue

        print(f"Resultado: {resultado}")
        historial_chat.append({"autor": rol_usuario, "descripcion": f"Realizó una operación: {num1} {operacion} {num2} = {resultado}"})

    elif cmd.startswith("historial"):
        partes = cmd.split() 
        if len(partes) > 1 and partes[1] == "all":
            if not historial_chat:
                print("[PseudoAgente] La memoria está vacía.")
            for memoria in historial_chat:
                print(f"Autor: {memoria['autor']} | Acción: {memoria['descripcion']}")

        elif len(partes) > 1 and partes[1] == "clear":
            historial_chat.clear()
            print("[PseudoAgente] Memoria borrada con éxito.")
        else:
            busqueda = input("Ingresa la palabra clave a buscar: ").lower()
            coincidencias = 0
            
            for memoria in historial_chat:
                descripcion_min = memoria["descripcion"].lower()
                # Logré saber si una palabra estaba dentro de otra usando el operador in que busca dentro de otra adena en un string
                # Resolví las singularidades del comando usando .split() para dividir la entrada en una lista y evaluar así su contenido
                if busqueda in descripcion_min:
                    print(f"-> Encontrado: [Autor: {memoria['autor']}] Mensaje: {memoria['descripcion']}")
                    coincidencias += 1
            
            if coincidencias == 0:
                print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")
            else:
                print(f"[PseudoAgente] Se encontraron {coincidencias} coincidencias.")
    else:
        print("------Comando desconocido. Intente de nuevo.-------")