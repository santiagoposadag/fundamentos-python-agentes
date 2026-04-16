# agente.py - Contiene la clase PseudoAgente, AgenteAdmin y los alias de tipos

from datetime import datetime
from typing import Dict, List
import random

Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]  # Alias que deja claro cómo está estructurada la memoria del agente


class PseudoAgente:
    # Una variable con self. pertenece a la instancia del objeto y persiste durante toda su vida útil:
    # self.tokens y self.historial_chat son accesibles desde cualquier método de la clase en cualquier momento.
    # Una variable local (sin self.) solo existe mientras se ejecuta la función donde fue creada
    # y desaparece al terminar, sin dejar rastro en el objeto ni en ningún otro lugar del programa.
    def __init__(self, nombre: str, energia: int = 100):
        self.nombre = nombre
        self.tokens = energia  # energia inicial: 100 por defecto o el valor cargado desde la BD
        self.historial_chat: MemoriaAgente = []

    def ping(self) -> str:
        if self.tokens <= 0:
            return "[Pseudoagente] Batería agotada. El agente no puede continuar."
        self.tokens -= 2
        return "pong."

    def gestionar_historial(self, accion: str) -> str:
        if self.tokens <= 0:
            return "[Pseudoagente] Batería agotada. El agente no puede continuar."
        self.tokens -= 5
        if not self.historial_chat:
            return "[Pseudoagente] No hay registros en el historial."
        if accion == "all":
            return "\n".join(str(log) for log in self.historial_chat)
        elif accion == "clear":
            self.historial_chat.clear()
            return "Historial de comandos borrado."
        else:
            coincidencias = [log for log in self.historial_chat if accion in log["descripcion"].lower()]
            if coincidencias:
                return "\n".join(str(log) for log in coincidencias) + f"\nCoincidencias encontradas: {len(coincidencias)}"
            else:
                return "[Pseudoagente] No encontré registros que coincidan con esa palabra."

    def contar_letras(self, palabra: str) -> str:
        if self.tokens <= 0:
            return "[Pseudoagente] Batería agotada. El agente no puede continuar."
        self.tokens -= 3
        tot_letras = len(palabra)
        tot_vocales = sum(1 for p in palabra if p in "aeiou")
        tot_cons = tot_letras - tot_vocales
        return (f"Palabra ingresada: {palabra}\n"
                f"Total de letras: {tot_letras}\n"
                f"Total de vocales: {tot_vocales}\n"
                f"Total de consonantes: {tot_cons}")

    def validar_password(self, usuario: str, nueva_contrasenia: str) -> str:
        if self.tokens <= 0:
            return "[Pseudoagente] Batería agotada. El agente no puede continuar."
        self.tokens -= 3
        if len(nueva_contrasenia) < 8:
            return "Contraseña demasiado corta. Debe tener al menos 8 caracteres."
        elif nueva_contrasenia == usuario:
            return "Contraseña no puede ser igual al nombre de usuario."
        else:
            return "Contraseña válida."

    def calculadora(self, num1: float, operador: str, num2: float) -> str:
        if self.tokens <= 0:
            return "[Pseudoagente] Batería agotada. El agente no puede continuar."
        self.tokens -= 5
        if operador == "+":
            return f"Resultado: {num1 + num2}"
        elif operador == "-":
            return f"Resultado: {num1 - num2}"
        elif operador == "*":
            return f"Resultado: {num1 * num2}"
        elif operador == "/":
            if num2 == 0:
                raise ValueError("Error: no se puede dividir por cero.")  # Atrapado en main para no dañar el flujo
            return f"Resultado: {num1 / num2}"
        else:
            raise ValueError("Operador no válido.")

    def fecha_hoy(self, rol: str) -> str:
        if self.tokens <= 0:
            return "[Pseudoagente] Batería agotada. El agente no puede continuar."
        if rol != "admin":
            raise PermissionError("Privilegios insuficientes")  # Se verifica el permiso antes de consumir tokens
        self.tokens -= 4
        return f"Fecha y hora actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def lanzar_dado(self) -> str:
        if self.tokens <= 0:
            return "[Pseudoagente] Batería agotada. El agente no puede continuar."
        self.tokens -= 1
        numero = random.randint(1, 6)
        return f"El dado cayó en: {numero}"

    def usar_energia(self, cantidad: int) -> str:
        """Descuenta energia_requerida de los tokens del agente. La clase controla la lógica."""
        if self.tokens < cantidad:
            raise ValueError(
                f"[{self.nombre}] Energía insuficiente: tiene {self.tokens}, necesita {cantidad}."
            )
        self.tokens -= cantidad
        return (
            f"[{self.nombre}] Misión ejecutada. Energía consumida: {cantidad}. "
            f"Energía restante: {self.tokens}."
        )

    def registrar_log(self, cmd: list, mensaje: str, rol: str):
        d_log = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": str(cmd),
            "rol": rol,
            "descripcion": mensaje
        }
        self.historial_chat.append(d_log)


# Crear AgenteAdmin como clase hija de PseudoAgente es mejor que copiar y pegar el código porque
# reutilizamos toda la lógica ya probada sin duplicarla: si PseudoAgente evoluciona (nuevos métodos,
# correcciones), AgenteAdmin hereda esas mejoras de forma automática y solo redefinimos lo que
# realmente necesita ser diferente, manteniendo el código limpio y fácil de mantener.
class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str, energia: int = 100):
        super().__init__(nombre, energia)

    def gestionar_historial(self, accion: str) -> str:
        # El administrador puede consultar el historial sin consumir batería como privilegio de su rol
        if not self.historial_chat:
            return "[Pseudoagente] No hay registros en el historial."
        if accion == "all":
            return "\n".join(str(log) for log in self.historial_chat)
        elif accion == "clear":
            self.historial_chat.clear()
            return "Historial de comandos borrado."
        else:
            coincidencias = [log for log in self.historial_chat if accion in log["descripcion"].lower()]
            if coincidencias:
                return "\n".join(str(log) for log in coincidencias) + f"\nCoincidencias encontradas: {len(coincidencias)}"
            else:
                return "[Pseudoagente] No encontré registros que coincidan con esa palabra."
