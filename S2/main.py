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
    elif cmd == "fecha_hoy":
        if rol_usuario == "invitado":
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
            continue

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        print(f"Fecha actual: {fecha_actual}")

    elif cmd == "validar_pass":
        nueva_pass = input("Ingrese la nueva contraseña: ")
        if len(nueva_pass) < 8 or nueva_pass == rol_usuario:
            print("La contraseña no cumple con las políticas de seguridad.")
        else:
            print("Contraseña válida. Se ha actualizado correctamente.")

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

    else:
        print("------Comando desconocido. Intente de nuevo.-------")