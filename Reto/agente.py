# Este módulo define la clase PseudoAgente, que es la base para cualquier agente en nuestro sistema.
# Aquí también definimos la clase AgenteAdmin, que es una especialización de PseudoAgente con habilidades mejoradas.
# El cerebro (Sabe gastar energía y usar habilidades).

import random # Para la habilidad de lanzar dado
import datetime # Para la habilidad de obtener fecha y hora del sistema (Requisito R2)
# typing nos ayuda a que el código sea más robusto (Documentación clara)
from typing import Optional, List, Dict # Para definir tipos de datos más complejos en las habilidades (Requisito R2)

# ============================================================ #
# CLASE BASE: EL ADN DEL AGENTE (Semana 4 + Adaptación Semana 5) 
# ============================================================ #
class PseudoAgente: # El "ADN" de cualquier agente. Define su identidad, energía y habilidades básicas.
    """
    Esta es la 'plantilla' de cualquier agente. 
    A diferencia de la Semana 4, aquí recibimos 'rol' y 'energia' en el constructor 
    porque esos datos vendrán desde la base de datos (SQLite).
    """
    def __init__(self, nombre: str, rol: str = "explorer", energia: int = 100):
        # Usamos nombres que coinciden con las columnas de nuestra tabla SQL
        self.nombre = nombre
        self.rol = rol
        self.energia = energia 

    def __str__(self):
        """
        Muestra la identidad del agente de forma amigable.
        """
        return f"Agente: {self.nombre} | Rol: {self.rol} | Energía: {self.energia}%"

    def gastar_energia(self, costo: int):
        """
        Lógica de cansancio: cada acción gasta energía. 
        Evitamos que la energía sea negativa (piso de 0).
        """
        self.energia -= costo
        if self.energia < 0:
            self.energia = 0

    # --- HABILIDADES (NOS TRAEMOS LAS HERRAMIENTAS DE SEMANAS ANTERIORES) --- #
    
    def ejecutar_ping(self) -> str:
        """
        Prueba de conexión básica. Gasta poca energía. 
        Útil para verificar que el agente está 'vivo'. 
        Devuelve un ´pong´ como respuesta.
        """
        self.gastar_energia(2)
        return f"[{self.nombre}]: ¡Pong! Conexión activa."
    
    def obtener_fecha_sistema(self) -> str:
        """
        Obtiene la fecha y hora del sistema.
        """
        if self.rol != "admin":
            return "[Acceso denegado]: Solo administradores pueden ver la fecha."
        self.gastar_energia(5)
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[Fecha/Hora]: {ahora}"    
    
    def lanzar_dado(self) -> str:
        """
        Genera un número al azar. Útil para decisiones aleatorias.
        """
        self.gastar_energia(3)
        resultado = random.randint(1, 6)
        return f"[{self.nombre}]: Lanzó un dado y sacó: {resultado}"
    
    def contador_letras(self, texto: str) -> str:
        """
        Habilidad de contar letras en un texto.
        El agente cuenta cuántas veces aparece cada letra en el texto.
        """
        self.gastar_energia(6)
        limpio = texto.strip().lower()  # Limpiamos el texto y lo pasamos a minúsculas para contar sin distinción.
        # Filtros rápidos (List Comprehension) para contar solo letras y no espacios u otros caracteres.
        vocales = [l for l in limpio if l in "aeiouáéíóú"]  # Contamos solo las vocales.
        consonantes = [l for l in limpio if l.isalpha() and l not in "aeiouáéíóú"]  # Contamos solo las consonantes.
        return (f"Análisis para '{limpio}':\n"
                f" > Vocales: {len(vocales)}\n"
                f" > Consonantes: {len(consonantes)}"
                f" > Total de letras: {len(limpio)}")  # Devuelve el conteo de letras.    
    
    def validar_seguridad_clave(self, clave: str, usuario: str) -> str:
        """
        Habilidad de validar la seguridad de una contraseña.
        El agente evalúa si la contraseña es segura (longitud, mayúsculas, números).
        """
        self.gastar_energia(4)
        if len(clave) < 8:
            return "Rechazado:La contraseña es demasiado corta. Debe tener al menos 8 caracteres."
        if clave.lower() == usuario.lower():
            return "Rechazado: La contraseña no puede ser igual al nombre de usuario."
        
        return "Exitosa: Contraseña aceptada.La contraseña es segura."  # Devuelve el resultado de la validación.

    
    def realizar_calculo(self, n1: float, operacion: str, n2: float) -> str:
        """
        Habilidad lógica de cálculo matemático. 
        """
        self.gastar_energia(4)
        if operacion == "+": resultado = n1 + n2
        elif operacion == "-": resultado = n1 - n2
        elif operacion == "*": resultado = n1 * n2
        elif operacion == "/":
            if n2 == 0: return "[Error]: División por cero no permitida."
            resultado = n1 / n2
        else:
            return "¿? Operación no reconocida."
        return f"[{self.nombre}]: Calculó: {resultado}"


# ============================================================ #
# ESPECIALIZACIÓN: EL AGENTE ADMINISTRADOR (Herencia)
# ============================================================ #
class AgenteAdmin(PseudoAgente):
    """
    Esta clase es 'hija' de PseudoAgente. 
    Cumple el requisito R2: Tiene comportamientos diferentes por su rol.
    """
    def __init__(self, nombre: str, energia: int = 200):
        # super() llama al constructor del padre pero fija el rol como 'admin'
        super().__init__(nombre, rol="admin", energia=energia)

    def gastar_energia(self, costo: int):
        """
        POLIMORFISMO: El admin tiene una armadura que lo hace 
        gastar solo la mitad de la energía que un agente normal. Es decir, es más eficiente.
        """
        costo_reducido = costo // 2 # Calculamos la mitad del costo (división entera //)
        # Llamamos al método gastar_energia del padre pero con el costo barato
        super().gastar_energia(costo_reducido)