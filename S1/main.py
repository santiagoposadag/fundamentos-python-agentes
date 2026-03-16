from datetime import date

# ─── Credenciales del sistema ────────────────────────────────────────────────
USUARIOS = {
    "invitado": {"password": "123456",  "rol": "invitado"},
    "admin":    {"password": "123456",  "rol": "admin"},
}

# ─── Fase 1: Login ────────────────────────────────────────────────────────────
# Uso un contador `intentos` que arranca en 0 y sube 1 cada vez que el usuario
# se equivoca. El while corre mientras los intentos sean menores a 3 Y el
# usuario no haya ingresado correctamente (sesion_activa = False).
# Cuando intentos llega a 3 el while se corta solo, sin necesidad de break,
# y el programa termina porque nunca se llega a la Fase 2.

print("=" * 50)
print("      SISTEMA DE AGENTE - INICIO DE SESIÓN")
print("=" * 50)

intentos = 0
sesion_activa = False
usuario_actual = ""
rol_actual = ""

while intentos < 3 and not sesion_activa:
    usuario_input = input("Usuario: ")
    password_input = input("Contraseña: ")

    if usuario_input in USUARIOS and USUARIOS[usuario_input]["password"] == password_input:
        sesion_activa = True
        usuario_actual = usuario_input
        rol_actual = USUARIOS[usuario_input]["rol"]
        print(f"\n[OK] Bienvenido, {usuario_actual}. Rol: {rol_actual}\n")
    else:
        intentos += 1
        restantes = 3 - intentos
        if restantes > 0:
            print(f"[Error] Credenciales incorrectas. Intentos restantes: {restantes}")

if not sesion_activa:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
    exit()

# ─── Fase 2 y 3: Bucle principal del agente ──────────────────────────────────
print("-" * 50)
print("Comandos disponibles: ping | contar | fecha_hoy | validar_pass | calculadora | salir")
print("-" * 50)

sistema_activo = True
while sistema_activo:
    cmd = input("Agente> ").strip().lower()

    # ── ping ──────────────────────────────────────────────────────────────────
    if cmd == "ping":
        print("pong!")

    # ── contar ────────────────────────────────────────────────────────────────
    elif cmd == "contar":
        frase = input("Ingresa una frase: ").lower()
        tot_vocales = 0
        tot_cons = 0
        for letra in frase:
            if letra in "aeiouáéíóú":
                tot_vocales += 1
            elif letra.isalpha():
                tot_cons += 1
        print(f"Vocales: {tot_vocales} | Consonantes: {tot_cons} | Total letras: {tot_vocales + tot_cons}")

    # ── fecha_hoy (solo admin) ────────────────────────────────────────────────
    elif cmd == "fecha_hoy":
        if rol_actual == "admin":
            print(f"Fecha de hoy: {date.today()}")
        else:
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")

    # ── validar_pass ──────────────────────────────────────────────────────────
    elif cmd == "validar_pass":
        nueva = input("Propón una nueva contraseña: ")
        if len(nueva) < 8:
            print("[Rechazada] La contraseña debe tener al menos 8 caracteres.")
        elif nueva == usuario_actual:
            print("[Rechazada] La contraseña no puede ser igual a tu nombre de usuario.")
        else:
            print("[OK] Contraseña válida.")

    # ── calculadora ───────────────────────────────────────────────────────────
    # Se usa int() / float() porque input() siempre devuelve texto (str).
    # Sin la conversión, Python no puede hacer aritmética: "5" + "3" = "53"
    # (concatenación de strings), no 8. Si el usuario escribe letras, el
    # programa lanzaría un ValueError; por eso lo envuelvo en try/except.
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
                if num2 == 0:
                    print("[Error] No se puede dividir entre cero.")
                    resultado = None
                else:
                    resultado = num1 / num2
            else:
                print("[Error] Operador no reconocido.")
                resultado = None

            if resultado is not None:
                print(f"Resultado: {resultado}")

        except ValueError:
            print("[Error] Debes ingresar números válidos.")

    # ── salir ─────────────────────────────────────────────────────────────────
    elif cmd == "salir":
        print("Agente apagado. Vuelve pronto.")
        sistema_activo = False

    # ── comando desconocido ───────────────────────────────────────────────────
    else:
        print("Comando desconocido. Intenta de nuevo.")
