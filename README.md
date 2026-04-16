# Agentes — Reto de Consolidación

Integra POO, persistencia SQLite y API REST con FastAPI en un sistema modular con autenticación, variables de entorno, logs estructurados e inteligencia externa.

---

## Estructura del proyecto

```
agente.py      # Clases PseudoAgente y AgenteAdmin (dominio puro, sin SQL ni FastAPI)
db.py          # Capa de persistencia: todas las queries SQLite
main.py        # Aplicación FastAPI: endpoints, autenticación, logs
cliente.py     # Script de demostración end-to-end
seed.py        # Siembra la BD con datos iniciales
config.py      # Carga variables de entorno desde .env
.env.example   # Plantilla de variables de entorno (versionar SIN valores reales)
.gitignore     # Excluye .env y caché de Python
requirements.txt
README.md
```

---

## Instalación y ejecución

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` y asigna un valor a `AGENCIA_API_KEY` (cualquier string secreto, p. ej. `mi-clave-secreta-123`).

### 3. Sembrar la base de datos (primera vez)

```bash
python seed.py
```

Esto crea `agentes.db` con 4 agentes, 5 mensajes y 3 misiones en estados distintos.

### 4. Lanzar el servidor

```bash
uvicorn main:app --reload
```

Swagger UI disponible en: **http://localhost:8000/docs**

### 5. Ejecutar el demo end-to-end (en otra terminal)

```bash
python cliente.py
```

---

## Endpoints

| Método | Ruta | Protegido | Descripción |
|--------|------|-----------|-------------|
| `GET`  | `/` | No | Estado del servidor |
| `GET`  | `/agentes/` | No | Lista todos los agentes |
| `GET`  | `/agente/{nombre}` | No | Consulta un agente por nombre |
| `POST` | `/agentes/` | **Sí** | Registra un nuevo agente |
| `POST` | `/mensajes/` | **Sí** | Envía un mensaje entre agentes |
| `GET`  | `/mensajes/{nombre}` | No | Lee la bandeja de un agente |
| `POST` | `/misiones/` | **Sí** | Crea una misión (404 si el agente no existe) |
| `GET`  | `/misiones/{id}` | No | Consulta una misión por ID |
| `GET`  | `/agente/{nombre}/misiones` | No | Lista las misiones de un agente |
| `POST` | `/misiones/{id}/completar` | **Sí** | Completa una misión y descuenta energía |
| `GET`  | `/briefing/{nombre}` | No | Datos del agente + inteligencia externa |

**Endpoints protegidos:** requieren el header `X-API-KEY: <tu_clave>`.

> **Decisión:** se protegen únicamente los endpoints de escritura (todos los `POST`). Los `GET` son públicos porque la información de agentes y misiones no es sensible y facilita la consulta desde Swagger UI sin configuración adicional. Esta política es coherente con el principio de mínimo privilegio aplicado al contexto de la Agencia.

---

## Decisiones de Ingeniería

### 1. Esquema de la tabla `misiones`

Más allá del mínimo obligatorio se añadieron tres columnas:

- **`prioridad TEXT`** (`alta` / `media` / `baja`): permite al operador de la Agencia clasificar la urgencia de cada misión y filtrarlas visualmente en Swagger UI sin necesidad de código adicional.
- **`recompensa INTEGER`**: energía devuelta al agente al completar la misión (mecánica de juego). Abre la puerta a implementar `POST /misiones/{id}/completar` que sume la recompensa en una futura iteración.
- **`creado_por TEXT`**: campo de auditoría que registra qué operador (o script) creó la misión, útil para trazabilidad en un sistema multiusuario.

### 2. API pública elegida

Se usa **Advice Slip** (`https://api.adviceslip.com/advice`): API gratuita, sin autenticación, que retorna un consejo estratégico aleatorio en JSON (`{"slip": {"id": ..., "advice": "..."}}`). Encaja con la narrativa de los agentes porque reciben "inteligencia del mundo exterior" (consejos tácticos) antes de una misión, como si fuera un briefing real. No requiere registro ni API key, lo que simplifica la configuración del proyecto.

### 3. Estrategia de resiliencia frente a fallos externos

Si la API externa falla o supera el **timeout de 5 segundos**, el endpoint `GET /briefing/{nombre}` **no lanza un error al cliente**. En su lugar retorna los datos locales del agente con:

```json
{
  "inteligencia_externa": "Inteligencia exterior no disponible. Procede con los datos locales.",
  "fuente_externa": "fallback"
}
```

Esta decisión garantiza que el servidor **nunca se bloquea** esperando un tercero y que el cliente siempre recibe una respuesta útil (con datos locales completos). Se registra un `logger.warning` para que el operador sepa que el fallback se activó sin que el usuario final lo note.

---

## Política de autenticación

Enviar el header en cada request protegido:

```
X-API-KEY: tu_clave_aquí
```

Ejemplo con `curl`:

```bash
curl -X POST http://localhost:8000/misiones/ \
  -H "X-API-KEY: mi-clave-secreta-123" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Misión X","agente_asignado":"Orion","energia_requerida":30}'
```

---

## Verificación del checklist del reto

- [x] El servidor levanta sin errores con `uvicorn main:app --reload`.
- [x] Todos los endpoints aparecen en `http://localhost:8000/docs`.
- [x] Los endpoints de escritura rechazan requests sin `X-API-KEY` válido con código **401**.
- [x] `GET /briefing/{nombre}` retorna JSON con datos locales + inteligencia externa.
- [x] `cliente.py` ejecuta el flujo completo sin intervención manual.
- [x] Los datos persisten entre reinicios del servidor.
- [x] En `main.py` no hay `print`; todo pasa por `logger.*`.
- [x] `.env` no está versionado; existe `.env.example`.
- [x] Agente con rol `"admin"` → `isinstance(agente, AgenteAdmin)` devuelve `True`.
- [x] `README.md` justifica las tres Decisiones de Ingeniería.

---

## Evidencia visual

Añadir capturas de pantalla en la carpeta `screenshots/`:

| Archivo | Qué debe mostrar |
|---------|-----------------|
| `01_401_sin_key.png` | `POST /misiones/` sin `X-API-KEY` → **401** |
| `02_201_con_key.png` | `POST /misiones/` con `X-API-KEY` válida → **201** |
| `03_briefing.png` | `GET /briefing/{nombre}` → JSON con datos locales + externos |

---

## Referencias consultadas

- [FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI — Header Parameters](https://fastapi.tiangolo.com/tutorial/header-params/)
- [python-dotenv — Documentación](https://pypi.org/project/python-dotenv/)
- [Python logging — HOWTO](https://docs.python.org/3/howto/logging.html)
- [Requests — Timeouts y manejo de excepciones](https://docs.python-requests.org/en/latest/user/quickstart/#timeouts)
- [Advice Slip API](https://api.adviceslip.com/)
- [Pydantic v2 — Field validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [SQLite — Parámetros en queries](https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders)