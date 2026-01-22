def saludar(nombre):
    print("Hola, cómo estás?", nombre)

saludar("José")  

def sumar(a, b):
    print(a + b)


sumar(2, 8)



def lector_precio(producto):
    precio_taza = 3000
    precio_cuaderno = 25000
    percio_timbre = 6000

    if producto == "taza":
        print("el valor a pagar es: ", precio_taza)
    elif producto == "cuaderno":
        print("el valor a pagar es: ", precio_cuaderno)
    elif producto == "timbre":
        print("el valor a pagar es ", percio_timbre)
    else:
        print("el producto no existe")

lector_precio("estuche")




nombre_completo = "Juan Perez"

print(type(nombre_completo))
print(nombre_completo)

numerico = 13

print(type(numerico))

otro_numero = 8.5

print(type(otro_numero))


un_dato = "143"

print(type(un_dato))

nombre = input("Escrive tu nombre: ")

print(nombre)

edad = int(input("Escrive tu edad: "))

print(edad)
print(type(edad))

