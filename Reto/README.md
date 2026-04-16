# 🕵️‍♂️ Proyecto: La Agencia de Agentes - Sistema de Inteligencia Central

Este sistema es una API desarrollada con **FastAPI** para la gestión de agentes, misiones y comunicaciones. El proyecto integra persistencia de datos en **SQLite**, seguridad mediante **API Key**, y una arquitectura orientada a objetos que aplica **Polimorfismo** para la gestión de recursos.

---

## 🚀 Guía de Instalación y Uso

### 1. Requisitos Previos
- Python 3.10 o superior.

### 2. Instalación de Dependencias
Abre la terminal en la carpeta del proyecto y ejecuta:
`pip install fastapi uvicorn requests python-dotenv`

### 3. Configuración del Entorno
1. Localiza el archivo `.env.example`.
2. Crea una copia y renómbrala a `.env`.
3. Configura las siguientes variables en el archivo `.env`:
   - AGENCIA_API_KEY=agencia-secreta-2024
   - EXTERNAL_API_URL=https://catfact.ninja/fact

### 4. Ejecución del Servidor
Inicia la API con el siguiente comando:
`uvicorn main:app --reload`

---

## 🛠️ Decisiones de Ingeniería (Justificación)

* **Gestión de Energía mediante Polimorfismo (R2):** Se diseñó una estructura de clases donde `AgenteAdmin` hereda de `PseudoAgente`. Al sobrescribir el método `gastar_energia`, el sistema permite que el administrador gaste solo el 50% de la energía requerida por una misión.

* **Patrón Factory para Persistencia de Objetos:** Se implementó la función `despertar_agente_clase` en el módulo de base de datos. Esta función actúa como una fábrica que reconstruye objetos complejos de Python a partir de registros planos de SQLite.

* **Resiliencia ante Fallos de API Externa (5.2):** Para el endpoint de briefing, se integró un **Plan de Contingencia** usando un `timeout` de 2 segundos y un bloque `try/except` para manejar posibles caídas de la API de CatFacts.

---

## 📡 Documentación de Endpoints

| Método | Endpoint | Descripción | Requiere API Key |
| :--- | :--- | :--- | :---: |
| GET | / | Inicio del sistema. | No |
| GET | /agentes/ | Lista todos los agentes registrados. | No |
| POST | /agentes/ | Registra un nuevo agente. | **Sí** |
| POST | /misiones/ | Crea y asigna misiones (R3). | **Sí** |
| POST | /misiones/{id}/completar | Completa misión y actualiza energía (R4). | **Sí** |
| GET | /briefing/{nombre} | Datos locales + API Externa (R5.2). | No |

---

## 📚 Referencias Consultadas

* [Repositorio de FastAPI y Guía de FastAPI](https://github.com/fastapi/fastapi): Creación de endpoints y manejo de parámetros de ruta
* [Introducción a la Seguridad en FastAPI](https://mintlify.wiki/fastapi/fastapi/tutorial/security/security-intro): Implementar la protección de rutas mediante encabezados
* [SQLite3 en Python (Docs Oficiales)](https://docs.python.org/3/library/sqlite3.html): Persistencia de datos y manejo de cursores
* [Real Python - Python Classes and Inheritance](https://realpython.com/inheritance-composition-python/): Consultada para la implementación de Herencia y Polimorfismo en las clases de Agentes.
* [Requests Library Guide](https://requests.readthedocs.io/en/latest/): Utilizada para la integración con la API externa de CatFacts.

---

## 📦 Contenido del Entregable
- main.py, db.py, agente.py, config.py, cliente.py, semillas.py y agentes.db.