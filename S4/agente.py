# Importa el módulo datetime para trabajar con fechas y horas
import datetime

# Importa el módulo random para generar números aleatorios
import random

# Importa List y Dict para anotaciones de tipo
from typing import List, Dict


# Alias de tipos para la memoria del agente
# Historial representa un registro individual de comando
Historial = Dict[str, str]
# MemoriaAgente es una lista de registros de historial
MemoriaAgente = List[Historial]


# Comentario de auditoría sobre herencia:
# Heredar permite reutilizar y especializar el comportamiento sin duplicar código.
# Si hay un cambio en la lógica base, todas las clases hijas lo heredan automáticamente.


# Comentario de auditoría sobre self:
# Las variables con self. son atributos del objeto y persisten entre métodos.
# Las variables locales solo existen dentro de la función.


class PseudoAgente:
    """
    Clase que representa un agente con historial, tokens y comandos básicos.
    Encapsula la memoria y las operaciones del agente.
    """

    def __init__(self, nombre: str):
        """
        Constructor de la clase. Inicializa el nombre, los tokens y el historial interno.
        """
        # Nombre del agente
        self.nombre = nombre
        # Tokens disponibles para ejecutar comandos
        self.tokens = 100
        # Historial de comandos ejecutados (memoria del agente)
        self.historial_chat: MemoriaAgente = []

    def registrar_log(self, comando: str, rol: str, descripcion: str) -> None:
        """
        Agrega un registro al historial de comandos del agente.
        """
        # Crea un diccionario con la información del comando ejecutado
        d_log: Historial = {
            "timestamp": datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # Fecha y hora actual
            "cmd": comando,  # Comando ejecutado
            "rol": rol,  # Rol del usuario
            "descripcion": descripcion,  # Descripción del resultado
        }
        # Agrega el registro al historial
        self.historial_chat.append(d_log)

    def gestionar_historial(self, accion: str) -> str:
        """
        Gestiona la memoria del agente: muestra todo, limpia o busca coincidencias.
        Descuenta tokens por uso. Si los tokens llegan a 0 o menos, el agente se apaga.
        """
        # Descuenta tokens por usar el historial
        self.tokens -= 50
        # Si no hay energía, retorna mensaje de apagado
        if self.tokens <= 0:
            return "[Agente] Sin energía para operar."
        # Divide la acción en partes para analizar el comando
        partes = accion.split()
        # Si la acción es 'historial all', muestra todo el historial
        if len(partes) == 2 and partes[1] == "all":
            if len(self.historial_chat) == 0:
                return "[PseudoAgente] No hay historial para mostrar."
            else:
                # Formatea cada registro del historial
                resultado = [
                    f"{i + 1}. [{d['timestamp']}] ({d['rol']}) {d['cmd']}: {d['descripcion']}"
                    for i, d in enumerate(self.historial_chat)
                ]
                return "[PseudoAgente] Historial completo:\n" + "\n".join(resultado)
        # Si la acción es 'historial clear', borra el historial
        elif len(partes) == 2 and partes[1] == "clear":
            self.historial_chat.clear()
            return "[PseudoAgente] Historial borrado correctamente."
        # Si solo es 'historial', busca una palabra clave
        elif len(partes) == 1:
            if len(self.historial_chat) == 0:
                return "[PseudoAgente] No hay historial para buscar."
            else:
                # Solicita la palabra clave al usuario
                palabra = input("Ingresa la palabra clave a buscar: ").lower()
                # Busca coincidencias en las descripciones
                encontrados = [
                    f"[{d['timestamp']}] ({d['rol']}) {d['cmd']}: {d['descripcion']}"
                    for d in self.historial_chat
                    if palabra in d["descripcion"].lower()
                ]
                if len(encontrados) == 0:
                    return "[PseudoAgente] No encontré registros que coincidan con esa palabra."
                else:
                    return (
                        f"[PseudoAgente] Se encontraron {len(encontrados)} coincidencia(s):\n"
                        + "\n".join(encontrados)
                    )
        # Opción no reconocida
        else:
            return "[PseudoAgente] Opción de historial no reconocida. Usa 'historial', 'historial all' o 'historial clear'."

    def contar_letras(self) -> str:
        """
        Solicita una palabra y cuenta letras, vocales y consonantes usando list comprehensions.
        Descuenta tokens por uso. Si los tokens llegan a 0 o menos, el agente se apaga.
        """
        # Descuenta tokens por usar el comando
        self.tokens -= 20
        if self.tokens <= 0:
            return "[Agente] Sin energía para operar."
        # Solicita la palabra al usuario
        palabra = input("Ingresa una palabra: ").lower()
        # Cuenta vocales usando list comprehension
        vocales = [letra for letra in palabra if letra in "aeiou"]
        # Cuenta consonantes usando list comprehension
        consonantes = [letra for letra in palabra if letra not in "aeiou"]
        tot_vocales = len(vocales)
        tot_cons = len(consonantes)
        tot_letras = len(palabra)
        # Muestra los resultados
        print(f"Palabra ingresada: {palabra}")
        print(f"Total de letras: {tot_letras}")
        print(f"Total de vocales: {tot_vocales}")
        print(f"Total de consonantes: {tot_cons}")
        return f"Se solicitó el conteo de la palabra {palabra}, dando como resultados:\nVocales: {tot_vocales}\nConsonantes: {tot_cons}\nTotal: {tot_letras}"

    def fecha_hoy(self, rol_usuario: str) -> str:
        """
        Muestra la fecha y hora actual solo si el usuario es admin.
        Descuenta tokens por uso. Si los tokens llegan a 0 o menos, el agente se apaga.
        Si el usuario no es admin, lanza una excepción PermissionError.
        """
        # Descuenta tokens por usar el comando
        self.tokens -= 20
        if self.tokens <= 0:
            return "[Agente] Sin energía para operar."
        # Verifica si el usuario es admin
        if rol_usuario != "admin":
            raise PermissionError("Privilegios insuficientes")
        # Retorna la fecha y hora actual
        mensaje_fecha = f"Se ha consultado la fecha actual: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return mensaje_fecha

    def validar_pass(self, nombre_usuario: str) -> str:
        """
        Valida una nueva contraseña propuesta por el usuario.
        Descuenta tokens por uso. Si los tokens llegan a 0 o menos, el agente se apaga.
        """
        # Descuenta tokens por usar el comando
        self.tokens -= 20
        if self.tokens <= 0:
            return "[Agente] Sin energía para operar."
        # Solicita la nueva contraseña
        nueva = input("Propuesta de nueva contraseña: ")
        # No puede ser igual al usuario
        if nueva == nombre_usuario:
            print("La contraseña no puede ser igual al nombre de usuario.")
            return f"Intento fallido: la contraseña es igual al nombre de usuario. [Tokens restantes: {self.tokens}]"
        elif len(nueva) < 8:
            print("La contraseña debe tener al menos 8 caracteres.")
            return f"Intento fallido: la contraseña tiene menos de 8 caracteres. [Tokens restantes: {self.tokens}]"
        else:
            print("Contraseña válida.")
            return f"Contraseña propuesta válida. [Tokens restantes: {self.tokens}]"

    def calculadora(self) -> str:
        """
        Realiza operaciones matemáticas básicas entre dos números. Lanza ValueError si el input no es válido.
        Descuenta tokens por uso. Si los tokens llegan a 0 o menos, el agente se apaga.
        """
        # Descuenta tokens por usar el comando
        self.tokens -= 30
        if self.tokens <= 0:
            return "[Agente] Sin energía para operar."
        # Solicita los números y el operador
        n1 = input("Ingresa el primer número: ")
        op = input("Ingresa el operador (+, -, *, /): ")
        n2 = input("Ingresa el segundo número: ")
        try:
            # Intenta convertir los inputs a float
            n1 = float(n1)
            n2 = float(n2)
        except ValueError as exc:
            # Si falla la conversión, relanza el error personalizado
            raise ValueError("Debes ingresar números válidos.") from exc
        # Realiza la operación según el operador
        if op == "+":
            resultado = n1 + n2
            return f"Se realizó una suma: {n1} + {n2} = {resultado}"
        elif op == "-":
            resultado = n1 - n2
            return f"Se realizó una resta: {n1} - {n2} = {resultado}"
        elif op == "*":
            resultado = n1 * n2
            return f"Se realizó una multiplicación: {n1} * {n2} = {resultado}"
        elif op == "/":
            # Verifica división por cero
            if n2 == 0:
                raise ValueError("No se puede dividir por cero.")
            resultado = n1 / n2
            return f"Se realizó una división: {n1} / {n2} = {resultado}"
        else:
            # Operador no válido
            raise ValueError("Operador no válido en la calculadora.")

    def lanzar_dado(self) -> str:
        """
        Lanza un dado y devuelve un número aleatorio entre 1 y 6.
        Descuenta tokens por uso. Si los tokens llegan a 0 o menos, el agente se apaga.
        """
        # Descuenta tokens por usar el comando
        self.tokens -= 10
        if self.tokens <= 0:
            return "[Agente] Sin energía para operar."
        # Genera un número aleatorio entre 1 y 6
        resultado = random.randint(1, 6)
        return f"El dado cayó en: {resultado}\n[Tokens restantes: {self.tokens}]"


