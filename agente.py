# Modulo del PseudoAgente - Semana 4
# Contiene la clase PseudoAgente, AgenteAdmin y los Type Aliases.

from datetime import datetime
import random
from typing import Dict, List

# Type Aliases para que quede claro que estructura maneja cada funcion
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


class PseudoAgente:
    # __init__ es el constructor: corre cada vez que hacemos PseudoAgente()
    # self. hace que la variable viva con el objeto (no desaparece al salir de la funcion)
    # Agregamos energia como parametro para poder reconstruir el agente desde la DB
    # con su energia real. Por defecto es 100 para no romper el codigo anterior.
    def __init__(self, nombre: str = "Athena", energia: int = 100):
        self.nombre = nombre
        self.tokens: int = energia  # tokens y energia son el mismo concepto
        self.historial_chat: MemoriaAgente = []

    def descontar_energia(self, cantidad: int) -> str:
        """Descuenta energia al agente. Retorna un mensaje de resultado."""
        # Verificamos antes de descontar para que no quede con energia negativa
        if self.tokens < cantidad:
            return f"[Error] Energia insuficiente. Disponible: {self.tokens}, requerida: {cantidad}"
        self.tokens -= cantidad
        return f"[OK] Energia descontada. Energia restante: {self.tokens}"

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
        return "Se ha enviado un ping y de respuesta se devolvio un pong."

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
        return f"Se solicito el conteo de la frase. Vocales: {cont_v}, Consonantes: {cont_c}"

    def comando_fecha_hoy(self, role: str) -> str:
        """Muestra la fecha y hora actual. Solo para administradores."""
        self.tokens -= 5
        # raise lanza el error; el try/except del bucle principal lo atrapa (similar a un 403)
        if role != "admin":
            raise PermissionError("Privilegios insuficientes")
        hoy = datetime.now()
        print("Fecha y hora actual:", hoy.strftime('%Y-%m-%d %H:%M:%S'))
        return f"[PseudoAgente] La fecha y hora actual es: {hoy.strftime('%Y-%m-%d %H:%M:%S')}"

    def validar_password(self, logged_username: str) -> str:
        """Valida una nueva contrasena propuesta segun reglas de seguridad."""
        self.tokens -= 5
        propuesta = input("Ingresa la nueva contrasena propuesta: ")
        if len(propuesta) < 8:
            print("[Rechazada] La contrasena debe tener al menos 8 caracteres.")
            return "[Rechazada] La contrasena debe tener al menos 8 caracteres."
        if propuesta == logged_username:
            print("[Rechazada] La contrasena no puede ser igual al nombre de usuario.")
            return "[Rechazada] La contrasena no puede ser igual al nombre de usuario."
        print("[OK] Contrasena valida (segun las reglas del ejercicio).")
        return "[OK] Contrasena valida."

    def calculadora(self) -> str:
        """Realiza operaciones aritmeticas basicas (+, -, *, /)."""
        self.tokens -= 10
        while True:
            a_str = input("Ingresa el primer numero: ").strip()
            try:
                a = float(a_str)
                break
            except ValueError:
                print("Entrada invalida. Debes ingresar un numero. Intenta de nuevo.")

        valid_ops = ['+', '-', '*', '/']
        while True:
            op = input("Ingresa el operador (+, -, *, /): ").strip()
            if op in valid_ops:
                break
            print("Operador no valido. Ingresa uno de: +, -, *, /. Intenta nuevamente.")

        # Evitamos division por cero antes de aceptar el segundo numero
        while True:
            b_str = input("Ingresa el segundo numero: ").strip()
            try:
                b = float(b_str)
                if op == '/' and b == 0:
                    print("Operacion no valida: division por cero. Ingresa otro numero.")
                    continue
                break
            except ValueError:
                print("Entrada invalida. Debes ingresar un numero. Intenta de nuevo.")

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
            return f"Se ejecuto la calculadora. Resultado: {int(res)}"
        else:
            print("Resultado:", res)
            return f"Se ejecuto la calculadora. Resultado: {res}"

    def gestionar_historial(self, accion: str, keyword: str = "") -> str:
        """Gestiona el historial: mostrar todo, limpiar o buscar."""
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
                return "[PseudoAgente] No encontre registros que coincidan con esa palabra."
            resultado = f"[PseudoAgente] Total de coincidencias: {len(found)}\n"
            for i, elem in enumerate(found, start=1):
                resultado += f"{i} >>> [{elem.get('timestamp')}] {elem.get('rol')}: {elem.get('descripcion')}\n"
            return resultado.strip()

        return "[PseudoAgente] Accion no reconocida."

    def lanzar_dado(self) -> str:
        """Lanza un dado de 6 caras usando random.randint()."""
        self.tokens -= 2
        resultado = random.randint(1, 6)
        return f"[{self.nombre}] Resultado del dado: {resultado}"


# AgenteAdmin hereda de PseudoAgente.
# Solo sobreescribimos lo que necesita cambiar: gestionar_historial sin consumir tokens.
class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str = "Athena", energia: int = 100):
        # super() llama al constructor del padre para no repetir codigo
        super().__init__(nombre, energia)

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
                return "[PseudoAgente] No encontre registros que coincidan con esa palabra."
            resultado = f"[PseudoAgente] Total de coincidencias: {len(found)}\n"
            for i, elem in enumerate(found, start=1):
                resultado += f"{i} >>> [{elem.get('timestamp')}] {elem.get('rol')}: {elem.get('descripcion')}\n"
            return resultado.strip()

        return "[PseudoAgente] Accion no reconocida."
