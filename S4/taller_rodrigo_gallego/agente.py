## Librerias adicionales para el taller
from datetime import datetime
import random

type Recuerdo = dict[str, str]
type MemoriaAgente = list[Recuerdo]

class PseudoAgente:
    def __init__ (self, usuario: str, rol: str):
        # Se definen las variables de la clase, las cuales serán válidas para todos los métodos de la misma,
        # con esto se evita el pasarlas como parámetros en cada función ya que se pueden acceder directamente
        # a través de 'self'.
        # a diferencia de las variables locales o temporales que solo existen dentro de la función donde se crean.
        self.usuario = usuario
        self.rol = rol
        self.historial_chat: MemoriaAgente = []
        self.sistema_activo = True
        self.tokens = 100
        self.mensaje = ""
        self.comando_valido = True # Se agrega esta variable para controlar cuando se guarda el log y cuando no

    def validar_pass(self, contrasena: str) -> str:
        self.tokens -= 20
        print(f"Validando contraseña para el usuario '{self.usuario}'...")
        if len(contrasena) >= 8 and any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in contrasena):
            return "La contraseña es fuerte."
        elif len(contrasena) >= 6:
            return "La contraseña es moderada."
        elif contrasena == self.usuario:
            return "La contraseña no debe ser igual al nombre de usuario."
        elif len(contrasena) == 0:
            return "La contraseña no puede estar vacía."
        else:
            return "La contraseña es débil."
        
    def calculadora(self) -> str:
        self.tokens -= 20
        num1 = input("Ingrese el primer número: ").strip()
        operador = input("Ingrese el operador (+, -, *, /): ").strip()
        num2 = input("Ingrese el segundo número: ").strip()
        try:
            num1 = float(num1)
            num2 = float(num2)
        except ValueError:
            raise ValueError("Por favor, ingrese números válidos.")

        if operador == "+":
            return str(num1 + num2)
        elif operador == "-":
            return str(num1 - num2)
        elif operador == "*":
            return str(num1 * num2)
        elif operador == "/":
            if num2 != 0:
                return str(num1 / num2)
            else:
                raise ValueError("División por cero no permitida.")
        else:
            raise ValueError("Operador no reconocido. Use +, -, *, o /.")
    
    def contar_letras(self, dato: str) -> str:
        # quitar los espacios de la palabra para contar solo las letras
        self.tokens -= 20
        palabra = dato.replace(" ", "")
        tot_letras = len(palabra)
        tot_vocales = sum(1 for p in palabra if p in "aeiou")
        tot_consonantes = tot_letras - tot_vocales
        return f"Total de letras: {tot_letras}, Vocales: {tot_vocales}, Consonantes: {tot_consonantes}"

    def gestionar_historial(self, accion: str) -> str:
        self.tokens -= 20
        log: str = ""
        if accion == "all":
            if not self.historial_chat:
                log = "El historial está vacío."
            else:
                log += f"Historial completo:\n"
                for entry in self.historial_chat:
                    # se retorna el log con el historial completo entrada por entrada
                    log += f"{entry}\n"
                    
        elif accion == "clear":
            self.historial_chat.clear()
            log = "Se limpió el historial."
        elif accion == "buscar":
            # Se almacena la entrada de busqueda, se limpian los espacios y se convierte a minusculas para facilitar la búsqueda
            keyword = input("Ingrese la palabra clave para buscar en el historial: ").strip().lower()
            # Se itera sobre el historial_chat para encontrar entradas que contengan la palabra clave "keyword" en el comando o en la descripción, se almacena el resultado en una nueva lista 'resultados'
            resultados: MemoriaAgente = [entry for entry in self.historial_chat if keyword in entry['cmd'] or keyword in entry['descripcion']]
            if resultados:
                log += f"Resultados de búsqueda para '{keyword}':\n"
                for entry in resultados:
                    log += f"{entry}\n"
            else:
                log=f"No se encontraron entradas en el historial que contengan '{keyword}'."
        self.comando_valido = False # No se guarda el log para el comando de historial, ya que es una consulta al mismo
        return log
    
    def almacenar_log(self, cmd: str) -> None:
        if self.comando_valido:
            d_log: Recuerdo = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "cmd": cmd,
                    "rol": self.rol,
                    "descripcion": self.mensaje}
                        
            self.historial_chat.append(d_log)
        self.comando_valido = True # Se resetea la variable para el siguiente comando
        self.mensaje = "" # Se resetea el mensaje para el siguiente comando

    def lanzar_dado(self) -> str:
        self.tokens -= 20
        resultado = random.randint(1, 6)
        return f"Has lanzado un dado y ha salido: {resultado}"
    
    def pseudo_action(self, cmd: str) -> None:
        if cmd == "salir":
            print("------Agente apagado. Vuelve pronto.------")
            self.sistema_activo = False
            self.mensaje = "Se ha solicitado terminar la sesión."
        elif cmd == "ping":
            self.tokens -= 20
            print("pong.")
            self.mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
        elif cmd == "contar":
            palabra = input("Ingrese una palabra: ").strip().lower()
            self.mensaje = self.contar_letras(palabra)
            print(self.mensaje)
        # Nueva funcionalidad: Mostrar fecha y hora actual
        elif cmd == "fecha_hoy":
            self.tokens -= 20
            # Se obtiene la fecha y hora actual formateada como "DD/MM/YYYY HH:MM:SS"
            fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Solo el usuario 'admin' tiene acceso a esta información, se verifica el usuario antes de mostrarla
            if self.usuario == "admin":
                print(f"Fecha y hora actual: {fecha_hora_actual}")
                self.mensaje = f"[PseudoAgente] La fecha y hora actual es: {fecha_hora_actual}"
            else:
                self.mensaje = "[Acceso Denegado] Este comando requiere privilegios de administrador."  
                # print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
                raise PermissionError("Acceso Denegado - Privilegios insuficientes.")
        # Nueva funcionalidad: Validar fortaleza de una contraseña
        elif cmd == "validar_pass":
            contrasena_a_validar = input("Ingrese la contraseña a validar: ").strip()
            # Se define la fortaleza de la contraseña basada en su longitud y la presencia de caracteres especiales
            self.mensaje = self.validar_pass(contrasena_a_validar)
            print(self.mensaje)
        # Función de calculadora
        elif cmd == "calculadora":
            try:
                resultado = self.calculadora()
                self.mensaje = f"Resultado: {resultado}"
                print(self.mensaje)
            except ValueError as ex:
                self.mensaje = f"Error: {ex}"
                print(self.mensaje)
        elif cmd == "lanzar_dado":
            resultado = self.lanzar_dado()
            self.mensaje = resultado
            print(self.mensaje)
        elif cmd == "historial":
            historial = input("""Historial de Comandos:
- 'all' ver todo el historial
- 'clear' limpiar el historial
- 'buscar' buscar en el historial por palabra clave
""")
            log: str = self.gestionar_historial(historial)
            print(log)
        else:
            print("------Comando desconocido. Intente de nuevo.-------")
            self.comando_valido = False
    
        self.almacenar_log(cmd)

    def iniciar(self, nombre: str = "AgenteConsola") -> None:
        print(f"----- Iniciando el pseudoagente {nombre} -------")
        print(f"Bienvenido, {self.usuario}. Eres un {self.rol}.")
        while self.sistema_activo:
            if self.tokens <= 0:
                    raise RuntimeError("Tokens insuficientes - Fin de la sesión.")        
            try:
                cmd = input(f"""Seleccione un comando para el pseudoagente (tokens disponibles: {self.tokens}):
    - 'salir' para terminar la sesión
    - 'ping' para recibir un pong
    - 'contar' para contar letras, vocales y consonantes en una palabra
    - 'fecha_hoy' para mostrar la fecha y hora actual
    - 'validar_pass' para validar la fortaleza de una contraseña
    - 'calculadora' para realizar operaciones matemáticas básicas
    - 'lanzar_dado' para lanzar un dado virtual
    - 'historial' para mostrar el historial de comandos
Agente: """).strip().lower()
                self.pseudo_action(cmd)
            except Exception as e:
                print(f"[Error] {e}")