class AgenteAdmin(PseudoAgente):
    """
    Clase hija de PseudoAgente que representa un agente administrador.
    No descuenta tokens al consultar el historial.
    """

    def gestionar_historial(self, accion: str) -> str:
        """
        Gestiona la memoria del agente: muestra todo, limpia o busca coincidencias.
        Para el AgenteAdmin, NO se descuentan tokens por este método.
        """
        partes = accion.split()
        if len(partes) == 2 and partes[1] == "all":
            if len(self.historial_chat) == 0:
                return "[PseudoAgente] No hay historial para mostrar."
            else:
                resultado = [
                    f"{i + 1}. [{d['timestamp']}] ({d['rol']}) {d['cmd']}: {d['descripcion']}"
                    for i, d in enumerate(self.historial_chat)
                ]
                return "[PseudoAgente] Historial completo:\n" + "\n".join(resultado)
        elif len(partes) == 2 and partes[1] == "clear":
            self.historial_chat.clear()
            return "[PseudoAgente] Historial borrado correctamente."
        elif len(partes) == 1:
            if len(self.historial_chat) == 0:
                return "[PseudoAgente] No hay historial para buscar."
            else:
                palabra = input("Ingresa la palabra clave a buscar: ").lower()
                encontrados = [
                    f"[{d['timestamp']}] ({d['rol']}) {d['cmd']}: {d['descripcion']}"
                    for d in self.historial_chat
                    if palabra in d["descripcion"].lower()
                ]
                if len(encontrados) == 0:
                    return "[PseudoAgente] No encontré registros que coincidan con esa palabra."
                else:
                    return (
                        f"[PseudoAgente] Se encontraron {len(encontrados)} coincidencia(s):\n"
                        + "\n".join(encontrados)
                    )
        else:
            return "[PseudoAgente] Opción de historial no reconocida. Usa 'historial', 'historial all' o 'historial clear'."
