"""
tests/test_api.py — Tests automáticos del Reto Eutagógico.

Ejecutar:
    pytest tests/ -v

Cubre:
    (a) POST /misiones/ sin API key → 401
    (b) GET /briefing/{nombre} → estructura correcta con API externa mockeada
"""

import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("AGENCIA_API_KEY", "test_key_123")
os.environ.setdefault("EXTERNAL_API_URL", "https://api.adviceslip.com/advice")

from main import app

client = TestClient(app)

MISION_BODY = {
    "titulo": "Misión de prueba",
    "descripcion": "Test automatizado",
    "agente_asignado": "AgentePrueba",
    "estado": "pendiente",
    "energia_requerida": 10,
    "prioridad": "media",
}


# ── Test (a) — 401 sin API key ────────────────────────────────────────────────

def test_mision_sin_api_key_retorna_401():
    """
    POST /misiones/ sin X-API-KEY debe retornar 401.
    Verifica que la autenticación rechaza requests sin credenciales.
    """
    resp = client.post("/misiones/", json=MISION_BODY)
    assert resp.status_code == 401, f"Esperado 401, recibido {resp.status_code}"
    assert "inválida" in resp.json()["detail"]


def test_mision_con_api_key_incorrecta_retorna_401():
    """
    POST /misiones/ con X-API-KEY incorrecta debe retornar 401.
    """
    resp = client.post(
        "/misiones/",
        json=MISION_BODY,
        headers={"X-API-KEY": "clave_incorrecta"},
    )
    assert resp.status_code == 401


# ── Test (b) — briefing con estructura correcta ───────────────────────────────

def test_briefing_estructura_con_agente_existente():
    """
    GET /briefing/{nombre} debe retornar los 3 campos requeridos:
    agente (datos locales), consejo_de_mision (API externa), fuente_externa.
    La API externa está mockeada para que el test no dependa de internet.
    """
    # Primero creamos el agente en la DB de test
    client.post(
        "/agentes/",
        json={"nombre": "AgentePrueba", "rol": "explorador", "energia": 100},
        headers={"X-API-KEY": "test_key_123"},
    )

    # Mockeamos la API externa para no depender de internet
    mock_response = MagicMock()
    mock_response.json.return_value = {"slip": {"advice": "Consejo de prueba"}}

    with patch("main.requests.get", return_value=mock_response):
        resp = client.get("/briefing/AgentePrueba")

    assert resp.status_code == 200
    data = resp.json()

    assert "agente" in data,              "Falta campo 'agente'"
    assert "consejo_de_mision" in data,   "Falta campo 'consejo_de_mision'"
    assert "fuente_externa" in data,      "Falta campo 'fuente_externa'"
    assert data["consejo_de_mision"] == "Consejo de prueba"


def test_briefing_agente_inexistente_retorna_404():
    """
    GET /briefing/{nombre} con agente que no existe debe retornar 404.
    """
    resp = client.get("/briefing/AgenteQueNoExiste_XYZ")
    assert resp.status_code == 404


# ── Tests Pydantic validators ─────────────────────────────────────────────────

def test_mision_energia_negativa_retorna_422():
    """
    El validator de energia_requerida debe rechazar valores <= 0.
    """
    body = {**MISION_BODY, "energia_requerida": -5}
    resp = client.post("/misiones/", json=body, headers={"X-API-KEY": "test_key_123"})
    assert resp.status_code == 422


def test_mision_estado_invalido_retorna_422():
    """
    El validator de estado debe rechazar valores fuera del enum permitido.
    """
    body = {**MISION_BODY, "estado": "activo"}
    resp = client.post("/misiones/", json=body, headers={"X-API-KEY": "test_key_123"})
    assert resp.status_code == 422