# Se genera la clase AgenteAdmin que hereda de PseudoAgente, al aplicar el principio de Herencia de POO
# evitamos el código repetido y simplemente cambiamos lo que necesitamos que sea diferente
# en este caso, el método gestionar_historial se redefine para que no consuma tokens.
class AgenteAdmin(PseudoAgente):
    def __init__(self, usuario: str):
        super().__init__(usuario, "admin")
    
    def gestionar_historial(self, accion):
        log: str = ""
        if accion == "all":
            if not self.historial_chat:
                log = "El historial está vacío."
            else:
                log += f"Historial completo:\n"
                for entry in self.historial_chat:
                    # se retorna el log con el historial completo entrada por entrada
                    log += f"{entry}\n"
                    
        elif accion == "clear":
            self.historial_chat.clear()
            log = "Se limpió el historial."
        elif accion == "buscar":
            # Se almacena la entrada de busqueda, se limpian los espacios y se convierte a minusculas para facilitar la búsqueda
            keyword = input("Ingrese la palabra clave para buscar en el historial: ").strip().lower()
            # Se itera sobre el historial_chat para encontrar entradas que contengan la palabra clave "keyword" en el comando o en la descripción, se almacena el resultado en una nueva lista 'resultados'
            resultados: MemoriaAgente = [entry for entry in self.historial_chat if keyword in entry['cmd'] or keyword in entry['descripcion']]
            if resultados:
                log += f"Resultados de búsqueda para '{keyword}':\n"
                for entry in resultados:
                    log += f"{entry}\n"
            else:
                log=f"No se encontraron entradas en el historial que contengan '{keyword}'."
        self.comando_valido = False # No se guarda el log para el comando de historial, ya que es una consulta al mismo
        return log