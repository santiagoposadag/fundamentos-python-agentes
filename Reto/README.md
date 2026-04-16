# La Agencia de Agentes

API REST para gestionar agentes, mensajes y misiones. Integra POO (S4) con persistencia SQLite y FastAPI (S5).

## Requisitos

- Python 3.12 o superior

## Instalación

```bash
cd Reto/
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración

```bash
cp .env.example .env
# Editá .env con tu API key
```

Contenido de `.env`:
```
AGENCIA_API_KEY=mi_clave_secreta
EXTERNAL_API_URL=https://api.adviceslip.com/advice
```

## Ejecución

```bash
# Terminal 1 — servidor
uvicorn main:app --reload

# Terminal 2 — demo completa
python cliente.py

# Swagger UI
http://localhost:8000/docs
```

---

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/` | No | Estado del servidor |
| GET | `/agentes/` | No | Lista todos los agentes |
| GET | `/agente/{nombre}` | No | Datos de un agente |
| POST | `/agentes/` | Sí | Registra un nuevo agente |
| POST | `/mensajes/` | No | Envía un mensaje |
| GET | `/mensajes/{nombre}` | No | Bandeja de entrada de un agente |
| POST | `/misiones/` | Sí | Crea una misión asignada a un agente |
| GET | `/misiones/{id}` | No | Detalle de una misión |
| GET | `/agente/{nombre}/misiones` | No | Misiones asignadas a un agente |
| POST | `/misiones/{id}/completar` | Sí | Completa una misión y descuenta energía |
| GET | `/briefing/{nombre}` | No | Datos del agente + consejo de API externa |

**Auth**: header `X-API-KEY: <valor de AGENCIA_API_KEY>`

---

## Decisiones de Ingeniería

### 1. Esquema de la tabla `misiones`

Además del mínimo requerido, agregué dos columnas:
- `prioridad TEXT` (`alta` / `media` / `baja`): permite filtrar misiones por urgencia sin necesidad de agregar lógica extra de ordenamiento en el cliente. Es información que el asignador de misiones necesita al momento de crear, no después.
- `completada_at TEXT`: timestamp de cuándo se marcó como completada. Sirve para auditoría y para calcular tiempos de respuesta por agente en el futuro. No cuesta nada almacenarlo y es imposible reconstruirlo después.

### 2. API pública elegida

Elegí **adviceslip.com** (`https://api.adviceslip.com/advice`). Devuelve un consejo aleatorio en JSON sin autenticación ni rate limit documentado. Encaja con la narrativa de "briefing de misión": el agente recibe un consejo operacional antes de actuar. El campo `consejo_de_mision` en la respuesta hace que tenga sentido semántico dentro de la Agencia, no parece un dato arbitrario pegado.

### 3. Estrategia de resiliencia

Si la API externa falla o tarda más de 3 segundos (`timeout=3`), el `except Exception` captura cualquier error (timeout, DNS, respuesta malformada) y devuelve un valor de fallback: `"Sin datos externos disponibles en este momento."`. El endpoint siempre responde con 200 y los datos locales del agente intactos. Se loguea un `WARNING` para que el operador sepa que el fallback se activó. La decisión es no propagar el error al cliente porque la información externa es complementaria, no bloqueante.

---

## Referencias consultadas

- [FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI — Header Parameters](https://fastapi.tiangolo.com/tutorial/header-params/)
- [python-dotenv docs](https://pypi.org/project/python-dotenv/)
- [Python logging — HOWTO](https://docs.python.org/3/howto/logging.html)
- [requests — Timeouts](https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts)
- [adviceslip API](https://api.adviceslip.com/)
- [Pydantic v2 — BaseModel](https://docs.pydantic.dev/latest/concepts/models/)
