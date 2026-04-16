# Semana 5: Persistencia con SQLite y APIs con FastAPI

## Contexto

Curso "Fundamentos de Python para Ingenieria de Agentes", Semana 5. Dos sesiones de 1 hora cada una. Los estudiantes ya dominan: tipos primitivos, estructuras de datos, funciones tipadas, clases/herencia, y modularizacion (Semanas 1-4).

Esta semana se desvincula del PseudoAgente existente y crea una practica nueva centrada en un sistema multi-agente con persistencia real y comunicacion por API.

## Enfoque pedagogico

**Aprendizaje guiado paso a paso en un archivo unico por sesion.**

Cada archivo Python contiene capitulos numerados. Cada capitulo sigue el ciclo:
1. Concepto explicado en comentarios
2. Codigo comentado para descomentar y ejecutar
3. Bloque `# PRUEBA:` con experimentos sugeridos
4. Bloque `# CONCLUSION:` para que el alumno escriba lo que observo

Los alumnos no escriben desde cero; descomentan, prueban, modifican y sacan conclusiones.

## Estructura de archivos

```
S5/
  S5_sesion_1.py          # Persistencia con SQLite
  S5_sesion_2.py          # APIs con FastAPI
  Taller_Semana_5.md      # Enunciado del taller/practica
```

Ambas sesiones comparten el archivo `agentes.db` (SQLite) que se genera en la Sesion 1 y se reutiliza en la Sesion 2.

---

## Sesion 1 — Persistencia con SQLite (60 min)

**Narrativa:** "Tus agentes viven en RAM y mueren al cerrar la terminal. Hoy les damos un hogar permanente en una base de datos."

### Capitulo 1: El problema de la amnesia (5 min)

- Crear un dict representando un agente con nombre, rol y energia
- Imprimirlo, "terminar" el bloque
- Pregunta al alumno: donde quedo ese agente?
- **Concepto:** Variables viven en RAM, RAM es temporal

### Capitulo 2: SQL en 5 minutos (10 min)

- `import sqlite3` (viene con Python, cero instalacion)
- `sqlite3.connect("agentes.db")` — crea el archivo de base de datos
- `cursor.execute("CREATE TABLE IF NOT EXISTS agentes (...)")`
- Tabla `agentes`: columnas `nombre TEXT PRIMARY KEY, rol TEXT, energia INTEGER`
- Analogia: tabla = hoja de Excel, fila = registro, columna = campo
- `conn.commit()` — confirmar cambios
- `conn.close()` — cerrar conexion
- **PRUEBA:** Verificar que el archivo `agentes.db` aparece en el directorio

### Capitulo 3: Registrar un agente (10 min)

- Funcion `registrar_agente(nombre: str, rol: str, energia: int) -> str`
- `INSERT INTO agentes VALUES (?, ?, ?)` con parametros (prevencion SQL injection)
- `try/except sqlite3.IntegrityError` para nombre duplicado
- Registrar 2-3 agentes diferentes
- **PRUEBA:** Intentar registrar el mismo nombre dos veces. Que pasa?

### Capitulo 4: Despertar un agente (10 min)

- Funcion `despertar_agente(nombre: str) -> dict | None`
- `SELECT * FROM agentes WHERE nombre = ?`
- `cursor.fetchone()` retorna tupla o None
- Convertir tupla a dict para manejarlo como Python puro
- **Momento "wow":** Cerrar Python completamente, volver a abrir, ejecutar `despertar_agente()` — el agente sigue ahi
- **PRUEBA:** Despertar un agente que no existe. Que retorna?

### Capitulo 5: La tabla de mensajes (10 min)

- Segunda tabla: `mensajes(id INTEGER PRIMARY KEY AUTOINCREMENT, remitente TEXT, destinatario TEXT, contenido TEXT, timestamp TEXT)`
- Funcion `enviar_mensaje(remitente: str, destinatario: str, contenido: str) -> str`
- Usa `datetime.now().isoformat()` para timestamp automatico
- **PRUEBA:** Enviar 3 mensajes entre agentes diferentes

### Capitulo 6: Bandeja de entrada (10 min)

- Funcion `leer_mensajes(nombre_agente: str) -> list[dict]`
- `SELECT * FROM mensajes WHERE destinatario = ? ORDER BY timestamp`
- Retorna lista de dicts con los mensajes
- **PRUEBA:** Crear un tercer agente, enviarle mensajes desde dos agentes distintos, leer su bandeja

### Capitulo 7: Experimentacion libre (5 min)

- Desafio abierto: crear multiples agentes, mensajes cruzados
- Verificar que todo persiste cerrando y reabriendo Python
- Espacio para `# CONCLUSION:` del alumno

### Resultado de la sesion

- Archivo `agentes.db` con tablas `agentes` y `mensajes`
- 4 funciones utilitarias: `registrar_agente`, `despertar_agente`, `enviar_mensaje`, `leer_mensajes`
- Evidencia tangible de persistencia entre ejecuciones

---

## Sesion 2 — APIs con FastAPI (60 min)

**Narrativa:** "Tus agentes se comunican dejandose notas en la base de datos. Hoy les damos telefono: van a hablar en tiempo real por HTTP."

**Prerequisitos:** `pip install fastapi uvicorn requests`

### Capitulo 1: La analogia del restaurante (5 min)

