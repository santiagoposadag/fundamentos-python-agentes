## Día 1: Lista y Diccionarios 
## Día 2: Anidaciones - [[],[],[]...], {"a": {1: []}}, [{},{}]

import datetime
print("-----------Iniciando el pseudoagente estilo consola--------------------")

##Login

intentos = 0
rol_actual = ""
tiene_acceso = False

while intentos < 3 and not tiene_acceso:
    usuario = input("Usuario: ").strip().lower()
    password = input("Contraseña: ").strip()
    
    if usuario == "admin" and password == "admin123":
        rol_actual = "admin"
        tiene_acceso = True
        print("[Sistema] Acceso concedido. Privilegios de Administrador activados.")
        
    elif usuario == "invitado" and password == "1234":
        rol_actual = "invitado"
        tiene_acceso = True
        print("[Sistema] Acceso concedido. Modo Invitado.")
        
    else:
        intentos += 1
        print(f"[Error] Credenciales incorrectas. Te quedan {3 - intentos} intentos.")

## Pseudoagente
if tiene_acceso:
    #TO-DO: Agregar una memoria al pseudo agente utilizando listas y diccionarios
    historial_chat=[{'timestamp': '2026-03-18 13:50:51', 'cmd': 'ping', 'rol': 'invitado', 'descripcion': 'Se ha enviado un ping y de respuesta se devolvió un pong.'}, {'timestamp': '2026-03-18 13:50:56', 'cmd': 'fecha_hoy', 'rol': 'invitado', 'descripcion': '[Acceso Denegado] Este comando requiere privilegios de administrador.'}, {'timestamp': '2026-03-18 13:51:02', 'cmd': 'dormir', 'rol': 'invitado', 'descripcion': 'Comando no existe. Intente de nuevo'}, {'timestamp': '2026-03-18 13:51:07', 'cmd': 'salir', 'rol': 'invitado', 'descripcion': 'Se ha solicitado terminar la sesión.'}] 
    pseudo_activo = True
    mensaje = ""

    while pseudo_activo:
        cmd = input(f"\n{usuario}@PseudoAgente>: ").strip().lower() 


        if cmd == "salir":
            print("[PseudoAgente] Apagando sistemas...")
            pseudo_activo = False
            mensaje = "Se ha solicitado terminar la sesión."
        elif cmd == "ping":
            print("pong~")
            mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
        elif cmd == "contar":
            pal = input("Ingrese una palabra: ").strip().lower()
            tot_letras = len(pal)
            tot_vocales = 0
            tot_cons = 0
            for p in pal:
                if p in "aeiou":
                    tot_vocales += 1
                elif p.isalpha(): 
                    tot_cons += 1                    
            print(f"Palabra ingresada: {pal}")
            print(f"Total de vocales: {tot_vocales}")
            print(f"Total de consonantes: {tot_cons}")
            print(f"Total de letras: {tot_letras}")
            mensaje = f"""Se solicitó el conteo de la palabra {pal}, dando como resultados:\nVocales: {tot_vocales}\nConsonantes: {tot_cons}\nTotal: {tot_letras}"""
        elif cmd == "fecha_hoy":
            if rol_actual == "admin":
                ahora = datetime.datetime.now()
                mensaje = f"[PseudoAgente] La fecha y hora actual es: {ahora.strftime('%Y-%m-%d %H:%M:%S')}"
                print(mensaje)
            else:
                mensaje = "[Acceso Denegado] Este comando requiere privilegios de administrador."
                print(mensaje)
        elif cmd == "validar_pass":
            print("Validar pass")
            mensaje = ""
        elif cmd == "calculadora":
            print("Calculadora")
            mensaje = ""
        elif cmd.split()[0] == "historial":
            # Regla de auditoría: Uso split() para manejar comandos con argumentos (all, clear)
            partes = cmd.split()
            if len(partes) > 1:
                if partes[1] == "all":
                    print("\n--- HISTORIAL COMPLETO ---")
                    if len(historial_chat) == 0:
                        print("[PseudoAgente] El historial está vacío.")
                    else:
                        for i, h in enumerate(historial_chat, 1):
                            print(f"#{i} | {h['timestamp']} | {h['rol']} | {h['cmd']}\n   {h['descripcion']}\n")
                    mensaje = "Se mostró el historial completo."
                elif partes[1] == "clear":
                    historial_chat.clear()
                    print("[PseudoAgente] Historial eliminado correctamente.")
                    mensaje = "Se eliminó el historial."
                else:
                    print("[PseudoAgente] Opción de historial no reconocida.")
                    mensaje = "Opción de historial no reconocida."
            else:
                palabra = input("Ingresa la palabra clave a buscar: ").strip().lower()
                coincidencias = []
                for h in historial_chat:
                    # Regla de auditoría:
                    # Para saber si una palabra está dentro de otra en Python, uso 'in' y convierto ambos a minúsculas con .lower().
                    # Así la búsqueda es insensible a mayúsculas/minúsculas.
                    if palabra in h["descripcion"].lower():
                        coincidencias.append(h)
                if coincidencias:
                    print(f"\n--- RESULTADOS DE BÚSQUEDA PARA '{palabra}' ---")
                    for i, h in enumerate(coincidencias, 1):
                        print(f"#{i} | {h['timestamp']} | {h['rol']} | {h['cmd']}\n   {h['descripcion']}\n")
                    mensaje = f"Se encontraron {len(coincidencias)} coincidencias para '{palabra}'."
                else:
                    print("[PseudoAgente] No encontré registros que coincidan con esa palabra.")
                    mensaje = f"No se encontraron coincidencias para '{palabra}'."
        else:
            mensaje = "Comando no existe. Intente de nuevo"
            print(mensaje)
        #TO-DO: Taller de la semana - Búsqueda de memoria
        d_log = {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "cmd": cmd,
                "rol": rol_actual,
                "descripcion": mensaje}
        historial_chat.append(d_log)

else:
    print("Acceso denegado.")
