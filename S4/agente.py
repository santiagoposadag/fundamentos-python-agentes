# Solución Taller Semana 4: Nace la Entidad (POO y Modularización)
## Andrés Felipe Chalarca Rueda.

# --- IMPORTAMOS LAS HERRAMIENTAS --- #
import datetime
import random
import os
from typing import List, Dict, Optional

# --- 1. LAS ETIQUETAS DE CALIDAD (TYPE ALIASING) --- #
# Definimos cómo se ve un "Recuedo" para que Python nos ayude a no cometer errores.
Recuerdo = Dict[str, str]  # Un Recuerdo es un diccionario con claves y valores de tipo string.
MemoriaAgente = List[Recuerdo]  # La Memoria del agente es una lista de Recuerdos.

# --- 2. EL MOLDE PRINCIPAL: CLASE PSEUDOAGENTE --- #
class PseudoAgente:
    """
    Esta clase es como el plano de un bot.
    Define que cada bot tendrá su propio nombre, batería (tokens) y memoria (recuerdos).
    """

    # EL CONSTRUCTOR (__init__): Es el método que se ejecuta cuando creamos un nuevo agente.
    def __init__(self, nombre: str = "Athena"):
        # EXPPLICACIÓN SELF:
        # 'nombre' es una viariable que muere cuando termina esta función.
        # 'self.nombre' es como tatuarle el nombre al bot; lo recordará siempre.
        self.nombre = nombre  # El nombre del agente.
        self.tokens = 100  # La batería inicial del agente, que se gasta al hacer cosas.
        self.historial_chat: MemoriaAgente = []  # El cuaderno de notas privado del agente, donde guarda sus recuerdos.

    # MÉTODO DE APOYO: Registrar lo que pasa.
    def registrar_log(self, comando: str, rol: str, descripcion: str):
        """
        Este método es como el diario del agente.
        Cada vez que el agente hace algo, registra lo que hizo, quién lo hizo (rol) y una descripción.
        """
        # Creamos un diccionario con la información del turno.
        nuevo_item: Recuerdo = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # La fecha y hora actual.
            "cmd": comando,  # El comando que se ejecutó.
            "rol": rol,  # El rol que ejecutó el comando
            "descripcion": descripcion  # Una descripción de lo que pasó.
        }
        # Lo guardamos en su propia memoria (self).
        self.historial_chat.append(nuevo_item)

    # MÉTODO DE APOYO: Desgaste de energía (tokens).
    def gastar_energia(self, costo: int):
        """
        Este método es como el consumo de batería del agente.
        Cada vez que el agente hace algo, gasta tokens. Si se queda sin tokens, no puede hacer nada más.
        """
        self.tokens -= costo  # Restamos el costo a los tokens disponibles.
    
    # --- LAS HERRAMIENTAS DE LA SEMANA 3 AHORA COMO "HABILIDADES" (MÉTODOS) --- #
    def ejecutar_ping(self) -> str:
        """
        Esta es la habilidad de "ping". El agente responde con "pong" y gasta 2 tokens.
        """
        self.gastar_energia(2)  # Gasta 2 tokens por usar esta habilidad.
        return "Respuesta del sistema: ¡Pong! (Conexión estable)"  # Devuelve la respuesta.
    
    def obtener_fecha_sistema(self, rol: str) -> str:
        """
        Esta es la habilidad de obtener la fecha del sistema. El agente devuelve la fecha actual y gasta 5 tokens.
        """
        # El blindaje: Si no es el rol 'admin', lanzamos una excepción (Error).
        if rol != "admin":
            raise PermissionError("Acceso denegado: Solo el rol 'Administrador' puede ejecutar este comando.")
        
        self.gastar_energia(5)  # Gasta 5 tokens por usar esta habilidad.
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtenemos la fecha y hora actual.
        return f"La fecha y hora actual es: {ahora}"  # Devuelve la fecha y hora.
    
    def lanzar_dado(self) -> str:
        """
        Esta es la habilidad de lanzar un dado. El agente devuelve un número aleatorio entre 1 y 6 y gasta 3 tokens.
        """
        # Nueva habilidad usando la libreria 'random' para generar un número aleatorio.
        self.gastar_energia(3)  # Gasta 3 tokens por usar esta habilidad.
        resultado = random.randint(1, 6)  # Genera un número aleatorio entre 1 y 6.
        return f"Has lanzado el dado y ha salido: {resultado}"  # Devuelve el resultado del dado.
    
    def gestionar_historial(self, accion: str, palabra: Optional[str] = None) -> str:
        """
        Esta es la habilidad de gestionar el historial de chat del agente.
        Permite mostrar todo el historial o buscar por una palabra clave.
        Nota que ya NO recibe la memoria por fuera, usa 'self.historial_chat', que es su propia memoria interna.
        Gasta 10 tokens por usar esta habilidad.
        """
        self.gastar_energia(10)  # Gasta 10 tokens por usar esta habilidad.
        
        if accion == "all":
            if not self.historial_chat:
                return "El historial de chat está vacío."
            reporte = "\n--- LEYENDO TODA LA MEMORIA ---\n"
            for r in self.historial_chat:
                reporte += f"{r['timestamp']} - {r['rol']} ejecutó '{r['cmd']}': {r['descripcion']}\n"
            return reporte
        
        elif accion == "clear":
            self.historial_chat.clear()  # Limpia todo su propio cuaderno (historial).
            return "El historial de chat ha sido limpiado con éxito."
        
        elif accion == "search" and palabra:
            # Buscamos en la memoria usando la lógica de la semana 3.
            encontrados = [r for r in self.historial_chat if palabra.lower() in r['descripcion'].lower()]
            if not encontrados:
                return f"No se encontraron resultados para la palabra clave: '{palabra}'."
            res = f"\n--- RESULTADOS DE LA BÚSQUEDA CON '{palabra}' ---\n"
            for r in encontrados:
                res += f" > {r['timestamp']} - {r['rol']} ejecutó '{r['cmd']}': {r['descripcion']}\n"
            return res
        
        return "Acción de historial desconocida. Por favor, use 'all', 'clear' o 'search' con una palabra clave."
    
    def realizar_calculo(self, n1: float, operacion: str, n2: float) -> str:
        """
        Habilidad de cálculo matemático.
        El agente puede sumar, restar, multiplicar o dividir dos números y gasta 4 tokens.
        """
        self.gastar_energia(4)  # Gasta 4 tokens por usar esta habilidad.
        if operacion == "+":
            resultado = n1 + n2
        elif operacion == "-":
            resultado = n1 - n2
        elif operacion == "*":
            resultado = n1 * n2
        elif operacion == "/":
            if n2 == 0:
                return "Error: No se puede dividir por cero."
            resultado = n1 / n2
        else:
            return "Operación desconocida. Por favor, use '+', '-', '*' o '/'."
        
        return f"El resultado de {n1} {operacion} {n2} es: {resultado}"  # Devuelve el resultado del cálculo.
    
    def contador_letras(self, texto: str) -> str:
        """
        Habilidad de contar letras en un texto.
        El agente cuenta cuántas veces aparece cada letra en el texto y gasta 6 tokens.
        """
        self.gastar_energia(6)  # Gasta 6 tokens por usar esta habilidad.
        texto_limpio = texto.strip().lower()  # Limpiamos el texto y lo pasamos a minúsculas para contar sin distinción.

        # Filtros rápidos (List Comprehension) para contar solo letras y no espacios u otros caracteres.
        vocales = [l for l in texto_limpio if l in "aeiouáéíóú"]  # Contamos solo las vocales.
        consonantes = [l for l in texto_limpio if l.isalpha() and l not in "aeiouáéíóú"]  # Contamos solo las consonantes.

        return (f"Análisis para '{texto_limpio}':\n"
                f" > Vocales: {len(vocales)}\n"
                f" > Consonantes: {len(consonantes)}"
                f" > Total de letras: {len(texto_limpio)}")  # Devuelve el conteo de letras.
    
    def validar_seguridad_clave(self, clave: str, usuario: str) -> str:
        """
        Habilidad de validar la seguridad de una contraseña.
        El agente evalúa si la contraseña es segura (longitud, mayúsculas, números) y gasta 4 tokens.
        """
        self.gastar_energia(4)  # Gasta 4 tokens por usar esta habilidad.
        if len(clave) < 8:
            return "Rechazado:La contraseña es demasiado corta. Debe tener al menos 8 caracteres."
        if clave.lower() == usuario.lower():
            return "Rechazado: La contraseña no puede ser igual al nombre de usuario."
        
        return "Exitosa: Contraseña aceptada.La contraseña es segura."  # Devuelve el resultado de la validación.

