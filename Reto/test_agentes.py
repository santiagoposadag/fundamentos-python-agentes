"""
test_agentes.py — Prueba directa de las clases PseudoAgente y AgenteAdmin.

Ejecutar:
    python test_agentes.py
"""

from agente import AgenteAdmin, PseudoAgente

SEP = "─" * 45


def titulo(texto: str) -> None:
    print(f"\n{SEP}")
    print(f"  {texto}")
    print(SEP)


# ── PseudoAgente ──────────────────────────────────────────────────────────────
titulo("PseudoAgente — 'Nova' con 80 de energía")
nova = PseudoAgente("Nova", energia=80)
print(f"Energía inicial: {nova.energia}")

print(nova.ping())                              # costo 2 → queda 78
print(nova.contar_letras("hola mundo"))         # costo 5 → queda 73
print(nova.calculadora(10, "+", 5))            # costo 5 → queda 68
print(nova.calculadora(100, "/", 0))           # división por cero
print(nova.lanzar_dado())                       # costo 1 → queda 67
print(nova.validar_password("abc", "Nova"))     # muy corta
print(nova.validar_password("Nova", "Nova"))    # igual al usuario
print(nova.validar_password("Segura123", "Nova"))  # válida → costo 3

print(f"Energía tras operaciones: {nova.energia}")

# historial
nova.gestionar_historial("all")   # costo 10
print(nova.gestionar_historial("all"))

# usar_energia (para misiones)
titulo("usar_energia — descuenta como lo haría una misión")
print(f"Antes: {nova.energia}")
nova.usar_energia(20)
print(f"Después de usar 20: {nova.energia}")


# ── AgenteAdmin ───────────────────────────────────────────────────────────────
titulo("AgenteAdmin — 'Orion' con 150 de energía")
orion = AgenteAdmin("Orion", energia=150)
print(f"Energía inicial: {orion.energia}")

orion.ping()                                    # costo 2
energia_antes = orion.energia
orion.gestionar_historial("all")                # admin: SIN costo
print(f"Energía antes/después de historial: {energia_antes} / {orion.energia}  (no cambió)")


# ── isinstance ────────────────────────────────────────────────────────────────
titulo("isinstance — verificación de tipos")
print(f"nova  is PseudoAgente: {isinstance(nova,  PseudoAgente)}")   # True
print(f"nova  is AgenteAdmin:  {isinstance(nova,  AgenteAdmin)}")    # False
print(f"orion is PseudoAgente: {isinstance(orion, PseudoAgente)}")   # True (hereda)
print(f"orion is AgenteAdmin:  {isinstance(orion, AgenteAdmin)}")    # True

print(f"\n{SEP}")
print("  Pruebas completadas.")
print(SEP)
