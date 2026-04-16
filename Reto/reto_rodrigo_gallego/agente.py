"""
agente.py - Capa de Dominio

Este módulo contiene las entidades principales de la Agencia de Agentes.
Siguiendo la Arquitectura Hexagonal, esta capa no tiene dependencias
de infraestructura (Base de Datos o API).
"""

from typing import Optional

class PseudoAgente:
    """Clase base para un agente estándar."""
    
    def __init__(
        self, 
        nombre: str, 
        tokens: int = 100, 
        rol: str = "invitado"
    ) -> None:
        self.nombre: str = nombre
        self.tokens: int = tokens
        self.rol: str = rol

    def descontar_energia(self, cantidad: int) -> bool:
        """
        Descuenta una cantidad de tokens del agente.
        Devuelve True si la operación fue exitosa, False si no hay energía suficiente.
        """
        if self.tokens >= cantidad:
            self.tokens -= cantidad
            return True
        return False

    def __repr__(self) -> str:
        return f"PseudoAgente(nombre={self.nombre}, tokens={self.tokens}, rol={self.rol})"


class AgenteAdmin(PseudoAgente):
    """Clase para un agente con privilegios de administrador."""
    
    def __init__(self, nombre: str, tokens: int = 100) -> None:
        # Forzamos el rol de admin
        super().__init__(nombre, tokens, rol="admin")

    def descontar_energia(self, cantidad: int) -> bool:
        """
        Override: Los administradores descuentan la mitad de energía 
        como beneficio de su rango (R2/Lógica de Negocio).
        """
        desc_admin = cantidad // 2
        if self.tokens >= desc_admin:
            self.tokens -= desc_admin
            return True
        return False

    def __repr__(self) -> str:
        return f"AgenteAdmin(nombre={self.nombre}, tokens={self.tokens}, rol={self.rol})"