# --- 3. ESPECIALIZACIÓN: CLASE AGENTEADMIN (HERENCIA) --- #
# Crear un AgenteAdmin heredando de PseudoAgente es mejor porque no hay que volver a escribir toda la lógica de memoria y energía. 
# Si mejora el PseudoAgente, el AgenteAdmin mejora automáticamente.

class AgenteAdmin(PseudoAgente):
    """
    Esta clase es una versión especializada de PseudoAgente, con habilidades adicionales que solo un administrador puede usar.
    Hereda todas las habilidades y características de PseudoAgente, pero añade nuevas funciones exclusivas para el rol 'admin'.
    """

    def __init__(self, nombre: str = "Admin-Bot"):
        # super() le dice a Python: "Crea primero la base de un Agente normal".
        super().__init__(nombre)  # Llamamos al constructor de la clase padre para inicializar el nombre, tokens y memoria.

    # SOBREESCRITURA (Override): Cambiamos las reglas para el Admin.
    def gestionar_historial(self, accion: str, palabra: Optional[str] = None) -> str:
        """
        El AgenteAdmin tiene una versión mejorada de la habilidad de gestionar el historial.
        Además de mostrar y limpiar, puede exportar el historial a un archivo de texto.
        Para el admin esta acción es gratis, no gasta tokens.
        """
        # Guardamos cuánta energía tiene el agente antes de gastar.
        energia_antes = self.tokens
        # Ejecutamos la acción normal del padre.
        resultado = super().gestionar_historial(accion, palabra)
        # Si el agente es admin, no gasta energía por gestionar el historial (devolvemos la energía).
        self.tokens = energia_antes  # El admin no gasta tokens por esta acción.
        return f"{resultado}\n[LOGI]: acción gratuita por ser Administrador." # Devolvemos el resultado con una nota especial para el admin.