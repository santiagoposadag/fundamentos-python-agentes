# Agencia de Agentes 🕶️ - Reto de Consolidación

Este proyecto implementa una central de inteligencia para agentes, desarrollada con **FastAPI**, **SQLite** y siguiendo una **Arquitectura Hexagonal** para asegurar la mantenibilidad y escalabilidad del sistema.

## 🚀 Instalación y Ejecución

Para ejecutar este proyecto correctamente, sigue estos pasos desde la terminal:

1.  **Situarse en la raíz del repositorio e iniciar el ambiente virtual**:
    ```bash
    # Desde fundamentos-python-agentes/
    source .venv/bin/activate
    ```
2.  **Instalar dependencias** (si aún no lo has hecho):
    ```bash
    pip install fastapi uvicorn requests python-dotenv
    ```
3.  **Navegar a la carpeta del proyecto**:
    ```bash
    cd Reto/reto_rodrigo_gallego
    ```
4.  **Configurar entorno**:
    Copia `.env.example` a `.env` y define tu `AGENCIA_API_KEY`.
    ```bash
    cp .env.example .env
    ```
5.  **Iniciar el servidor**:
    ```bash
    uvicorn main:app --reload
    ```
6.  **Ejecutar Demostración**:
    En otra terminal (asegurándote de haber activado el `.venv` y estar en la misma carpeta), ejecuta:
    ```bash
    python cliente.py
    ```

## 🛠️ Justificación de Decisiones de Ingeniería

Para este desarrollo, he tomado las siguientes decisiones clave para asegurar la calidad del proyecto:

### 1. Esquema de la Tabla `misiones`
Más allá de los campos mínimos, se han incluido **claves foráneas estructuradas** y un campo `created_at` en formato ISO. Esto permite una auditoría cronológica precisa y asegura que no se asignen misiones a agentes inexistentes a nivel de base de datos.

### 2. API Pública Elegida: CatFacts/Briefing Intel
Se ha seleccionado una API de curiosidades (CatFacts) para simular el canal de "Inteligencia Externa". Encaja con la narrativa de "Agentes" que necesitan datos externos para sus briefings operativos. La elección se debe a su alta disponibilidad y simplicidad de respuesta JSON.

### 3. Estrategia de Resiliencia
Para el endpoint `/briefing/{nombre}`, se ha implementado un bloque `try-except` con un **timeout de 3.0 segundos**. Si la API externa falla o tarda demasiado, el sistema responde con los datos locales del agente y un mensaje de fallback, asegurando que el servicio principal nunca se vea interrumpido por fallos de terceros.

## 📡 Tabla de Endpoints (Resumen)

| Método | Ruta | Protegido | Descripción |
|---|---|---|---|
| POST | `/agentes/` | Sí | Crea o actualiza un agente. |
| GET | `/agente/{nombre}` | No | Obtiene datos de un agente. |
| POST | `/misiones/` | Sí | Crea una misión nueva. |
| POST | `/misiones/{id}/completar` | Sí | Resta energía y marca éxito. |
| GET | `/briefing/{nombre}` | No | Datos locales + Intel externa. |

---

**Desarrollado por**: Rodrigo Gallego
**Arquitectura**: Hexagonal (Puertos y Adaptadores)
**Enfoque**: Clean Code & POO