- Cliente = tu (la mesa), Servidor = la cocina, HTTP = el mesero, API = el menu
- Codigos de estado: 200 OK, 404 No encontrado, 422 Datos invalidos
- **Concepto:** Una API es un contrato: "si me pides X con estos datos, te respondo Y"

### Capitulo 2: Instalacion y verificacion (5 min)

- `pip install fastapi uvicorn requests`
- Verificar con `import fastapi; import uvicorn; import requests`
- Explicar cada paquete: fastapi (el framework), uvicorn (el servidor), requests (el cliente)

### Capitulo 3: Mi primer endpoint (10 min)

- Crear app basica: `app = FastAPI()`
- `@app.get("/")` que retorna `{"status": "online", "mensaje": "Bienvenido al sistema de agentes"}`
- Ejecutar con `uvicorn S5_sesion_2:app --reload`
- Abrir navegador en `http://localhost:8000/docs` — Swagger UI automatica
- **Momento "wow":** el navegador muestra documentacion interactiva sin escribir una linea de HTML
- **PRUEBA:** Cambiar el mensaje, guardar, ver que `--reload` lo actualiza automaticamente

### Capitulo 4: GET con parametros — consultar agentes (10 min)

- `@app.get("/agente/{nombre}")` que consulta SQLite con `despertar_agente()` de la Sesion 1
- Importar/reutilizar las funciones de persistencia de la Sesion 1
- Si el agente existe: retorna el dict. Si no: `HTTPException(status_code=404)`
- Probar desde Swagger UI con nombres que existen y que no
- **PRUEBA:** Crear un endpoint `GET /agentes/` que retorne la lista de todos los agentes

### Capitulo 5: POST — recibir datos (10 min)

- Modelo Pydantic basico:
  ```python
  class MensajeRequest(BaseModel):
      remitente: str
      destinatario: str
      contenido: str
  ```
- `@app.post("/mensajes/")` que recibe el modelo y usa `enviar_mensaje()` de la Sesion 1
- Probar desde Swagger UI: llenar el formulario, enviar, verificar en la BD
- **PRUEBA:** Crear un endpoint `POST /agentes/` para registrar nuevos agentes

### Capitulo 6: El agente como cliente HTTP (10 min)

- Funcion `enviar_mensaje_http(remitente: str, destinatario: str, contenido: str) -> dict`
- Usa `requests.post("http://localhost:8000/mensajes/", json={...})`
- Verificar `response.status_code` y `response.json()`
- Funcion `consultar_agente_http(nombre: str) -> dict`
- Usa `requests.get(f"http://localhost:8000/agente/{nombre}")`
- **Concepto clave:** Ahora el agente habla por HTTP, no por llamada directa a funcion. Es el mismo resultado, pero ahora podria estar en otra maquina
- **PRUEBA:** Enviar un mensaje via HTTP y luego leer la bandeja directamente desde SQLite. El mensaje aparece?

### Capitulo 7: El circuito completo (10 min)

- Script que:
  1. Registra un agente via POST
  2. Envia un mensaje via POST
  3. Consulta la bandeja via GET
  4. Imprime el resultado
- Todo desde codigo Python, todo pasando por HTTP
- **PRUEBA:** Hacer lo mismo desde Swagger UI en el navegador
- Espacio para `# CONCLUSION:` del alumno

### Resultado de la sesion

- Servidor FastAPI con 4+ endpoints funcionales
- Modelos Pydantic para validacion automatica
- Swagger UI como herramienta de testing
- Funciones cliente que usan `requests` para comunicarse con el API
- El mismo `agentes.db` de la Sesion 1 ahora accesible por HTTP

---

## Conexion entre sesiones

```
Sesion 1 (Persistencia)              Sesion 2 (APIs)
========================             ========================
registrar_agente()  ──────────────►  POST /agentes/
despertar_agente()  ──────────────►  GET  /agente/{nombre}
enviar_mensaje()    ──────────────►  POST /mensajes/
leer_mensajes()     ──────────────►  GET  /mensajes/{nombre}
                                          |
agentes.db ◄──── SQLite ────────────► FastAPI lee/escribe
  ├─ tabla agentes                        |
  └─ tabla mensajes                  requests.post() / .get()
                                     (agente como cliente HTTP)
```

## Decisiones de diseno

- **SQLite sobre JSON files:** Ensenar SQL transferible a cualquier BD real. Cero instalacion.
- **FastAPI sobre Django:** 5 lineas vs 30+ para un endpoint. Swagger gratis. Type hints que ya conocen.
- **Funciones sueltas sobre clases:** En esta semana el foco es persistencia y APIs, no OOP. Las funciones de la Sesion 1 se reutilizan directamente en la Sesion 2.
- **Mismo archivo DB compartido:** La Sesion 2 no empieza de cero; amplifica lo construido en la Sesion 1.
- **Pydantic solo lo basico:** Un modelo con 3 campos. No herencia de modelos, no validadores custom, no configuracion avanzada.

## Riesgos y mitigaciones

| Riesgo | Mitigacion |
|--------|-----------|
| `pip install` falla | Preparar instrucciones para venv y pip upgrade |
| Puerto 8000 ocupado | Documentar `--port 8001` como alternativa |
| SQLite locked (multiples conexiones) | Cada funcion abre y cierra su propia conexion |
| Alumnos se adelantan | Los bloques comentados evitan spoilers; cada capitulo depende del anterior |
| Swagger UI confunde | Guiar paso a paso: "click Try it out → llena los campos → click Execute" |
