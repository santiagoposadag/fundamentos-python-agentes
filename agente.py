import datetime
from typing import Dict, List
import random

# Aquí le damos un nombre más claro a estructuras de datos.
# En vez de escribir siempre List[Dict[str, str]], usamos MemoriaAgente.
# Esto hace que el código sea más fácil de leer y entender.
# Además, si en el futuro cambia la estructura de la memoria,
# solo debemos modificar el alias y no todo el programa.
type Historial = Dict[str, str]
type MemoriaAgente = List[Historial]

class PseudoAgente:
    def __init__(self, nombre: str):
        """Inicializa un nuevo agente con nombre, historial vacío y 100 tokens de batería."""
        # Las variables con 'self.' son atributos de instancia, accesibles desde cualquier método de la clase durante su vida útil.
        # Una variable temporal (sin self.) solo existe dentro de esta función y se pierde cuando la función termina.
        self.nombre = nombre
        self.historial_chat: MemoriaAgente = []
        self.tokens = 100
        
    def gestionar_historial(self, op: str, rol: str) -> str:
        """Gestiona el historial del agente: muestra todo (all), limpia (clear) o busca por palabra clave. Consume 3-10 tokens."""
        self._verificar_vitalidad()
        resultado = ""
        if op == "all":
            if self.tokens < 5:
                raise ValueError(f"Tokens insuficientes. Requiere 5 tokens, tienes {self.tokens}.")
            self.tokens -= 5
            if not self.historial_chat:
                mensaje_descripcion = "[PseudoAgente] El historial está vacío."
                self.agregar_log("historial all", rol, mensaje_descripcion)
                return mensaje_descripcion
            for i, recuerdo in enumerate(self.historial_chat):
                resultado += (
                    f"\nIteración: {i}\n"
                    f"Fecha: {recuerdo['timestamp']}\n"
                    f"Comando: {recuerdo['cmd']}\n"
                    f"Autor: {recuerdo['rol']}\n"
                    f"Mensaje: {recuerdo['descripción']}\n"
                )
            mensaje_descripcion = "Se mostró todo el historial."
            self.agregar_log("historial all", rol, mensaje_descripcion)
            return resultado
        elif op == "clear":
            if self.tokens < 10:
                raise ValueError(f"Tokens insuficientes. Requiere 10 tokens, tienes {self.tokens}.")
            self.tokens -= 10
            self.historial_chat.clear()
            mensaje_descripcion = "[PseudoAgente] El historial ha sido limpiado."
            self.agregar_log("historial clear", rol, mensaje_descripcion)
            return mensaje_descripcion
        else:
            if self.tokens < 3:
                raise ValueError(f"Tokens insuficientes. Requiere 3 tokens, tienes {self.tokens}.")
            self.tokens -= 3
            contador = 0
            for i, recuerdo in enumerate(self.historial_chat):
                if op in recuerdo["descripción"].lower():
                    contador += 1
                    resultado += (
                        f"\nIteración: {i}\n"
                        f"Autor: {recuerdo['rol']}\n"
                        f"Mensaje: {recuerdo['descripción']}\n"
                    )
            if contador == 0:
                mensaje_descripcion = "[PseudoAgente] No encontré registros que coincidan con esa palabra."
                self.agregar_log("historial " + op, rol, mensaje_descripcion)
                return mensaje_descripcion
            mensaje_descripcion = f"La palabra clave es: {op} y hay {contador} coincidencias."
            self.agregar_log("historial " + op, rol, mensaje_descripcion)
            return (
                    f"La palabra clave es: {op} "
                    f"y hay {contador} coincidencias.\n"
                    + resultado
            )
    
    def agregar_log(self, cmd: str, rol: str, descripcion: str):
        """Registra un evento en el historial con timestamp, comando, rol y descripción."""
        d_log = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": cmd,
            "rol": rol,
            "descripción": descripcion
        }
        self.historial_chat.append(d_log)
    
    def contar(self, pal: str, rol: str) -> str:
        """Analiza una palabra y cuenta vocales, consonantes y letras totales. Consume 2 tokens."""
        self._verificar_vitalidad()
        if self.tokens < 2:
            raise ValueError(f"Tokens insuficientes. Requiere 2 tokens, tienes {self.tokens}.")
        self.tokens -= 2
        tot_letras = len(pal)
        tot_vocales = 0
        tot_cons = 0
        for p in pal:
            if p.lower() in "aeiou":
                tot_vocales += 1
            else:
                tot_cons += 1
        resultado = f"Palabra ingresada: {pal}\n Total de vocales: {tot_vocales}\n Total de consonantes: {tot_cons}\n Total de letras: {tot_letras}"
        mensaje_descripcion = f"Se solicitó el conteo de la palabra {pal}"
        self.agregar_log("contar", rol, mensaje_descripcion)
        return resultado
    
    def validar_contrasena(self, nueva_contra: str, rol: str, user_invitado: str = "invitado", user_admin: str = "admin") -> str:
        """Valida que una contraseña tenga más de 8 caracteres y no sea igual a un nombre de usuario. Consume 3 tokens."""
        self._verificar_vitalidad()
        if self.tokens < 3:
            raise ValueError(f"Tokens insuficientes. Requiere 3 tokens, tienes {self.tokens}.")
        self.tokens -= 3
        if len(nueva_contra) > 8 and nueva_contra != user_invitado and nueva_contra != user_admin:
            resultado = "Propuesta de nueva contraseña aceptada"
        else:
            resultado = "La contraseña debe tener mas de 8 caracteres y no debe ser igual al nombre de usuario"
        
        mensaje_descripcion = f"Se ha solicitado validar la contraseña"
        self.agregar_log("validar_pass", rol, mensaje_descripcion)
        return resultado
    
    def calcular(self, num_uno: float, num_dos: float, oper: str, rol: str) -> float:
        """Realiza operaciones matemáticas básicas (suma, resta, multiplicación, división). Consume 4 tokens."""
        try:
            self._verificar_vitalidad()
            if self.tokens < 4:
                raise ValueError(f"Tokens insuficientes. Requiere 4 tokens, tienes {self.tokens}.")
            self.tokens -= 4
            if oper == "suma":
                resultado = num_uno + num_dos
            elif oper == "resta":
                resultado = num_uno - num_dos
            elif oper == "multiplicacion":
                resultado = num_uno * num_dos
            elif oper == "division":
                if num_dos == 0:
                    raise ValueError("No se permite la división entre cero.")
                resultado = round(num_uno / num_dos, 2)
            else:
                raise ValueError("Operador no válido. Use 'suma', 'resta', 'multiplicacion' o 'division'.")
            
            mensaje_descripcion = f"Se ha solicitado realizar la operación {oper} entre el número {num_uno} y {num_dos}. Resultado: {resultado}"
            self.agregar_log("calculadora", rol, mensaje_descripcion)
            return resultado
        except ValueError as e:
            mensaje_descripcion = str(e)
            self.agregar_log("calculadora", rol, mensaje_descripcion)
            raise

    def fecha_hoy_rol(self, rol_sesion: str) -> str:
        """Devuelve la fecha y hora actual. Solo accesible para rol Administrador. Consume 2 tokens."""
        try:
            self._verificar_vitalidad()
            if self.tokens < 2:
                raise ValueError(f"Tokens insuficientes. Requiere 2 tokens, tienes {self.tokens}.")
            self.tokens -= 2
            if rol_sesion != "Administrador":
                raise PermissionError("Acceso denegado. Se requiere rol Administrador.")
            
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mensaje_descripcion = f"[PseudoAgente] La fecha y hora actual es: {fecha}"
            self.agregar_log("fecha_hoy", rol_sesion, mensaje_descripcion)
            return mensaje_descripcion
        except (PermissionError, ValueError) as e:
            mensaje_descripcion = str(e)
            self.agregar_log("fecha_hoy", rol_sesion, mensaje_descripcion)
            raise

    def obtener_tokens(self) -> int:
        """Devuelve la cantidad actual de tokens disponibles. No consume tokens."""
        return self.tokens
    
    def ping(self, rol: str) -> str:
        """Responde 'pong' a un ping. Consume 1 token."""
        self._verificar_vitalidad()
        if self.tokens < 1:
            raise ValueError(f"Tokens insuficientes. Requiere 1 token, tienes {self.tokens}.")
        self.tokens -= 1
        mensaje_descripcion = "Se ha enviado un ping y de respuesta se devolvió un pong."
        self.agregar_log("ping", rol, mensaje_descripcion)
        return mensaje_descripcion
    
    def lanzar_dado(self, rol: str) -> str:
        """Lanza un dado virtual y devuelve un número aleatorio entre 1 y 6. Consume 1 token."""
        self._verificar_vitalidad()
        if self.tokens < 1:
            raise ValueError(f"Tokens insuficientes. Requiere 1 token, tienes {self.tokens}.")
        self.tokens -= 1
        
        numero_dado = random.randint(1, 6)
        mensaje_descripcion = f"Se lanzó el dado y el resultado es: {numero_dado}"
        self.agregar_log("lanzar_dado", rol, mensaje_descripcion)
        
        return mensaje_descripcion

    def _verificar_vitalidad(self):
        """Verifica si el agente tiene tokens. Si no los tiene, lanza RuntimeError para detener al agente."""
        if self.tokens <= 0:
            raise RuntimeError("El Agente ha agotado todos sus tokens y no puede continuar.")

