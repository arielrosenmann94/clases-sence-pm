clientes = []

id = input("ID: ")
nombre = input("Nombre: ")
apellido = input("Apellido: ")
telefono = input("Número de teléfono: ")
tipo_in = input("Tipo de cliente (ELige un numero: 1.- Potencial, 2.- alto interes, 3.- en proceso, 4.- Efectivo, 5.- Super): ").strip().lower()

if tipo_in.isdigit():
    tipo = int(tipo_in)
    opciones = {
        1: "Cliente potencial",
        2: "Cliente alto interes",
        3: "Cliente en proceso",
        4: "Cliente efectivo",
        5: "Super Cliente"
    }
    tipo_in = opciones.get(tipo, tipo_in)
# else: resuelve el else y el isdigit para que no entren letras 
 

cliente = {
    "id": id,
    "nombre": nombre,
    "apellido": apellido,
    "telefono": telefono,
    "tipo": tipo_in
}
clientes.append(cliente)

print(clientes)