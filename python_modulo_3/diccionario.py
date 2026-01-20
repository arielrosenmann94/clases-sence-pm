diccionario = {
    "clave": "valor",
    "otra clave": 23,
    "una clave más": "otro valor"
}

persona = {
    "nombre": "Apolo",
    "edad": 5000,
    "correo": "apolo@olimpo.cl",
}

print("Acá imprimo todo el diccionario persona: ", persona)
print("Acá solo estoy imprimiento el valor de la clave 'nombre' para el diccionario 'persona'", persona["nombre"])

correo = persona["correo"]
print(correo)
print(persona["correo"])

persona["correo"] = "soyapolo@olimpo.com"
correo = persona["correo"]
print(correo)

persona["ubicación"] = "olimpo"

print(persona)
print(type(persona))

lista_diccionario = [
    {"id": 1, "nombre": "Juan perez", "correo": "soyjuan@gmail.com"},
    {"id": 2, "nombre": "Juan Rojas", "correo": "juan@rojas.com"}
]

diccionario_de_diccionarios = {
    1: {"nombre": "Juan perez", "correo": "soyjuan@gmail.com"},
    2: {"nombre": "Juan Rojas", "correo": "juan@rojas.com"}
}