# Crear AgenteAdmin heredando de PseudoAgente es mejor que copiar el código porque permite reutilizar toda la funcionalidad existente sin duplicación.
# Además, facilita mantener y actualizar el código, ya que cambios en PseudoAgente se propagan automáticamente a AgenteAdmin.
class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str):
        """Inicializa un agente administrador con nombre, historial vacío y 200 tokens de batería (el doble del agente normal)."""
        super().__init__(nombre)
        self.tokens = 200
        self.es_admin = True
    
    def gestionar_historial(self, op: str, rol: str) -> str:
        """Gestiona el historial. Solo 'historial all' es gratuito. Las otras operaciones consumen tokens como un agente normal."""
        self._verificar_vitalidad()
        resultado = ""
        if op == "all":
            if not self.historial_chat:
                mensaje_descripcion = "[AgenteAdmin] El historial está vacío (sin costo de tokens)."
                self.agregar_log("historial all", rol, mensaje_descripcion)
                return mensaje_descripcion
            for i, recuerdo in enumerate(self.historial_chat):
                resultado += (
                    f"\nIteración: {i}\n"
                    f"Fecha: {recuerdo['timestamp']}\n"
                    f"Comando: {recuerdo['cmd']}\n"
                    f"Autor: {recuerdo['rol']}\n"
                    f"Mensaje: {recuerdo['descripción']}\n"
                )
            mensaje_descripcion = "Se mostró todo el historial (sin costo de tokens)."
            self.agregar_log("historial all", rol, mensaje_descripcion)
            return resultado
        elif op == "clear":
            # historial clear SÍ consume 10 tokens
            if self.tokens < 10:
                raise ValueError(f"Tokens insuficientes. Requiere 10 tokens, tienes {self.tokens}.")
            self.tokens -= 10
            self.historial_chat.clear()
            mensaje_descripcion = "[AgenteAdmin] El historial ha sido limpiado."
            self.agregar_log("historial clear", rol, mensaje_descripcion)
            return mensaje_descripcion
        else:
            # búsqueda por palabra clave SÍ consume 3 tokens
            if self.tokens < 3:
                raise ValueError(f"Tokens insuficientes. Requiere 3 tokens, tienes {self.tokens}.")
            self.tokens -= 3
            contador = 0
            for i, recuerdo in enumerate(self.historial_chat):
                if op in recuerdo["descripción"].lower():
                    contador += 1
                    resultado += (
                        f"\nIteración: {i}\n"
                        f"Autor: {recuerdo['rol']}\n"
                        f"Mensaje: {recuerdo['descripción']}\n"
                    )
            if contador == 0:
                mensaje_descripcion = "[AgenteAdmin] No encontré registros que coincidan con esa palabra."
                self.agregar_log("historial " + op, rol, mensaje_descripcion)
                return mensaje_descripcion
            mensaje_descripcion = f"La palabra clave es: {op} y hay {contador} coincidencias."
            self.agregar_log("historial " + op, rol, mensaje_descripcion)
            return (
                    f"La palabra clave es: {op} "
                    f"y hay {contador} coincidencias.\n"
                    + resultado
            )
