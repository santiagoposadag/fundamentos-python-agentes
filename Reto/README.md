# Agencia de Agentes

Reto de consolidación del curso **Fundamentos de Python — Agentes**.  
Integra POO (S4), SQLite (S5 S1) y FastAPI (S5 S2) en un sistema completo con autenticación, variables de entorno, logging estructurado y consumo de API pública.

---

## Requisitos previos

- Python 3.12+
- Git

---

## Instalación

```bash
# 1. Posiciónate en la carpeta del reto
cd Reto

# 2. Crea y activa el entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate         # macOS / Linux

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Configura las variables de entorno
copy .env.example .env              # Windows
# cp .env.example .env              # macOS / Linux
# Edita .env y pon tu propia AGENCIA_API_KEY
```

---

## Ejecución

### Servidor

```bash
# En una terminal (con el entorno virtual activo y desde Reto/)
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Swagger UI disponible en: **http://127.0.0.1:8000/docs**

### Cliente de demostración

```bash
# En otra terminal (con el entorno virtual activo y desde Reto/)
python cliente.py
```

El cliente ejecuta el flujo completo sin intervención manual: crea agentes, misiones, las completa, consulta briefings y envía mensajes.

---

## Tabla de endpoints

| Método | Ruta | Protegido | Descripción |
|--------|------|-----------|-------------|
| `GET`  | `/` | No | Estado del servidor |
| `GET`  | `/agentes/` | No | Lista todos los agentes |
| `GET`  | `/agente/{nombre}` | No | Obtiene un agente por nombre |
| `POST` | `/agentes/` | **Sí** | Crea un agente |
| `POST` | `/mensajes/` | **Sí** | Envía un mensaje entre agentes |
| `GET`  | `/mensajes/{nombre}` | No | Lee la bandeja de un agente |
| `POST` | `/misiones/` | **Sí** | Crea una misión |
| `GET`  | `/misiones/{id}` | No | Obtiene una misión por ID |
| `GET`  | `/agente/{nombre}/misiones` | No | Lista misiones de un agente |
| `POST` | `/misiones/{id}/completar` | **Sí** | Completa una misión y descuenta energía |
| `GET`  | `/briefing/{nombre}` | No | Datos locales del agente + API externa |

Los endpoints protegidos requieren el header `X-API-KEY` con el valor configurado en `.env`.

---

## Estructura del proyecto

```
Reto/
├── agente.py          # Clases PseudoAgente y AgenteAdmin (solo lógica de negocio)
├── db.py              # Capa SQLite: tablas agentes, mensajes y misiones
├── main.py            # Servidor FastAPI: endpoints, auth, logging
├── cliente.py         # Guion de demostración end-to-end
├── config.py          # Carga variables de entorno desde .env
├── requirements.txt   # Dependencias del proyecto
├── .env               # Secretos locales (NO versionado)
├── .env.example       # Plantilla de variables (SÍ versionado)
└── agentes.db         # Base de datos SQLite con datos semilla
```

---

## Decisiones de Ingeniería

### 1. Esquema de la tabla `misiones`

Además del mínimo requerido, añadí dos columnas:

- **`prioridad` (INTEGER, default 1):** permite ordenar misiones por urgencia sin leer toda la tabla (`ORDER BY prioridad DESC`). Un admin puede crear misiones de prioridad 3 mientras el grueso son de prioridad 1. Es un dato que existe desde la creación y no requiere lógica adicional en Python.
- **`creado_por` (TEXT, default 'sistema'):** auditoría básica — registra qué operador creó la misión. El valor viene del campo `creado_por` del `MisionRequest`, que `main.py` recibe del cliente. Así, si hay un problema de integridad, se puede rastrear el origen sin revisar logs.

### 2. API pública elegida

Elegí **Open Notify** (`http://api.open-notify.org/astros.json`) porque encaja perfectamente con la narrativa de agentes: el briefing muestra en tiempo real cuántas personas están en el espacio y sus nombres — como un reporte de "agentes en misión activa" fuera del planeta. Es una API pública, gratuita, sin autenticación, usa HTTP puro (sin SSL) y devuelve un JSON estable con los campos `people`, `number` y `message`.

### 3. Estrategia de resiliencia ante fallo externo

Si Open Library tarda más de 3 segundos o devuelve un error, el endpoint `GET /briefing/{nombre}` responde igual pero con:
```json
{
  "inteligencia_externa": {"lectura_recomendada": "Fuente externa no disponible."},
  "fuente_externa": "no disponible (timeout)"
}
```
Decidí **degradar el servicio** en vez de fallar con 500 porque el briefing contiene información local valiosa (energía, misiones, clase del agente) que sigue siendo útil aunque la fuente externa no responda. Un 500 por culpa de un tercero sería injusto para el cliente. El `logger.warning` registra el fallo para que el equipo de operaciones lo investigue sin interrumpir el flujo.

---

## Autenticación

Los endpoints de escritura requieren el header `X-API-KEY`. Los `GET` son públicos porque leer datos no altera el estado del sistema.

**Con key válida:**
```bash
curl -X POST http://127.0.0.1:8000/agentes/ \
  -H "X-API-KEY: agencia-super-secreta-2026" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Atlas", "rol": "agente", "energia": 100}'
```

**Sin key (devuelve 401):**
```bash
curl -X POST http://127.0.0.1:8000/agentes/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Atlas", "rol": "agente", "energia": 100}'
```

---

## Referencias consultadas

- [FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI — Header Parameters](https://fastapi.tiangolo.com/tutorial/header-params/)
- [python-dotenv — Documentación oficial](https://saurabh-kumar.com/python-dotenv/)
- [Python logging — HOWTO](https://docs.python.org/3/howto/logging.html)
- [Python logging — basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig)
- [requests — Timeouts](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)
- [Open Notify API — Personas en el espacio](http://open-notify.org/Open-Notify-API/People-In-Space/)
- [Public APIs list (GitHub)](https://github.com/public-apis/public-apis)
- [Pydantic v2 — BaseModel](https://docs.pydantic.dev/latest/concepts/models/)
- [SQLite — Python docs](https://docs.python.org/3/library/sqlite3.html)
