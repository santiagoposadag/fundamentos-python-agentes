# Módulo del PseudoAgente - Semana 4
# Contiene la clase PseudoAgente, AgenteAdmin y los Type Aliases.

from datetime import datetime
import random
from typing import Dict, List

# Type Aliases: nombrar los tipos hace el código más legible y deja claro
# qué estructura de datos espera cada función.
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


class PseudoAgente:
    # __init__ es el constructor: se ejecuta cada vez que creamos un PseudoAgente().
    # self. diferencia una variable de instancia (vive con el objeto mientras exista)
    # de una variable local (desaparece cuando la función termina).
    def __init__(self, nombre: str = "Athena"):
        self.nombre = nombre
        self.tokens: int = 100
        self.historial_chat: MemoriaAgente = []

    def registrar_log(self, cmd: str, rol: str, mensaje: str) -> None:
        d_log: Recuerdo = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": cmd,
            "rol": rol,
            "descripcion": mensaje
        }
        self.historial_chat.append(d_log)

    def comando_ping(self) -> str:
        """Responde con 'pong!' al comando ping."""
        self.tokens -= 2
        print("pong!")
        return "Se ha enviado un ping y de respuesta se devolvió un pong."

    def contar_letras(self) -> str:
        """Cuenta vocales y consonantes de una frase ingresada por el usuario."""
        self.tokens -= 5
        frase = input("Ingresa una frase: ").lower()
        vocales = 'aeiou'
        cont_v = 0
        cont_c = 0
        for ch in frase:
            if ch.isalpha():
                if ch in vocales:
                    cont_v += 1
                else:
                    cont_c += 1
        print(f"Vocales: {cont_v} | Consonantes: {cont_c}")
        return f"Se solicitó el conteo de la frase. Vocales: {cont_v}, Consonantes: {cont_c}"

    def comando_fecha_hoy(self, role: str) -> str:
        """Muestra la fecha y hora actual. Solo para administradores."""
        self.tokens -= 5
        # raise lanza el error hacia arriba; el try/except del bucle principal lo atrapa (similar a un 403)
        if role != "admin":
            raise PermissionError("Privilegios insuficientes")
        hoy = datetime.now()
        print("Fecha y hora actual:", hoy.strftime('%Y-%m-%d %H:%M:%S'))
        return f"[PseudoAgente] La fecha y hora actual es: {hoy.strftime('%Y-%m-%d %H:%M:%S')}"

    def validar_password(self, logged_username: str) -> str:
        """Valida una nueva contraseña propuesta según reglas de seguridad."""
        self.tokens -= 5
        propuesta = input("Ingresa la nueva contraseña propuesta: ")
        if len(propuesta) < 8:
            print("[Rechazada] La contraseña debe tener al menos 8 caracteres.")
            return "[Rechazada] La contraseña debe tener al menos 8 caracteres."
        if propuesta == logged_username:
            print("[Rechazada] La contraseña no puede ser igual al nombre de usuario.")
            return "[Rechazada] La contraseña no puede ser igual al nombre de usuario."
        print("[OK] Contraseña válida (según las reglas del ejercicio).")
        return "[OK] Contraseña válida."

    def calculadora(self) -> str:
        """Realiza operaciones aritméticas básicas (+, -, *, /)."""
        self.tokens -= 10
        while True:
            a_str = input("Ingresa el primer número: ").strip()
            try:
                a = float(a_str)
                break
            except ValueError:
                print("Entrada inválida. Debes ingresar un número. Intenta de nuevo.")

        valid_ops = ['+', '-', '*', '/']
        while True:
            op = input("Ingresa el operador (+, -, *, /): ").strip()
            if op in valid_ops:
                break
            print("Operador no válido. Ingresa uno de: +, -, *, /. Intenta nuevamente.")

        # Evitar división por cero antes de aceptar el segundo número
        while True:
            b_str = input("Ingresa el segundo número: ").strip()
            try:
                b = float(b_str)
                if op == '/' and b == 0:
                    print("Operación no válida: división por cero. Ingresa otro número.")
                    continue
                break
            except ValueError:
                print("Entrada inválida. Debes ingresar un número. Intenta de nuevo.")

        if op == "+":
            res = a + b
        elif op == "-":
            res = a - b
        elif op == "*":
            res = a * b
        elif op == "/":
            res = a / b

        if isinstance(res, float) and res.is_integer():
            print("Resultado:", int(res))
            return f"Se ejecutó la calculadora. Resultado: {int(res)}"
        else:
            print("Resultado:", res)
            return f"Se ejecutó la calculadora. Resultado: {res}"

    def gestionar_historial(self, accion: str, keyword: str = "") -> str:
        """Gestiona el historial: mostrar todo, limpiar o buscar. No imprime, solo retorna."""
        self.tokens -= 5
        if accion == "all":
            if not self.historial_chat:
                return "[PseudoAgente] No hay registros en el historial."
            resultado = "[PseudoAgente] Mostrando todo el historial:\n"
            for i, e in enumerate(self.historial_chat, start=1):
                resultado += f"{i}. [{e.get('timestamp')}] {e.get('rol')}: {e.get('descripcion')}\n"
            return resultado.strip()

        elif accion == "clear":
            self.historial_chat.clear()
            return "[PseudoAgente] Historial eliminado."

        elif accion == "search":
            found = []
            for entry in self.historial_chat:
                if keyword.lower() in entry.get("descripcion", "").lower():
                    found.append(entry)
            if not found:
                return "[PseudoAgente] No encontré registros que coincidan con esa palabra."
            resultado = f"[PseudoAgente] Total de coincidencias: {len(found)}\n"
            for i, elem in enumerate(found, start=1):
                resultado += f"{i} >>> [{elem.get('timestamp')}] {elem.get('rol')}: {elem.get('descripcion')}\n"
            return resultado.strip()

        return "[PseudoAgente] Acción no reconocida."

    def lanzar_dado(self) -> str:
        """Lanza un dado de 6 caras usando random.randint()."""
        self.tokens -= 2
        resultado = random.randint(1, 6)
        return f"[{self.nombre}] Resultado del dado: {resultado}"


