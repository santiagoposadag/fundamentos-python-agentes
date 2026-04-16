from datetime import datetime
import random

# ─── Contratos de Memoria ─────────────────────────────────────────────────────
# Los type aliases viven aquí porque son parte del contrato de la clase.
# Cualquier archivo que importe PseudoAgente ya sabe qué estructura esperar.
type Recuerdo = dict[str, str]
type MemoriaAgente = list[Recuerdo]


# ─── Clase PseudoAgente ───────────────────────────────────────────────────────

# ¿Por qué self. y no una variable local?
# Una variable local dentro de una función muere cuando la función termina.
# self.tokens y self.historial_chat son atributos del OBJETO: sobreviven entre
# llamadas a métodos y están disponibles para todos los métodos de la clase.
# Es la diferencia entre escribir algo en un papel (local) vs grabarlo en la
# memoria del agente (self): uno desaparece, el otro persiste.
class PseudoAgente:
    def __init__(self, nombre: str, energia: int = 100):
        self.nombre = nombre
        self.tokens: int = energia
        self.historial_chat: MemoriaAgente = []

    @property
    def energia(self) -> int:
        """Expone tokens como energía para persistencia en DB."""
        return self.tokens

    def usar_energia(self, cantidad: int) -> bool:
        """Descuenta energía al completar una misión. Retorna True si queda energía."""
        return self._consumir(cantidad)

    # ── Métodos internos ──────────────────────────────────────────────────────

    def _registrar(self, descripcion: str) -> None:
        """Guarda una entrada en el historial con timestamp."""
        hora = datetime.now().strftime("%H:%M:%S")
        self.historial_chat.append({
            "autor": self.nombre,
            "descripcion": descripcion,
            "hora": hora,
        })

    def _consumir(self, cantidad: int) -> bool:
        """Descuenta tokens. Retorna True si el agente sigue vivo."""
        self.tokens -= cantidad
        return self.tokens > 0

    # ── Tools (métodos públicos) ───────────────────────────────────────────────

    def ping(self) -> str:
        """Verifica que el agente está activo. Costo: 2 tokens."""
        if not self._consumir(2):
            return f"[{self.nombre}] Sin energía para responder."
        self._registrar("Ejecutó comando ping")
        return "pong!"

    def contar_letras(self, frase: str) -> str:
        """Cuenta vocales y consonantes de una frase. Costo: 5 tokens."""
        if not self._consumir(5):
            return f"[{self.nombre}] Sin energía para contar letras."
        tot_vocales = 0
        tot_cons = 0
        for letra in frase:
            if letra in "aeiouáéíóú":
                tot_vocales += 1
            elif letra.isalpha():
                tot_cons += 1
        self._registrar(f"Contó letras de la frase: {frase}")
        return f"Vocales: {tot_vocales} | Consonantes: {tot_cons} | Total letras: {tot_vocales + tot_cons}"

    def fecha_hoy(self, rol: str) -> str:
        """Retorna la fecha actual. Solo para admin. Costo: 5 tokens."""
        if not self._consumir(5):
            return f"[{self.nombre}] Sin energía para consultar fecha."
        # raise viaja hacia arriba en el call stack hasta encontrar el except en main.py
        if rol != "admin":
            raise PermissionError("Privilegios insuficientes")
        fecha = datetime.now().strftime("%Y-%m-%d")
        self._registrar(f"Consultó la fecha de hoy: {fecha}")
        return f"Fecha de hoy: {fecha}"

    def validar_password(self, nueva: str, usuario: str) -> str:
        """Valida una nueva contraseña contra las reglas de seguridad. Costo: 3 tokens."""
        if not self._consumir(3):
            return f"[{self.nombre}] Sin energía para validar contraseña."
        if len(nueva) < 8:
            resultado = "[Rechazada] La contraseña debe tener al menos 8 caracteres."
        elif nueva == usuario:
            resultado = "[Rechazada] La contraseña no puede ser igual a tu nombre de usuario."
        else:
            resultado = "[OK] Contraseña válida."
        self._registrar(f"Validó contraseña: {resultado}")
        return resultado

    def calculadora(self, num1: float, operador: str, num2: float) -> str:
        """Realiza operaciones aritméticas básicas. Costo: 5 tokens."""
        if not self._consumir(5):
            return f"[{self.nombre}] Sin energía para calcular."
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
        self._registrar(f"Calculó: {num1} {operador} {num2} = {resultado}")
        return f"Resultado: {resultado}"

    def gestionar_historial(self, accion: str) -> str:
        """Administra el historial del agente. Costo: 10 tokens.

        Ya no recibe memoria como parámetro — usa self.historial_chat directamente.
        Esto es encapsulamiento: el agente gestiona su propia memoria.
        """
        if not self._consumir(10):
            return f"[{self.nombre}] Sin energía para acceder al historial."
        if accion == "all":
            if not self.historial_chat:
                return "[PseudoAgente] El historial está vacío."
            return "\n".join(
                f"[{e['hora']}] [{e['autor']}]: {e['descripcion']}"
                for e in self.historial_chat
            )
        if accion == "clear":
            self.historial_chat.clear()
            return "[PseudoAgente] Historial eliminado."
        # Búsqueda por palabra clave — "in" verifica si la palabra está contenida en la descripción
        coincidencias = [
            f"[{e['hora']}] [{e['autor']}]: {e['descripcion']}"
            for e in self.historial_chat
            if accion in e["descripcion"].lower()
        ]
        if not coincidencias:
            return "[PseudoAgente] No encontré registros que coincidan con esa palabra."
        return "\n".join(coincidencias)

    def lanzar_dado(self) -> str:
        """Lanza un dado de 6 caras usando random.randint(). Costo: 1 token."""
        if not self._consumir(1):
            return f"[{self.nombre}] Sin energía para lanzar el dado."
        resultado = random.randint(1, 6)
        self._registrar(f"Lanzó el dado: obtuvo {resultado}")
        return f"[{self.nombre}] Resultado del dado: 🎲 {resultado}"


