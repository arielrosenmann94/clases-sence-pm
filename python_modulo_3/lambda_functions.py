'''n = "Ariel"

def bienvenida(nombre):
    print(f"hola {nombre}")

bienvenida(n)

bienvenida = lambda nombre: f"Hola {nombre}" 

print(bienvenida(n))

multiplicar = lambda x: 2 * x

print(multiplicar(10))

'''


carrito = [
    {"prducto": "avena", "precio": 2000, "cantidad": 4},
    {"prducto": "Leche", "precio": 1300, "cantidad": 5}
]


#palabra clave lambda parametro: sentencia
totales = list(map(lambda item: item["precio"] * item["cantidad"], carrito))

print(totales)


'''palabra clave def nombre_de_la_funcion(parametro):
                   la sentencia '''

pagos = [ 
    {"clientes": "Juan", "atrasado": True},
    {"clientes": "Zeus", "atrasado": False},
    {"clientes": "Titan", "atrasado": True},
]

atrasados = list(filter(lambda p: p["atrasado"] == True, pagos))
print(atrasados)