# 🏛️ La Agencia de Agentes - Proyecto de Consolidación

Este proyecto integra persistencia, APIs web, seguridad y consumo de servicios externos para gestionar una agencia de agentes autónomos.

## 🛠️ Instalación y Ejecución

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configurar entorno:**
   Copia el archivo `.env.example` a `.env` y ajusta los valores si es necesario.
   ```bash
   cp .env.example .env
   ```
3. **Iniciar el servidor:**
   Desde la carpeta `Reto`, ejecuta el siguiente comando para usar el entorno virtual:
   ```powershell
   uvicorn main:app --reload
   ```
4. **Ejecutar el cliente de demostración:**
   En otra terminal, corre:
   ```bash
   cd Reto
   python cliente.py
   ```

## 🛤️ Endpoints Documentados

| Método | Ruta | Protegido | Descripción |
|---|---|---|---|
| `GET` | `/` | No | Estado del servidor. |
| `POST` | `/agentes/` | Sí | Registra un nuevo agente. |
| `GET` | `/agente/{nombre}` | No | Obtiene datos de un agente. |
| `GET` | `/agentes/` | No | Lista todos los agentes. |
| `POST` | `/mensajes/` | Sí | Envía un mensaje entre agentes. |
| `GET` | `/mensajes/{nombre}` | No | Lee la bandeja de entrada de un agente. |
| `POST` | `/misiones/` | Sí | Crea una misión asignada. |
| `GET` | `/misiones/{id}` | No | Obtiene detalles de una misión. |
| `GET` | `/agente/{nombre}/misiones` | No | Lista misiones de un agente. |
| `POST` | `/misiones/{id}/completar` | Sí | Marca misión como completada y descuenta energía. |
| `GET` | `/briefing/{nombre}` | No | Datos del agente + Inteligencia externa (API). |

## 🧭 Decisiones de Ingeniería

1. **Esquema de la tabla `misiones`:**
   Se añadió la columna `prioridad` (TEXT). Esta decisión se tomó para permitir que la agencia clasifique las tareas por urgencia, lo cual es fundamental para una gestión operativa realista. Además, se incluyó `created_at` para auditoría temporal.

2. **API pública elegida:**
   Se utilizó `https://catfact.ninja/fact`. Elegí esta API porque ofrece hechos ligeros en formato JSON que sirven como "curiosidades" o "datos de distracción" en el briefing del agente, dándole una narrativa menos rígida y más "viva" al sistema.

3. **Estrategia de resiliencia:**
   Se implementó un `timeout` de 5 segundos en la petición a la API externa y un bloque `try/except`. Si la API falla o tarda demasiado, el servidor responde con un mensaje de fallback ("Información externa no disponible") en lugar de fallar, garantizando que los datos locales del agente siempre sean accesibles.

## 📚 Referencias consultadas
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic v2 Models](https://docs.pydantic.dev/latest/)
- [Python Logging Module](https://docs.python.org/3/library/logging.html)
- [Requests Library](https://requests.readthedocs.io/en/latest/)
- [SQLite3 Python Module](https://docs.python.org/3/library/sqlite3.html)
