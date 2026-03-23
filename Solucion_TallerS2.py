# Solución de taller S2 

#Carlos Arturo Ramirez Londoño
#carlos.ramirezl@sofka.com.co

from datetime import datetime


roles = ["invitado","admin"]  # Se crea una lista con el fin de agrupar eficientemente los dos perfiles de usaurios
contrasenias = ["123thonpy","py456thon"] # Se hace lo mismo para la contraeñas teniendo en cuenta que su posición en las listas corresponde a su respectivo perfil

login_usuario = True # Bandera para el ciclo de validación del usuario y controladora de seguridad
intentos = 0         # variable que lleva el conteo de los intentos fallidos
max_intentos = 3     # Número máximo de intentos permitidos
while login_usuario:

    usuario = input("Ingrese el rol de usuario (invitado/admin): ").lower()   # Se solicita un usuario de entrada de acuerdo a los dos tipos permitidos invitado/admin   
    if usuario in roles:     # Se valida si el usuario ingresado se encuentra en la lista de roles  
        login_contrasenia = True     # Si se encuentra entonces asignamos una bandera para el ciclo de validación de contraseña
        while login_contrasenia:     
            rol = roles.index(usuario)    # Mediante la función index() se obtiene el indice correspondiente de la lista del usuario ingresado. Como solo hay 2 elementos, entonces solo puede arrojar 0 o 1 
            contrasenia = input("Ingrese la contraseña: ")   # Se solicita la contraseña de entrada
            if contrasenia == contrasenias[rol]:    # Se valida la contraseña ingresada comparándola con la contraseña correspondiente al rol del usuario ingresado (usando el mismo indice obtenido anteriormente)
                print(f"Bienvenido, {usuario}. Acceso concedido.\n")  # Una vez ingresado se ejecuta la fase 2 del taller el cual ya se vio previamente en clase
                
                print("----- Iniciando el pseudoagente estilo consola -----")
                sistema_activo = True
                historial_chat=[]
                mensaje = ""
                while sistema_activo:
                    cmd = input("Agente>: ").strip().lower().split() # Se pone doble split, el primero para borrar espacios internos, el segundo para espacios externos de forma que si se manda un comando compuesto, entonces los separe en una lista y se puede validar cada uno por separado
                    
                    if cmd[0] == "salir":  # Para el comando de salir, se hace un ligero ajuste agregando el cambio de las banderas de todos los ciclos a falso para asegurar el apagado de todo el sístema
                        print("-----Agente apagado. Vuelve pronto. -----")
                        sistema_activo = False                              
                        login_contrasenia = False
                        login_usuario = False
                        mensaje = "Se ha solicitado terminar la sesión."
                    elif cmd[0] == "ping":
                        print("pong.")
                        mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
                    elif cmd[0] == "contar":
                        palabra = input("Ingrese una palabra: ").lower()
                        tot_letras = len(palabra)
                        tot_vocales = 0
                        tot_cons = 0
                        
                        for p in palabra:
                            if p in "aeiou":
                                tot_vocales += 1
                            else:
                                tot_cons += 1

                        print(f"Palabra ingresada: {palabra}")
                        print(f"Total de letras: {tot_letras}")
                        print(f"Total de vocales: {tot_vocales}")
                        print(f"Total de consonantes: {tot_cons}")
                        mensaje = f"""Se solicitó el conteo de la palabra {palabra}, dando como resultados:
                        Vocales: {tot_vocales}
                        Consonantes: {tot_cons}
                        Total: {tot_letras}"""
                    elif cmd[0] == "fecha_hoy":    # Como se solicita en el taller, se hace inicialmente la importación de la librería datetime la inicio del código
                        if usuario == "admin":  # Posteriormente se compara si el usuario ingresado corresponde al de admin para el uso de la funcionalidad de fecha_hoy 
                            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Una vez obtenida la fecha se formatea para que se muestre de manera correcta 
                            mensaje = f"Fecha y hora actual: {fecha_actual}"
                            print(mensaje)
                        else:
                            mensaje = "[Acceso Denegado] Este comando requiere privilegios de administrador."
                            print(mensaje)
                    elif cmd[0] == "validar_pass":
                        nueva_contrasenia = input("Ingrese una nueva contraseña: ")  # Se solicita la nueva contraseña
                        if len(nueva_contrasenia) < 8:    # Se valida con la función len() que el tamaño si corresponde al minimo de 8 requerido    
                            mensaje = "Contraseña demasiado corta. Debe tener al menos 8 caracteres."
                            print(mensaje)
                        elif nueva_contrasenia == usuario: # Se valida que la nueva contraseña ingresada no sea igual al nombre de usuario
                            mensaje = "Contraseña no puede ser igual al nombre de usuario."
                            print(mensaje)
                        else:
                            mensaje = "Contraseña válida."
                            print(mensaje)
                    elif cmd[0] == "calculadora":   # Para la calculadora se asume mejor los numeros como flotantes debido que en el caso de divisiones si se toman enteros y la división no es exacta, entonces el resultado se tomará como la parte entera de la división, lo cual no es correcto.
                        num1 = float(input("Ingresa el primer número: ")) 
                        operador = input("Ingresa el operador (+, -, *, /): ")
                        num2 = float(input("Ingresa el segundo número: "))
                        if operador == "+":
                            resultado = num1 + num2
                        elif operador == "-":
                            resultado = num1 - num2
                        elif operador == "*":
                            resultado = num1 * num2
                        elif operador == "/":
                            if num2 != 0:  # Se valida que el segundo número no sea cero para evitar el error de división por cero
                                resultado = num1 / num2
                            else:
                                mensaje = "Error: no se puede dividir por cero."
                                print(mensaje)
                                continue # Si se ingresa una división por cero, se muestra un mensaje de error y se utiliza continue para saltar a la siguiente iteración del ciclo sin intentar realizar la operación inválida
                        else:
                            mensaje = "Operador no válido." # Si el operador ingresado no corresponde a ninguno de los permitidos, se muestra un mensaje de error 
                            print(mensaje)
                            continue # Se utiliza continue para saltar a la siguiente iteración del ciclo sin intentar realizar una operación con un operador inválido
                        mensaje = f"Resultado: {resultado}"
                        print(mensaje)
                    elif cmd[0] == "historial": # Como el comando historial tiene 3 variantes, entonces se valida si el primer elemento de la lista del comando es historial, si lo es, entonces se procede a validar los siquientes elementos de la lista cmd en busca de la palabra all o clear
                        if len(historial_chat) == 0:   # Se valida inicialmente si el historial de comandos está vacío, para evitar mostrar un historial vacío o intentar hacer búsquedas en un historial sin registros, lo cual no tendría sentido y puede crashear el programa
                            print("[Pseudoagente] No hay registros en el historial.")
                            continue
                        if len(cmd)>1 and cmd[1] == "all":
                            print("-----Historial completo de comandos -----")
                            for log in historial_chat:  # Se muestra el historial completo de comandos ingresados durante la sesión
                                print(log)   
                        elif len(cmd)>1 and cmd[1] == "clear":
                            historial_chat.clear()  # Se borra todo el historial de comandos utilizando el método clear() de la lista
                            mensaje = "Historial de comandos borrado."
                            print(mensaje)
                        else:
                            clave = input("Ingrese la palabra clave a buscar: ").lower()  # Se solicita una palabra clave para filtrar el historial 
                            coincidencias = 0
                            for log in historial_chat:  # Se recorre el historial completo 
                                if clave in log["descripcion"].lower():  # Si la palabra clave se encuentra en la descripción asociada al historial, entonces se muestra ese registro, para esto la expresión "in" sirve para validar si la clave se encuentra dentro del campo descrioción
                                    coincidencias += 1
                                    print(log)
                            print(f"Coincidencias encontradas: {coincidencias}")    
                            if coincidencias == 0:
                                print("[Pseudoagente] No encontré registros que coincidan con esa palabra.")
                    else:
                        mensaje = "-----Comando desconocido. Intente de nuevo. -----"
                        print(mensaje)
                    d_log = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "cmd": cmd,
                    "rol": usuario,
                    "descripcion": mensaje}
                    historial_chat.append(d_log)
            else:
                print("Contraseña incorrecta. Intente de nuevo.") # Si la contraseña ingresada es incorrecta, se muestra un mensaje de error
                intentos += 1 # Se incrementa el contador de intentos fallidos cada vez que se ingresa una contraseña incorrecta
            if intentos >= max_intentos:   # Si el número de intentos fallidos alcanza o supera el máximo permitido, se cambian las banderas de los ciclos a falso para bloquear el usuario y cerrar el sistema 
                login_contrasenia = False
        login_usuario = False
    else:
        print("Usuario no reconocido. Intente de nuevo.")   # Si el usuario ingresado no se encuentra en la lista de roles, se muestra un mensaje de error
        intentos += 1    # Se incrementa el contador de intentos fallidos cada vez que se ingresa un usuario no reconocido
    if intentos >= max_intentos:  
        print("[Alerta] Usuario bloqueado. Cerrando sistema.") # Si el número de intentos fallidos alcanza o supera el máximo permitido, se muestra un mensaje de alerta indicando que el usuario ha sido bloqueado y se cambia la bandera de login_usuario a falso para cerrar el sistema
        login_usuario = False

