
"""
agente.py — Clases de dominio para la Agencia

Contiene las clases PseudoAgente y AgenteAdmin.
No incluye lógica de base de datos ni FastAPI.
"""

import datetime
import random
import json
import os

# Type alias para historial
Historial = dict[str, str]

class PseudoAgente:
    def __init__(self, nombre: str = "Athena", energia: int = 100):
        self.nombre = nombre
        self.energia = energia
        self.historial_chat: list[Historial] = []
        self.ruta_historial: str = f"historial_{self.nombre}.json"

    def registrar_log(self, comando: str, rol_activo: str, mensaje: str):
        d_log: Historial = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": comando,
            "rol": rol_activo,
            "descripcion": mensaje
        }
        self.historial_chat.append(d_log)

    def gestionar_historial(self, op: str, rol: str):
        self.energia -= 30
        if op == "all":
            mensaje = f"[{self.nombre}] Historial mostrado a las {datetime.datetime.now().strftime('%H:%M:%S')}"
            self.registrar_log("hist all", rol, mensaje)
            return self.historial_chat
        if op == "clear":
            mensaje = f"[{self.nombre}] Historial borrado a las {datetime.datetime.now().strftime('%H:%M:%S')}"
            self.registrar_log("hist clear", rol, mensaje)
            self.historial_chat.clear()
            return mensaje

    def descontar_energia(self, cantidad: int):
        self.energia = max(0, self.energia - cantidad)

    def lanzar_dado(self) -> str:
        self.energia -= 5
        resultado = random.randint(1, 6)
        return f"[{self.nombre}] Resultado del dado: {resultado}"

    def guardar_historial(self) -> str:
        self.energia -= 10
        with open(self.ruta_historial, "w", encoding="utf-8") as archivo:
            json.dump(self.historial_chat, archivo, indent=2, ensure_ascii=False)
        ruta_completa = os.path.abspath(self.ruta_historial)
        return f"[{self.nombre}] Historial guardado en: {ruta_completa}"

    def cargar_historial(self) -> str:
        self.energia -= 10
        if not os.path.exists(self.ruta_historial):
            return f"[{self.nombre}] No se encontró el archivo: {self.ruta_historial}"
        with open(self.ruta_historial, "r", encoding="utf-8") as archivo:
            self.historial_chat = json.load(archivo)
        return f"[{self.nombre}] Historial cargado. {len(self.historial_chat)} registros recuperados."

class AgenteAdmin(PseudoAgente):
    def gestionar_historial(self, op: str, rol: str):
        # Admin no descuenta energía
        if op == "all":
            mensaje = f"[{self.nombre}] Historial mostrado (sin costo - Admin)"
            self.registrar_log("hist all", rol, mensaje)
            return self.historial_chat
        if op == "clear":
            mensaje = f"[{self.nombre}] Historial borrado (sin costo - Admin)"
            self.registrar_log("hist clear", rol, mensaje)
            self.historial_chat.clear()
            return mensaje
