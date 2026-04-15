import datetime
import random

class PseudoAgente:
    def __init__(self, nombre: str, rol: str = "agente", energia: int = 100):
        self.nombre = nombre
        self.rol = rol
        self.energia = energia
        self.historial: list[dict] = []

    def consumir_energia(self, cantidad: int) -> str:
        if cantidad > self.energia:
            raise ValueError(
                f"Energía insuficiente: se requieren {cantidad}, "
                f"quedan {self.energia}."
            )
        self.energia -= cantidad
        return f"[{self.nombre}] Energía consumida: -{cantidad}. Restante: {self.energia}."

    def recargar_energia(self, cantidad: int) -> str:
        self.energia += cantidad
        return f"[{self.nombre}] Energía recargada: +{cantidad}. Total: {self.energia}."

    def registrar_log(self, comando: str, descripcion: str) -> None:
        self.historial.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "comando": comando,
            "descripcion": descripcion,
        })

    def ver_historial(self) -> list[dict]:
        self.registrar_log("ver_historial", "Historial consultado.")
        return self.historial

    def lanzar_dado(self) -> int:
        resultado = random.randint(1, 6)
        self.registrar_log("lanzar_dado", f"Resultado: {resultado}")
        return resultado

    def resumen(self) -> dict:
        return {
            "nombre": self.nombre,
            "rol": self.rol,
            "energia": self.energia,
        }

    def __repr__(self) -> str:
        return f"PseudoAgente(nombre={self.nombre!r}, rol={self.rol!r}, energia={self.energia})"

class AgenteAdmin(PseudoAgente):
    def __init__(self, nombre: str, energia: int = 100):
        # Llama al constructor del padre; el rol siempre es "admin"
        super().__init__(nombre=nombre, rol="admin", energia=energia)

    def consumir_energia(self, cantidad: int) -> str:
        costo_real = max(1, cantidad // 2)
        if costo_real > self.energia:
            raise ValueError(
                f"Energía insuficiente (admin): se requieren {costo_real}, "
                f"quedan {self.energia}."
            )
        self.energia -= costo_real
        return (
            f"[{self.nombre}] (Admin) Energía consumida: -{costo_real} "
            f"(50% de {cantidad}). Restante: {self.energia}."
        )

    def __repr__(self) -> str:
        return f"AgenteAdmin(nombre={self.nombre!r}, energia={self.energia})"