# Agencia de Agentes — Reto de Consolidacion

Reto de Consolidacion — Fundamentos de Python para Ingenieria de Agentes (Sofka).

Une lo visto en Semana 4 (POO) y Semana 5 (SQLite + FastAPI): la Agencia gestiona agentes,
les asigna misiones, registra mensajes y consulta informacion de paises reales para el briefing.

---

## Como ejecutar

Todos los comandos se corren desde dentro de la carpeta `Reto/`.

### 1. Instalar dependencias

```bash
# Windows
venv\Scripts\pip install -r requirements.txt

# Mac / Linux
venv/bin/pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Abrir .env y completar AGENCIA_API_KEY con cualquier clave secreta
```

### 3. Poblar la base de datos (solo la primera vez)

```bash
# Windows
venv\Scripts\python seed.py

# Mac / Linux
venv/bin/python seed.py
```

### 4. Levantar el servidor

```bash
# Windows
venv\Scripts\uvicorn main:app --reload

# Mac / Linux
venv/bin/uvicorn main:app --reload
```

Servidor: http://localhost:8000  
Swagger UI: http://localhost:8000/docs

### 5. Correr el cliente de demostracion

```bash
# Windows
venv\Scripts\python cliente.py

# Mac / Linux
venv/bin/python cliente.py
```

---

## Endpoints

| Metodo | Ruta                        | Requiere key | Descripcion                              |
|--------|-----------------------------|--------------|------------------------------------------|
| GET    | `/`                         | No           | Health check                             |
| GET    | `/agentes/`                 | No           | Lista todos los agentes                  |
| GET    | `/agente/{nombre}`          | No           | Datos de un agente por nombre            |
| POST   | `/agentes/`                 | Si           | Crea un agente nuevo                     |
| POST   | `/mensajes/`                | No           | Envia un mensaje entre agentes           |
| GET    | `/mensajes/{nombre}`        | No           | Bandeja de entrada de un agente          |
| POST   | `/misiones/`                | Si           | Crea una mision asignada a un agente     |
| GET    | `/misiones/{id}`            | No           | Detalle de una mision por ID             |
| GET    | `/agente/{nombre}/misiones` | No           | Misiones de un agente                    |
| POST   | `/misiones/{id}/completar`  | Si           | Completa la mision y descuenta energia   |
| GET    | `/briefing/{nombre}`        | No           | Perfil del agente + pais de operaciones  |

Los endpoints protegidos requieren el header `X-API-KEY`. Sin el o con clave incorrecta responden `401`.

### Briefing con pais especifico

El endpoint `/briefing/{nombre}` acepta dos parametros opcionales:

```bash
# Buscar por nombre de pais
GET /briefing/Atlas?pais=Colombia

# Buscar por capital
GET /briefing/Atlas?capital=Lima

# Sin parametros: elige un pais de America al azar
GET /briefing/Atlas
```

---

## Decisiones de diseno

**Tabla misiones con columnas extra:** ademas de lo minimo del enunciado, agregue `prioridad`
(alta / media / baja) y `creado_por` para saber urgencia y trazabilidad de cada mision.

**API externa:** use restcountries.com porque encaja con la narrativa de agentes que operan
en paises reales. Es publica y gratuita, sin necesidad de autenticacion.

**Resiliencia:** si la API externa falla o tarda mas de 3 segundos, el briefing igual responde
con los datos locales del agente. Un problema de red nunca rompe el endpoint.