# Herencia: AgenteAdmin hereda de PseudoAgente.
# Es mejor que copiar todo el código porque si se corrige un bug en PseudoAgente,
# AgenteAdmin lo hereda automáticamente. Solo sobreescribimos lo que necesita cambiar.
class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str = "Athena"):
        # super() llama al constructor del padre para no repetir la inicialización
        super().__init__(nombre)

    # Override: el admin gestiona el historial sin consumir tokens
    def gestionar_historial(self, accion: str, keyword: str = "") -> str:
        """Igual que el padre pero sin descuento de tokens."""
        if accion == "all":
            if not self.historial_chat:
                return "[PseudoAgente] No hay registros en el historial."
            resultado = "[PseudoAgente] Mostrando todo el historial:\n"
            for i, e in enumerate(self.historial_chat, start=1):
                resultado += f"{i}. [{e.get('timestamp')}] {e.get('rol')}: {e.get('descripcion')}\n"
            return resultado.strip()

        elif accion == "clear":
            self.historial_chat.clear()
            return "[PseudoAgente] Historial eliminado."

        elif accion == "search":
            found = []
            for entry in self.historial_chat:
                if keyword.lower() in entry.get("descripcion", "").lower():
                    found.append(entry)
            if not found:
                return "[PseudoAgente] No encontré registros que coincidan con esa palabra."
            resultado = f"[PseudoAgente] Total de coincidencias: {len(found)}\n"
            for i, elem in enumerate(found, start=1):
                resultado += f"{i} >>> [{elem.get('timestamp')}] {elem.get('rol')}: {elem.get('descripcion')}\n"
            return resultado.strip()

        return "[PseudoAgente] Acción no reconocida."
