# Taller Semana 5: Persistencia y APIs

**Fecha limite de entrega:** Lunes 13 abril, 2026, 23h59.

**Forma de entrega:** Pull-Request a la rama `semana_5` desde sus repositorios forkeados.

## Contexto

En la Semana 5 dimos dos pasos fundamentales para convertir nuestro agente en un sistema real. En la **Sesion 1** aprendimos a persistir datos usando **SQLite**, de forma que la informacion de nuestros agentes y sus mensajes sobrevive entre ejecuciones del programa. En la **Sesion 2** expusimos nuestro agente al mundo exterior creando un **servidor HTTP con FastAPI** y aprendimos a consumirlo programaticamente con un **cliente HTTP**.

## Instrucciones

1. Descomenta **TODOS** los capitulos en `S5_sesion_1.py` y ejecuta cada uno.
2. Descomenta **TODOS** los capitulos en `S5_sesion_2.py`.
3. Ejecuta el servidor:
   ```bash
   uvicorn S5_sesion_2:app --reload
   ```
4. Descomenta y ejecuta `S5_cliente.py` en una terminal aparte.
5. Escribe tus conclusiones en cada bloque `# CONCLUSION:`.

## Entregables

1. `S5_sesion_1.py` con todos los capitulos descomentados y funcionando.
2. `S5_sesion_2.py` con todos los endpoints descomentados y funcionando.
3. `S5_cliente.py` con las funciones cliente descomentadas y funcionando.
4. `agentes.db` con al menos 3 agentes y 5 mensajes.
5. Comentarios con conclusiones propias en cada bloque `# CONCLUSION:`.

## Criterios de Evaluacion

- El servidor levanta sin errores.
- Los endpoints responden correctamente desde Swagger UI (`http://localhost:8000/docs`).
- El cliente HTTP se comunica exitosamente con el servidor.
- Los datos persisten entre reinicios del servidor.
- Las conclusiones demuestran comprension de los conceptos.

## Desafio Extra (Opcional)

- Crear un nuevo endpoint `GET /agente/{nombre}/mensajes` que retorne los mensajes **enviados** por un agente (no los recibidos).
- Agregar un campo `leido` (bool) a la tabla `mensajes` y un endpoint para marcar mensajes como leidos.
