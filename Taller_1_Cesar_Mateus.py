import datetime ### librería para obtener la fecha actual

usuario_inv="invitado"
usuario_admin = "admin"
pass_inv="12345678"
pass_admin="abcdefgh"
error_sesion=0
sistema_activo = True

### Controla la sesión del usuario, permitiendo 3 intentos para ingresar las credenciales correctas.
while error_sesion <3 and sistema_activo:
    user_sesion= input("Ingrese su usuario: ").lower()
    pass_sesion= input("Ingrese su Contraseña: ")
### Verifica si las credenciales ingresadas corresponden a un usuario invitado o administrador, y otorga acceso al sistema.
    if (user_sesion == usuario_inv and pass_sesion == pass_inv) or (user_sesion == usuario_admin and pass_sesion == pass_admin):
        ### Valida el rol con el que el usuario ingresó
        if user_sesion == usuario_inv:
            print("Acceso concedido como Invitado")
            rol= "Invitado"
        elif user_sesion == usuario_admin:
            print ("Acceso concedido como Administrador")
            rol= "Administrador"
        while sistema_activo:
            ###muestra un menu de opciones disponibles para el usuario.
            cmd = input (
"""Agente> :
* ping
* contar
* fecha_hoy
* validar_pass
* calculadora
* salir \n\n""").lower()
            if cmd == "salir":
                print("■■■■■☻■■■■■  Agente Apagado  ■■■■■☻■■■■■")
                sistema_activo= False
                break
            elif cmd == "ping":
                    print ("pong")
            elif cmd == "contar":
                palabra = input("Ingrese una palabra: ").lower()
                tot_letras = len(palabra)
                tot_vocales= 0
                tot_cons= 0
                for p in palabra:
                    if p in "aeiou":
                        tot_vocales +=1
                    else:
                        tot_cons +=1
                print (f"Palabra ingresada: {palabra}")
                print (f"Total de vocales: {tot_vocales}")
                print (f"Total de consonantes: {tot_cons}")
                print (f"Total de letras: {tot_letras}\n\n")
            ### El comando "fecha_hoy" muestra la fecha y hora actual, pero solo si el usuario tiene rol de administrador.
            elif cmd == "fecha_hoy":
                if rol == "Administrador":
                    fecha_actual= datetime.datetime.now()
                    formato_fecha = fecha_actual.strftime("%d-%m-%Y %H:%M:%S")
                    print (f"La fecha de hoy es: {formato_fecha}\n\n")
                else:
                    print("■■  [Acceso Denegado] Este comando requiere privilegios de administrador.  ■■\n\n")
            ### El comando "validar_pass" permite a los usuarios cambiar su contraseña, despues de confirmar la contraseña actual correctamente y deben cumplir con ciertos criterios para la nueva contraseña.
            elif cmd == "validar_pass":
                if rol == "Administrador":
                    pass_sesion= input("Ingrese su Contraseña actual: ")
                    if pass_sesion == pass_admin:
                        nueva_pass= input("Ingrese su nueva contraseña: ")
                        if len(nueva_pass) < 8:
                            print("La contraseña debe tener al menos 8 caracteres.\n\n")
                        elif nueva_pass == pass_admin:
                            print("La nueva contraseña no puede ser igual a la contraseña actual.\n\n")
                        elif nueva_pass == usuario_admin:
                            print("La contraseña no puede ser igual al nombre de usuario.\n\n")
                        else:
                            pass_admin = nueva_pass
                            print("Contraseña actualizada exitosamente.\n\n")
                    else:
                        print("Contraseña actual incorrecta. No se pudo actualizar la contraseña.\n\n")
                if rol == "Invitado":
                    pass_sesion= input("Ingrese su Contraseña actual: ")
                    if pass_sesion == pass_inv:
                        nueva_pass= input("Ingrese su nueva contraseña: ")
                        if len(nueva_pass) < 8:
                            print("La contraseña debe tener al menos 8 caracteres.\n\n")
                        elif nueva_pass == pass_inv:
                            print("La nueva contraseña no puede ser igual a la contraseña actual.\n\n")
                        elif nueva_pass == usuario_inv:
                            print("La contraseña no puede ser igual al nombre de usuario.\n\n")
                        else:
                            pass_inv = nueva_pass
                            print("Contraseña actualizada exitosamente.\n\n")
                    else:
                        print("Contraseña actual incorrecta. No se pudo actualizar la contraseña.\n\n")
            elif cmd == "calculadora":
                ### Se solicita al usuario ingresar dos numeros y un operador para que el sistema realice la operación correspondiente, manejando casos de división por cero.
                num_1= float(input("Ingrese primer número: "))
                operador= input("Ingresa el operador (+, -, *, /): ")
                num_2= float(input("Ingrese segundo número: "))              
                if operador == "+":
                    res = num_1 + num_2
                    print (f"El resultado de la operación {num_1} {operador} {num_2} es = {res}\n\n")
                elif operador == "-":
                    res = num_1 - num_2
                    print (f"El resultado de la operación {num_1} {operador} {num_2} es = {res}\n\n")
                elif operador == "*":
                    res = num_1 * num_2
                    print (f"El resultado de la operación {num_1} {operador} {num_2} es = {res}\n\n")
                elif operador == "/":
                    if num_2 != 0:
                        res = num_1 / num_2
                        print (f"El resultado de la operación {num_1} {operador} {num_2} es = {res}\n\n")   
                    ### Si el usuario intenta dividir por cero, muestra un mensaje de error en lugar de realizar la operación.    
                    else:
                        print("Error: No es posible dividir por 0\n\n")
                ### Si el operador ingresado no es válido, muestra un mensaje de error.        
                else:
                    print("Operador desconocido.")
                    
            else:
                print("--- Comando desconocido. Intente de nuevo\n\n")
    ### Si las credenciales ingresadas son incorrectas, incrementa el contador de errores y muestra el número de intentos restantes. Si se alcanzan los 3 intentos, bloquea al usuario y cierra el sistema.
    else:
        print ("Usuario y/o contraseña erronea\n\n")
        error_sesion +=1
        intentos = 3 - error_sesion
        if intentos >0:
            print (f"Intentelo de nuevo. Quedan {intentos} intentos \n")
        else:
            print ("■■■■■■    Usuario Bloqueado. Cerrando Sistema     ■■■■■■")