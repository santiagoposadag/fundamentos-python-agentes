from datetime import date

# ─── Contratos de Memoria ──────────────────────────────────────
# Darle un alias a la estructura de datos no es solo comodidad: cuando trabajamos
# con modelos de IA (LLMs), cada herramienta (Tool) necesita un contrato claro
# sobre qué datos recibe y devuelve. Si mañana cambiamos "descripcion" por
# "content", solo tocamos el alias y todas las funciones que usan MemoriaAgente
# se actualizan solas. Es la misma razón por la que los LLMs reciben esquemas
# JSON tipados: sin un contrato, el modelo no sabe cómo procesar la memoria.
# Usamos la sintaxis moderna `type` disponible desde Python 3.12.
type Recuerdo = dict[str, str]
type MemoriaAgente = list[Recuerdo]

# ─── Credenciales del sistema ────────────────────────────────────────────────
USUARIOS = {
    "usuario": {"password": "123456",  "rol": "invitado"},
    "admin":    {"password": "123456",  "rol": "admin"},
}

# ─── Tools ────────────────────────────────────────────────────────────────────
# Antes (Semana 2): toda la lógica vivía dentro del while. El bucle hacía de
# todo: recibir input, procesar datos y mostrar resultados. Eso lo hacía
# difícil de mantener y de reutilizar.
#
# Ahora (Semana 3): cada comando se extrae a una función independiente.
# El while solo hace de "recepcionista": recibe el comando, llama la función
# e imprime lo que ella retorna. Así cada función tiene una sola responsabilidad.
#
# Por qué definirlas con tipos (frase: str) -> str:
# Los type hints son el "contrato" de la función. Le dicen a Python, al IDE
# y a cualquier LLM exactamente qué datos entran y qué datos salen,
# sin tener que leer todo el cuerpo de la función.

# ── Tool: contar_letras ───────────────────────────────────────────────────────
# Antes: el for y los contadores estaban pegados dentro del elif cmd == "contar"
# Ahora: es una función pura — recibe un str, retorna un str, sin efectos secundarios.
# "Pura" = no depende de variables externas ni imprime nada por su cuenta.
def contar_letras(frase: str) -> str:
    """
    Cuenta vocales y consonantes de una frase.

    Recorre letra por letra usando un for. Solo cuenta caracteres
    alfabéticos (.isalpha()), ignorando espacios, números y símbolos.

    Args:
        frase: texto en minúsculas a analizar.
    Returns:
        String con el conteo de vocales, consonantes y total de letras.
    """
    tot_vocales = 0
    tot_cons = 0
    for letra in frase:
        if letra in "aeiouáéíóú":
            tot_vocales += 1
        elif letra.isalpha():
            tot_cons += 1
    return f"Vocales: {tot_vocales} | Consonantes: {tot_cons} | Total letras: {tot_vocales + tot_cons}"


# ── Tool: validar_password ────────────────────────────────────────────────────
# Antes: los if/elif de validación estaban dentro del while con print() mezclado.
# Ahora: recibe los dos datos que necesita (contraseña nueva y usuario actual)
# y retorna el veredicto. El while solo imprime lo que ella devuelva.
# Recibe `usuario` como parámetro en lugar de usar la variable global usuario_actual,
# esto la hace independiente y reutilizable en cualquier contexto.
def validar_password(nueva: str, usuario: str) -> str:
    """
    Valida que una nueva contraseña cumpla las reglas de seguridad.

    Reglas aplicadas en orden:
      1. Mínimo 8 caracteres.
      2. No puede ser igual al nombre de usuario.

    Args:
        nueva:   contraseña propuesta por el usuario.
        usuario: nombre de usuario actual (para evitar coincidencias).
    Returns:
        String con el resultado de la validación.
    """
    if len(nueva) < 8:
        return "[Rechazada] La contraseña debe tener al menos 8 caracteres."
    elif nueva == usuario:
        return "[Rechazada] La contraseña no puede ser igual a tu nombre de usuario."
    return "[OK] Contraseña válida."


# ── Tool: calculadora ─────────────────────────────────────────────────────────
# Antes: el try/except y toda la aritmética estaban en el while.
# Ahora: la función recibe los números ya convertidos a float. La conversión
# (float(input(...))) se hace en el while y si falla, el except ValueError
# del while lo atrapa — la función nunca recibe texto, solo números válidos.
# Esto separa dos responsabilidades: "obtener input" (while) vs "calcular" (función).
def calculadora(num1: float, operador: str, num2: float) -> str:
    """
    Realiza operaciones aritméticas básicas entre dos números.

    Soporta: +, -, *, /. Protege contra división por cero y operadores
    no reconocidos. El try/except que llama a esta función atrapa
    el ValueError si el usuario ingresó texto en lugar de números.

    Args:
        num1:     primer operando.
        operador: símbolo de la operación (+, -, *, /).
        num2:     segundo operando.
    Returns:
        String con el resultado o mensaje de error.
    """
    if operador == "+":
        resultado = num1 + num2
    elif operador == "-":
        resultado = num1 - num2
    elif operador == "*":
        resultado = num1 * num2
    elif operador == "/":
        if num2 == 0:
            return "[Error] No se puede dividir entre cero."
        resultado = num1 / num2
    else:
        return "[Error] Operador no reconocido."
    return f"Resultado: {resultado}"


