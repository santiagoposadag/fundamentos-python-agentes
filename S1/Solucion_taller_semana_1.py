from datetime import date

#Creo un diccionario para guardar los diferentes perfiles con su respectivo password
CREDENCIALES = {
    "invitado": {"password": "invitado123", "rol": "invitado"},
    "admin":    {"password": "admin123",    "rol": "admin"},
}

#Encabezado del agente
print("=" * 45)
print("       SISTEMA DE AUTENTICACIÓN DEL AGENTE")
print("=" * 45)

#Creo variables que voy a utilizar en validaciones
sesion_activa = False
usuario_actual = ""
rol_actual = ""
intentos = 0

#Creo bucle para el login
while intentos < 3:
    usuario_input = input("Usuario: ").strip()
    password_input = input("Contraseña: ").strip()

    # Verifico si el usuario existe Y su contraseña coincide
    if usuario_input in CREDENCIALES and CREDENCIALES[usuario_input]["password"] == password_input:
        sesion_activa = True
        usuario_actual = usuario_input
        rol_actual = CREDENCIALES[usuario_input]["rol"]
        print(f"\n[OK] Acceso concedido. Bienvenido, {usuario_actual} (rol: {rol_actual}).\n")
        break
    else:
        intentos += 1
        restantes = 3 - intentos
        if restantes > 0:
            print(f"[Error] Credenciales incorrectas. Intentos restantes: {restantes}\n")

# Si terminé el while sin éxito, bloqueo el sistema y termina el programa
if not sesion_activa:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
    exit()  

#Continuo con las siguientes funciones manteniendo el sistema activo
print("=" * 45)
print("        AGENTE ACTIVO — ESPERANDO COMANDOS")
print("""  Comandos: 
      ping          -> Responde pong!
      contar        -> Cuenta vocales, Consonantes y Total de letras
      fecha_hoy     -> Genera la fecha actual si lo consulta Admin
      validar_pass  -> Cambia Password
      calculadora   -> suma, resta, multiplica ó Divide
      salir         -> Sale del sistema
      """)
print("=" * 45)

sistema_activo = True

while sistema_activo:
    cmd = input("\nAgente> ").strip().lower()
    #Utilizo if/elif/else para ingresar a funcion dependiendo de la solicitada
    if cmd == "salir":
        print("------ Agente apagado. Hasta pronto. ------")
        sistema_activo = False

    elif cmd == "ping":
        print("pong!")

    elif cmd == "contar":
        frase = input("Ingresa una frase: ").lower()
        tot_vocales = 0
        tot_cons = 0

        # Recorro letra por letra con for; solo cuento letras del alfabeto
        for letra in frase:
            if letra in "aeiouáéíóú":
                tot_vocales += 1
            elif letra.isalpha():
                tot_cons += 1

        print(f"  Frase       : '{frase}'")
        print(f"  Vocales     : {tot_vocales}")
        print(f"  Consonantes : {tot_cons}")
        print(f"  Total letras: {tot_vocales + tot_cons}")

    elif cmd == "fecha_hoy":
        if rol_actual == "admin":
            hoy = date.today()
            # Doy formato a la fecha
            print(f"  Fecha actual: {hoy.strftime('%d/%m/%Y')}")
        else:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")

    elif cmd == "validar_pass":
        nueva_pass = input("Propón una contraseña nueva: ").strip()
        if len(nueva_pass) < 8:
            print("[Rechazada] La contraseña debe tener al menos 8 caracteres.")
        elif nueva_pass == usuario_actual:
            print("[Rechazada] La contraseña no puede ser igual a tu nombre de usuario.")
        else:
            print("[Aceptada] La contraseña es válida.")

    elif cmd == "calculadora":
        try:
            n1 = float(input("  Ingresa el primer número : "))
            op = input("  Ingresa el operador (+, -, *, /): ").strip()
            n2 = float(input("  Ingresa el segundo número: "))
        except ValueError:
            print("[Error] Debes ingresar números válidos.")
        else:
            if op == "+":
                print(f"  Resultado: {n1} + {n2} = {n1 + n2}")
            elif op == "-":
                print(f"  Resultado: {n1} - {n2} = {n1 - n2}")
            elif op == "*":
                print(f"  Resultado: {n1} * {n2} = {n1 * n2}")
            elif op == "/":
                if n2 == 0:
                    print("[Error] No se puede dividir entre cero.")
                else:
                    print(f"  Resultado: {n1} / {n2} = {n1 / n2}")
            else:
                print(f"[Error] Operador '{op}' no reconocido. Usa +, -, * o /.")

    else:
        print("------ Comando desconocido. Intenta de nuevo. ------")

