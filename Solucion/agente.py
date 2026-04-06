from datetime import datetime
from typing import Dict, List
import random

# Los alias de tipo permiten que el código sea más legible y mantenible, ya que explícitamente
# definimos la estructura de la memoria del agente. Para que así entiendan rápidamente qué forma tiene cada dato sin analizar toda la lógica.
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


class PseudoAgente:
# Una variable local solo existe mientras la función se ejecuta y desaparece al terminar.
# Una variable con self pertenece al objeto y persiste mientras el objeto exista.

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tokens: int = 100
        self.historial_chat: MemoriaAgente = []

    def registrar_log(self, autor: str, descripcion: str):
        self.historial_chat.append({"autor": autor, "descripcion": descripcion})

    def contar_letras(self, palabra: str) -> str:
        self.tokens -= 5
        tot_letras = len(palabra)
        tot_vocales = 0
        tot_cons = 0

        for letra in palabra:
            if letra in "aeiou":
                tot_vocales += 1
            else:
                tot_cons += 1

        return (
            f"Palabra ingresada: {palabra}\n"
            f"Total de vocales: {tot_vocales}\n"
            f"Total de consonantes: {tot_cons}\n"
            f"Total de letras: {tot_letras}"
        )

    def obtener_fecha_actual(self, rol_usuario_func: str) -> str:
        self.tokens -= 3
        if rol_usuario_func == "invitado":
            # Se lanza el error con raise y Python detiene la ejecución. El error viaja hasta el bloque try/except en el menú principal donde se atrapa
            # con except PermissionError para mostrar un mensaje bonito sin que el programa se rompa.
            raise PermissionError("Privilegios insuficientes")
        return datetime.now().strftime("%Y-%m-%d")

    def validar_password(self, nueva_pass: str, rol_usuario_func: str) -> bool:
        self.tokens -= 3
        return not (len(nueva_pass) < 8 or nueva_pass == rol_usuario_func)

    def calculadora(self, num1_func: float, num2_func: float, operacion_func: str) -> float:
        self.tokens -= 5
        if operacion_func == "+":
            return num1_func + num2_func
        if operacion_func == "-":
            return num1_func - num2_func
        if operacion_func == "*":
            return num1_func * num2_func
        if operacion_func == "/":
            if num2_func == 0:
                raise ValueError("No se puede dividir por cero.")
            return num1_func / num2_func
        raise ValueError("Operación no válida.")

    def gestionar_historial(self, accion: str) -> str:
        self.tokens -= 10
        if accion == "all":
            if not self.historial_chat:
                return "[PseudoAgente] La memoria está vacía."

            lineas: List[str] = []
            for recuerdo in self.historial_chat:
                lineas.append(f"Autor: {recuerdo['autor']} | Acción: {recuerdo['descripcion']}")
            return "\n".join(lineas)

        if accion == "clear":
            self.historial_chat.clear()
            return "[PseudoAgente] Memoria borrada con éxito."

        coincidencias: List[str] = []
        for recuerdo in self.historial_chat:
            descripcion_min = recuerdo["descripcion"].lower()
            if accion in descripcion_min:
                coincidencias.append(
                    f"-> Encontrado: [Autor: {recuerdo['autor']}] Mensaje: {recuerdo['descripcion']}"
                )

        if not coincidencias:
            return "[PseudoAgente] No encontré registros que coincidan con esa palabra."

        coincidencias.append(f"[PseudoAgente] Se encontraron {len(coincidencias)} coincidencias.")
        return "\n".join(coincidencias)

    def lanzar_dado(self) -> str:
        self.tokens -= 1
        resultado = random.randint(1, 6)
        return f"[{self.nombre}] Resultado del dado: {resultado}"

#Con herencia AgenteAdmin hereda de PseudoAgente, por lo que tiene acceso a todos sus métodos y atributos 
# pero si se copiara y pegara todo el código en una clase nueva se estaría repitiendo código y además cualquier 
#cambio que se haga en una clase debería aplicarse de forma manual en otra clase.
class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str):
        super().__init__(nombre)

    def gestionar_historial(self, accion: str) -> str:
        if accion == "all":
            if not self.historial_chat:
                return "[PseudoAgente] La memoria está vacía."

            lineas: List[str] = []
            for recuerdo in self.historial_chat:
                lineas.append(f"Autor: {recuerdo['autor']} | Acción: {recuerdo['descripcion']}")
            return "\n".join(lineas)

        if accion == "clear":
            self.historial_chat.clear()
            return "[PseudoAgente] Memoria borrada con éxito."

        coincidencias: List[str] = []
        for recuerdo in self.historial_chat:
            descripcion_min = recuerdo["descripcion"].lower()
            if accion in descripcion_min:
                coincidencias.append(
                    f"-> Encontrado: [Autor: {recuerdo['autor']}] Mensaje: {recuerdo['descripcion']}"
                )

        if not coincidencias:
            return "[PseudoAgente] No encontré registros que coincidan con esa palabra."

        coincidencias.append(f"[PseudoAgente] Se encontraron {len(coincidencias)} coincidencias.")
        return "\n".join(coincidencias)