# ── Tool: gestionar_historial ─────────────────────────────────────────────────
# Antes: los tres casos (all, clear, búsqueda) estaban en el while con prints.
# Ahora: recibe la acción ya parseada y la lista de memoria, y retorna el texto.
# Usar `memoria: MemoriaAgente` en vez de `memoria: list` hace el contrato claro:
# quien llame esta función sabe exactamente qué estructura debe pasar.
# El while le pasa historial_chat directamente — las listas en Python se pasan
# por referencia, por eso memoria.clear() dentro de la función sí vacía el original.
def gestionar_historial(accion: str, memoria: MemoriaAgente) -> str:
    """
    Administra la memoria del agente: muestra, limpia o busca registros.

    Recibe la acción ya parseada (all, clear, o palabra clave) y la lista
    de recuerdos. No usa print() — devuelve el texto para que el bucle
    principal decida cómo mostrarlo.

    Args:
        accion:  "all" para ver todo, "clear" para borrar,
                 cualquier otro texto se trata como palabra clave de búsqueda.
        memoria: lista de recuerdos del agente (MemoriaAgente).
    Returns:
        String con el resultado de la operación solicitada.
    """
    if accion == "all":
        if not memoria:
            return "[PseudoAgente] El historial está vacío."
        return "\n".join(f"[{e['autor']}]: {e['descripcion']}" for e in memoria)

    elif accion == "clear":
        memoria.clear()
        return "[PseudoAgente] Historial eliminado."

    else:
        # Uso "in" para verificar si la palabra clave está contenida en la descripción.
        # En Python, "in" sobre strings busca subcadenas: "ping" in "Ejecutó comando ping" → True
        # Aplico .lower() a ambos lados para que la búsqueda ignore mayúsculas/minúsculas.
        coincidencias = [
            f"[{e['autor']}]: {e['descripcion']}"
            for e in memoria
            if accion in e["descripcion"].lower()
        ]
        if not coincidencias:
            return "[PseudoAgente] No encontré registros que coincidan con esa palabra."
        return "\n".join(coincidencias)


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

# ─── Fase 2 y 3: Bucle principal del agente ──────────────────────────────────
historial_chat: MemoriaAgente = []

print("-" * 50)
print("Comandos disponibles: ping | contar | fecha_hoy | validar_pass | calculadora | historial | salir")
print("-" * 50)

sistema_activo = True
while sistema_activo:
    cmd = input("Agente> ").strip().lower()

    # ── ping ──────────────────────────────────────────────────────────────────
    if cmd == "ping":
        print("pong!")
        historial_chat.append({"autor": usuario_actual, "descripcion": "Ejecutó comando ping"})

    # ── contar ────────────────────────────────────────────────────────────────
    elif cmd == "contar":
        frase = input("Ingresa una frase: ").lower()
        print(contar_letras(frase))
        historial_chat.append({"autor": usuario_actual, "descripcion": f"Contó letras de la frase: {frase}"})

    # ── fecha_hoy (solo admin) ────────────────────────────────────────────────
    elif cmd == "fecha_hoy":
        try:
            # El raise lanza un PermissionError en este punto exacto cuando el rol no es admin.
            # Python interrumpe la ejecución normal y busca hacia arriba en el call stack
            # el except más cercano que sepa manejar PermissionError — lo encuentra aquí mismo,
            # en el except de abajo, y ejecuta ese bloque en lugar de colapsar el programa.
            if rol_actual != "admin":
                raise PermissionError("Privilegios insuficientes")
            print(f"Fecha de hoy: {date.today()}")
            historial_chat.append({"autor": usuario_actual, "descripcion": f"Consultó la fecha de hoy: {date.today()}"})
        except PermissionError as e:
            print(f"[Acceso Denegado] {e}")
            historial_chat.append({"autor": usuario_actual, "descripcion": "Intentó consultar fecha_hoy sin permisos de admin"})

    # ── validar_pass ──────────────────────────────────────────────────────────
    elif cmd == "validar_pass":
        nueva = input("Propón una nueva contraseña: ")
        resultado = validar_password(nueva, usuario_actual)
        print(resultado)
        historial_chat.append({"autor": usuario_actual, "descripcion": f"Validó contraseña: {resultado}"})

    # ── calculadora ───────────────────────────────────────────────────────────
    elif cmd == "calculadora":
        try:
            num1 = float(input("Primer número: "))
            operador = input("Operador (+, -, *, /): ").strip()
            num2 = float(input("Segundo número: "))
            resultado = calculadora(num1, operador, num2)
            print(resultado)
            historial_chat.append({"autor": usuario_actual, "descripcion": f"Calculó: {num1} {operador} {num2} → {resultado}"})
        except ValueError:
            print("[Error] Debes ingresar números válidos.")
            historial_chat.append({"autor": usuario_actual, "descripcion": "Intentó usar calculadora con valores no numéricos"})

    # ── historial ─────────────────────────────────────────────────────────────
    # Uso .split() para separar el comando en partes: "historial all" → ["historial", "all"]
    # Así detecto el subcomando (all, clear) o trato el resto como palabra clave de búsqueda.
    elif cmd.startswith("historial"):
        partes = cmd.split()
        accion = partes[1] if len(partes) > 1 else input("Ingresa la palabra clave a buscar: ").lower()
        print(gestionar_historial(accion, historial_chat))

    # ── salir ─────────────────────────────────────────────────────────────────
    elif cmd == "salir":
        print("Agente apagado. Vuelve pronto.")
        sistema_activo = False

    # ── comando desconocido ───────────────────────────────────────────────────
    else:
        print("Comando desconocido. Intenta de nuevo.")
