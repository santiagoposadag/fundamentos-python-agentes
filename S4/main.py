from agente import PseudoAgente, AgenteAdmin

# ─── Credenciales del sistema ────────────────────────────────────────────────
USUARIOS = {
    "usuario": {"password": "123456", "rol": "invitado"},
    "admin":   {"password": "123456", "rol": "admin"},
}

# ─── Fase 1: Login ────────────────────────────────────────────────────────────
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

# ─── Instanciar el agente según rol ──────────────────────────────────────────
# Si el usuario es admin → AgenteAdmin (historial sin costo de tokens)
# Si es invitado → PseudoAgente normal
if rol_actual == "admin":
    agente = AgenteAdmin(usuario_actual)
else:
    agente = PseudoAgente(usuario_actual)

print(f"[Sistema] Agente '{agente.nombre}' iniciado | Tokens: {agente.tokens}")

# ─── Fase 2 y 3: Bucle principal del agente ──────────────────────────────────
# El historial ya no flota aquí — vive en agente.historial_chat
print("-" * 50)
print("Comandos: ping | contar | fecha_hoy | validar_pass | calculadora | historial | dado | salir")
print("-" * 50)

sistema_activo = True
while sistema_activo:
    print(f"[Tokens: {agente.tokens}]")
    cmd = input("Agente> ").strip().lower()

    # ── ping ──────────────────────────────────────────────────────────────────
    if cmd == "ping":
        print(agente.ping())

    # ── contar ────────────────────────────────────────────────────────────────
    elif cmd == "contar":
        frase = input("Ingresa una frase: ").lower()
        print(agente.contar_letras(frase))

    # ── fecha_hoy (solo admin) ────────────────────────────────────────────────
    elif cmd == "fecha_hoy":
        try:
            print(agente.fecha_hoy(rol_actual))
        except PermissionError as e:
            print(f"[Acceso Denegado] {e}")

    # ── validar_pass ──────────────────────────────────────────────────────────
    elif cmd == "validar_pass":
        nueva = input("Propón una nueva contraseña: ")
        print(agente.validar_password(nueva, usuario_actual))

    # ── calculadora ───────────────────────────────────────────────────────────
    elif cmd == "calculadora":
        try:
            num1 = float(input("Primer número: "))
            operador = input("Operador (+, -, *, /): ").strip()
            num2 = float(input("Segundo número: "))
            print(agente.calculadora(num1, operador, num2))
        except ValueError:
            print("[Error] Debes ingresar números válidos.")

    # ── historial ─────────────────────────────────────────────────────────────
    elif cmd.startswith("historial"):
        partes = cmd.split()
        accion = partes[1] if len(partes) > 1 else input("Ingresa la palabra clave a buscar: ").lower()
        print(agente.gestionar_historial(accion))

    # ── dado ──────────────────────────────────────────────────────────────────
    elif cmd == "dado":
        print(agente.lanzar_dado())

    # ── salir ─────────────────────────────────────────────────────────────────
    elif cmd == "salir":
        print("Agente apagado. Vuelve pronto.")
        sistema_activo = False

    # ── comando desconocido ───────────────────────────────────────────────────
    else:
        print("Comando desconocido. Intenta de nuevo.")

    # ── monitor de tokens ─────────────────────────────────────────────────────
    # No usamos break — cambiamos la bandera para que el while termine limpiamente
    if agente.tokens <= 0 and sistema_activo:
        print(f"\n[Sistema] {agente.nombre} se quedó sin energía. Apagando...")
        sistema_activo = False
