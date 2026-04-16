import datetime
import random

class PseudoAgente:
    def __init__(self, nombre: str, rol: str = "explorador", energia: int = 100):
        self.nombre = nombre
        self.rol = rol
        self.energia = energia
        self.historial_chat = []

    def registrar_log(self, comando: str, rol_activo: str, mensaje: str):
        d_log = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": comando,
            "rol": rol_activo,
            "descripcion": mensaje
        }
        self.historial_chat.append(d_log)

    def descontar_energia(self, cantidad: int):
        """Descuenta energía del agente. El PseudoAgente descuenta la cantidad exacta."""
        self.energia -= cantidad
        if self.energia < 0:
            self.energia = 0
        return f"[{self.nombre}] Energía descontada: {cantidad}. Energía restante: {self.energia}"

    def lanzar_dado(self) -> str:
        self.descontar_energia(5)
        resultado = random.randint(1, 6)
        return f"[{self.nombre}] Resultado del dado: {resultado}"

class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str, energia: int = 100):
        super().__init__(nombre, rol="admin", energia=energia)

    def descontar_energia(self, cantidad: int):
        """Override: El AgenteAdmin es más eficiente y solo descuenta la mitad de la energía."""
        descuento_real = cantidad // 2
        self.energia -= descuento_real
        if self.energia < 0:
            self.energia = 0
        return f"[{self.nombre}] (Admin) Descuento eficiente: {descuento_real} (original: {cantidad}). Energía restante: {self.energia}"
