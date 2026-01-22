def nombre_funcion(): # esta es la declaración de una función
    #todo lo de acá es el cuertpo de una función
    print("hola")

nombre_funcion()



def multiplicar(a, b):
    return a * b

resultado = multiplicar(3, 2)

print(resultado)
print(multiplicar(4, 8))


def  bienvenida(nombre):
    print (f"hola {nombre}, que tengas un buen día ")

bienvenida("User")



def pedir_texto(variable):
    return input(variable).strip()


nombre = pedir_texto("Nombre: ")
apellido = pedir_texto("Apellido: ")

print(nombre)
print(apellido)



nombre = "Ariel" #variable de entorno global


def saludar():
    print("hola ", nombre)


def tiempo_conexion():
    tiempo = "23 min" #variable de entorno local
    print(nombre, "Llevas ", tiempo, "conectado")

saludar()
tiempo_conexion()