# ─── Clase AgenteAdmin ────────────────────────────────────────────────────────

# ¿Por qué heredar en lugar de crear una clase nueva desde cero?
# Si copiamos todo el código de PseudoAgente en AgenteAdmin, cualquier cambio
# futuro habría que hacerlo en DOS lugares. Con herencia, AgenteAdmin recibe
# TODOS los métodos del padre gratis y solo sobreescribe lo que necesita cambiar.
# Es el principio DRY (Don't Repeat Yourself): un solo lugar de verdad.
class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str, energia: int = 100):
        # super().__init__() llama al constructor del padre (PseudoAgente).
        # Sin esto, self.tokens y self.historial_chat nunca se inicializarían.
        super().__init__(nombre, energia)

    def gestionar_historial(self, accion: str) -> str:
        """Override: para el admin revisar el historial NO consume tokens.

        El resto de la lógica es idéntica al padre — solo se omite _consumir().
        Esto demuestra polimorfismo: mismo método, comportamiento diferente según el tipo.
        """
        if accion == "all":
            if not self.historial_chat:
                return "[AgenteAdmin] El historial está vacío."
            return "\n".join(
                f"[{e['hora']}] [{e['autor']}]: {e['descripcion']}"
                for e in self.historial_chat
            )
        if accion == "clear":
            self.historial_chat.clear()
            return "[AgenteAdmin] Historial eliminado."
        coincidencias = [
            f"[{e['hora']}] [{e['autor']}]: {e['descripcion']}"
            for e in self.historial_chat
            if accion in e["descripcion"].lower()
        ]
        if not coincidencias:
            return "[AgenteAdmin] No encontré registros que coincidan con esa palabra."
        return "\n".join(coincidencias)


# ─── Auto-prueba ──────────────────────────────────────────────────────────────
# Este bloque solo corre si ejecutás python agente.py directamente.
# Si importás desde main.py, __name__ es "agente" y este bloque se ignora.
if __name__ == "__main__":
    agente = PseudoAgente("Test")
    print(f"Agente creado: {agente.nombre} | Tokens: {agente.tokens}")
    print(agente.ping())
    print(agente.lanzar_dado())

    admin = AgenteAdmin("AdminTest")
    print(f"\nAgenteAdmin creado: {admin.nombre}")
    print(f"¿Es instancia de PseudoAgente? {isinstance(admin, PseudoAgente)}")
