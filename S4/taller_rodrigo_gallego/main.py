from agente import PseudoAgente, AgenteAdmin

# Login básico
usuario: str = input("Usuario: ").strip()
contrasena: str = input("Contraseña: ").strip()

# Se define la variable 'tries' para limitar los intentos de login a 3 (1 inicial + 2 adicionales)
tries: int = 2
rol_actual: str = ""

# El bucle while se ejecuta mientras las credenciales sean incorrectas y queden intentos disponibles
while not (
    (usuario == "admin" and contrasena == "admin") or 
    (usuario == "invitado" and contrasena == "invitado")
    ) and tries > 0:
    print(f"[Alerta] Credenciales incorrectas. Intentos restantes: {tries}")
    usuario: str = input("Usuario: ").strip()
    contrasena: str = input("Contraseña: ").strip()
    tries -= 1

# Si después de 3 intentos las credenciales siguen siendo incorrectas, se bloquea el acceso
if not (
    (usuario == "admin" and contrasena == "admin") or 
    (usuario == "invitado" and contrasena == "invitado")
    ):
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
    exit()

rol_actual = usuario  # Asignamos el rol basado en el usuario ingresado
print(f"Bienvenido, {usuario}.")

if rol_actual == "admin":
    agente = AgenteAdmin(usuario)  # Admin 
else:
    agente = PseudoAgente(usuario, rol_actual)  # Invitado

nombre_agente = input("Ingrese el nombre del pseudoagente: ").strip()

try:
    if nombre_agente:
        agente.iniciar(nombre_agente)
    else:
        agente.iniciar()
except RuntimeError as re:
    print(f"[Sesión Finalizada] {re}")