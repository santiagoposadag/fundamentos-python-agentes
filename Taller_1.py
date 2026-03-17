# Fase 1: Capa de Seguridad (Login)
# Antes de que el Agente despierte y comience a escuchar comandos, debe verificar quién intenta acceder:

# El sistema debe pedir un usuario y una contraseña por consola.
# Roles: Define en tu código un perfil de invitado (ej. user = "invitado") y un administrador (admin = "admin"), con sus respectivas contraseñas.
# Sistema de Bloqueo: El usuario tiene un máximo de 3 intentos. Si falla 3 veces, el bucle de login se rompe, el programa imprime [Alerta] Usuario bloqueado. Cerrando sistema. y la ejecución termina.
# Si el inicio de sesión es exitoso, el sistema pasa a la Fase 2 y debe recordar con qué rol ingresó el usuario.
# Fase 2: Comandos Base (Repaso de Clase)
# El menú infinito (while) debe mantener los comandos que exploramos en nuestra sesión interactiva:

# ping: Responde con "pong!".
# contar: Pide una frase y cuenta las vocales y consonantes usando un ciclo for.
# salir: Rompe el bucle principal y apaga el Agente de forma elegante.
# Fase 3: Nuevas Herramientas (Tu verdadero reto)
# Debes programar estos 3 comandos nuevos integrándolos a tu estructura if/elif/else del menú principal:

# Comando fecha_hoy (Control de Acceso): * Este comando es clasificado. Si el usuario ingresó como administrador, muestra la fecha actual (Reto Eutagógico: investiga cómo importar el módulo datetime para esto).

# Si ingresó como invitado, imprime: [Acceso Denegado] Este comando requiere privilegios de administrador.
# Comando validar_pass (Manipulación de Strings):

# El agente pedirá al usuario que ingrese una propuesta de contraseña nueva.
# Debes validar dos cosas usando if/else y funciones de strings:
# Que tenga al menos 8 caracteres de longitud (len()).
# Que no sea exactamente igual a su nombre de usuario (para esto necesitas comparar el input con la variable que guardaste en el Login).
# Imprime un mensaje de éxito o el motivo del rechazo.
# Comando calculadora (Casting y Lógica Múltiple):

# El agente pedirá: "Ingresa el primer número", "Ingresa el operador (+, -, *, /)", y "Ingresa el segundo número".
# Debes convertir (int() o float()) los inputs numéricos.
# Usando if/elif/else para evaluar el operador, imprime el resultado de la operación matemática.
# (Opcional/Extra: ¿Qué pasa si intentan dividir por cero? Intenta manejar ese caso con un if).


from datetime import datetime


usuario_invitado="invitado" #aqui se crea el usuario invitado
contraseña_invitado="12345"  #aqui cree la contraseña
usuario_administrador="administrador"  #aqui se cree el usuario administrador
contraseña_administrador="67890"       #aqui cree la contraseña administrador 
intentos=0                             #se inicializa la variable en cero 
rol=None                               #se da valor none por que aun se desconoce cual rol va a ingresar el usuario
while intentos <3:                     # aqui inicia el bucle de intentos y es menor que tres
    usuario=input("ingresa tu usuario: ").strip().lower()  #se solicita el usuario y queda guardado en la variable usuario
    contraseña=input("ingresa tu contraseña: ").strip().lower() #se solicita la contraseña y queda guardado en la variable contraseña
    if usuario == usuario_administrador and contraseña == contraseña_administrador: #se crea la condicional de que los datos sean iguales a los roles de arriba
      rol="administrador"                     #como los datos fueron inguales entonces rol queda como administrador
      print("inicio exitoso bienvenido")      #imprime que fue exitoso
      print(f"tu rol es:{rol}")               #se concatena el rol ´
      break

    elif usuario == usuario_invitado and contraseña == contraseña_invitado: #se crea la condicional de que los datos sean iguales a los roles de arriba
      rol="invitado"                          #como los datos fueron inguales entonces rol queda como invitado
      print("inicio exitoso bienvenido")      #imprime que fue exitoso
      print(f"tu rol es:{rol}")               #se concatena el rol 
      break

    else:                                        #condicional si no
      intentos+=1                              #va sumando 1 la variable intentos
      print("datos incorrectos")               #aqui imprime que es incorrecto
if rol is None:                               # si el rol sigue siendo igual a vacio entonces 
    print("alerta usuario bloqueado. cerrando sistema") #imprime el mensaje bloqueado 
    exit ()                                              #se usa para que finalice el programa directamente
## al realizar este bucle se imprime el menu hasta que sea false
while True:
    print("Home de entrada")            #Imprimir el menu principal
    print("""                           #aqui se imprime el menu
    ping o pong                       
    contar
    fecha
    validarcontraseña
    calculadora
    salir
    """)
    comando = input ("ingresar la solicitud que deseas realizar: ").strip().lower()  #.strip(elimina espacios) y .lower ( para la escritura es con minuscula o mayuscula ejmeplo B o b) son controladores

    if comando == "ping":
        print("pong")
    elif comando == "pong":
        print("ping!")
    elif comando=="contar":
        palabra = input("ingresa una palabra: ").strip().lower()
        totalLetras = len(palabra)       #funcionalidad len es para contar cada letra
        totalvocales = 0
        totalconsonantes = 0
        vocales = "aeiouAEIOU"

        for letra in palabra: 
            if letra.isalpha(): #el metodo isalpha funciona para validar si contiene solo letras sin numero,espacios ni simbolos para retornar un true o false
               if letra in vocales:
                   totalvocales +=1
               else:
                   totalconsonantes +=1

        print(f"su palabra : {palabra} contiene {totalvocales} Vocales y tiene {totalconsonantes} consonantes")
    elif comando== "fecha":
        if rol == "administrador":
              hoy =  datetime.now() #se usa esta funcion para tener la fecha actual
              print("La fecha actual es: " + hoy.strftime("%Y-%m-%d %H:%M:%S")) #se usa strftime para darle formato a la fechaa
        else:
            print ("[Acceso negadp] Este comando necesita permisos de administrador.")
    ## para validar la contraseña se realizan condicionales de validaciones para el cambio de contraseña
    elif comando=="validarcontraseña": 
        nuevacontraseña = input ("Ingrese una nueva contraseña")
        if len(nuevacontraseña)<8:
            print("La contraseña debe contener al menos 8 caracteres")

        elif nuevacontraseña==usuario:
            print("La contraseña no puede ser igual al nombre de usuario")
        else:
            print("contraseña valida")
            ## para validar la calculadora se realizan condicionales de validaciones 
    elif comando == "calculadora":

         num1 = float(input("ingrese el primer numero").strip())
         operador = input("Ingresa el operador (+,-,*,/)").strip()
         num2 = float (input("ingresa el segundo numero: "))

         if operador == "+":
             print("Resultado:",num1+num2)
         elif operador == "-":
            print("Resultado:",num1+num2)
         elif operador == "*":
            print("Resultado:",num1+num2)
         elif operador == "/":   
            if num2 == 0:
                 print("Error,no se puede dividir por cero")
            else:
               print("operador no valido")    
    elif comando == "salir":
               print("Apagando agente....")
               break
    else:
               print("comando no reconocido,digite nuevamente")