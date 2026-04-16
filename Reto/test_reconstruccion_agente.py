import time
import unittest

from agente import AgenteAdmin, PseudoAgente
from db import despertar_agente, registrar_agente


def reconstruir_instancia_desde_db(nombre: str):
    """Replica la regla de reconstruccion usada en main.py al completar misiones."""
    agente_data = despertar_agente(nombre)
    if not agente_data:
        return None
    if agente_data["rol"] == "admin":
        return AgenteAdmin(agente_data["nombre"], agente_data["energia"])
    return PseudoAgente(agente_data["nombre"], agente_data["energia"])


class TestReconstruccionAgente(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        suffix = str(int(time.time() * 1000))
        cls.admin_name = f"AdminAuto_{suffix}"
        cls.operativo_name = f"OperativoAuto_{suffix}"

        registrar_agente(cls.admin_name, "admin", 200)
        registrar_agente(cls.operativo_name, "operativo", 100)

    def test_admin_reconstruye_como_agente_admin(self):
        agente = reconstruir_instancia_desde_db(self.admin_name)
        self.assertIsNotNone(agente)
        self.assertIsInstance(agente, AgenteAdmin)

    def test_no_admin_reconstruye_como_pseudo_agente(self):
        agente = reconstruir_instancia_desde_db(self.operativo_name)
        self.assertIsNotNone(agente)
        self.assertIsInstance(agente, PseudoAgente)
        self.assertNotIsInstance(agente, AgenteAdmin)


if __name__ == "__main__":
    unittest.main(verbosity=2)
