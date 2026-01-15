clientes = []

while True:
    id_cliente = input("Ingrese ID del cliente (solo números): ")
    if id_cliente.isdigit():
        id_cliente = int(id_cliente)
        break
    else:
        print("El ID debe ser un número entero.")

nombre = input("Ingrese nombre completo del cliente: ").strip()

while True:
    telefono = input("Ingrese teléfono (solo números incluyendo el 9): ")
    if telefono.isdigit() and (len(telefono) == 9) and (telefono.startswith("9")):
        telefono = int(telefono)
        break
    else:
        print("El teléfono debe contener solo números, incluyendo el 9 delante de su número.")

while True:
    correo = input("Ingrese correo electrónico: ").strip()
    if "@" in correo:
        partes = correo.split("@")
        if len(partes) == 2 and "." in partes[1]:
            break
    print("Correo inválido.")

estados = {
    "1": "Cliente potencial",
    "2": "Alto interés",
    "3": "En proceso de compra",
    "4": "Cliente efectivo",
    "5": "Super cliente"
}

print("\nEstado del cliente:")
for k, v in estados.items():
    print(f"{k}. {v}")

while True:
    opcion_estado = input("Seleccione una opción (1-5): ")
    estado_cliente = estados.get(opcion_estado, "Opción inválida")
    if estado_cliente != "Opción inválida":
        break
    else:
        print("Opción inválida.")

cliente = {
    "id": id_cliente,
    "nombre": nombre,
    "telefono": telefono,
    "correo": correo,
    "estado": estado_cliente
}

clientes.append(cliente)

print("\n Cliente agregado correctamente:")
print(cliente)