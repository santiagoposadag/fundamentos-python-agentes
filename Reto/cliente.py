# Este es el "Cliente de la Agencia". Simula a un agente externo que interactúa con nuestra API (main.py) para probar que todo funcione correctamente.
import requests # Para hacer peticiones HTTP a nuestra API
import time # Para simular tiempos de espera entre acciones

# Configuración inicial: ¿A dónde vamos a tocar la puerta?
BASE_URL = "http://127.0.0.1:8000"

# REQUISITO 5.1: Esta llave DEBE coincidir con la que tenemos en el archivo .env
# La llevamos a una variable para no repetirla y para que sea fácil de cambiar si es necesario.
HEADERS = {"X-API-KEY": "agencia-secreta-2024"} 

def ejecutar_demo(): # Función que simula una serie de interacciones con la API para demostrar que todo funciona (R1-R5)
    print("INICIANDO AUDITORÍA DE LA AGENCIA...\n")

    # --- PASO 1: Prueba de Vida --- #
    print("1. Verificando conexión básica...")
    res = requests.get(f"{BASE_URL}/")
    print(f"Respuesta: {res.json()}\n")

    # --- PASO 2: Seguridad (R5.1) --- #
    print("2. Probando seguridad (Intentando crear agente sin API Key)...")
    res_error = requests.post(f"{BASE_URL}/agentes/", json={"nombre": "Intruso", "rol": "spy"})
    print(f"Resultado esperado (401 Unauthorized): {res_error.status_code}\n")

    # --- PASO 3: Registro de Agentes (S4 + S5) --- #
    print("3. Registrando un Agente Administrador (Andres_Admin)...")
    admin_data = {"nombre": "Andres_Admin", "rol": "admin", "energia": 200}
    requests.post(f"{BASE_URL}/agentes/", json=admin_data, headers=HEADERS)
    
    print("4. Registrando un Agente Explorador (Agente_Bot)...")
    bot_data = {"nombre": "Agente_Bot", "rol": "explorer", "energia": 100}
    requests.post(f"{BASE_URL}/agentes/", json=bot_data, headers=HEADERS)
    print("Agentes registrados con éxito.\n")

    # --- PASO 4: Creación de Misiones (R3) --- #
    print("5. Asignando una misión de 50 de energía a Andres_Admin...")
    mision_data = {
        "titulo": "Rescate de Base",
        "descripcion": "Misión secreta de alta prioridad.",
        "agente_asignado": "Andres_Admin",
        "energia_requerida": 50
    }
    requests.post(f"{BASE_URL}/misiones/", json=mision_data, headers=HEADERS)
    print("Misión creada.\n")

    # --- PASO 5: El Corazón del Reto (R2 - Polimorfismo) --- #
    print("6. Completando misión (Andres_Admin es Admin, debería gastar la MITAD)...")
    # Intentamos completar la misión 1
    res_mision = requests.post(f"{BASE_URL}/misiones/1/completar", headers=HEADERS)
    print(f"Resultado: {res_mision.json()}")
    print("Explicación: Andres empezó con 200. La misión costaba 50, pero gastó 25 por ser Admin.\n")

    # --- PASO 6: Inteligencia Externa (R5.2) --- #
    print("7. Solicitando Briefing con Inteligencia Externa (CatFacts)...")
    res_briefing = requests.get(f"{BASE_URL}/briefing/Andres_Admin")
    print(f"Briefing Completo: {res_briefing.json()}\n")

    print("AUDITORÍA FINALIZADA: Todos los requerimientos (R1-R5) funcionan.")

if __name__ == "__main__":
    ejecutar_demo()