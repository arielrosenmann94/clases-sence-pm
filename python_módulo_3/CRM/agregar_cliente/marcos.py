clientes = []

estados_validos = {
    1: "cliente potencial",
    2: "alto interés",
    3: "en proceso de compra",
    4: "cliente efectivo",
    5: "super cliente"
}

id_cliente = len(clientes) + 1
print("ID del cliente (asignado automáticamente):", id_cliente)

while True:
    nombre = input("Ingrese nombre completo: ").strip()
    if nombre != "":
        break
    print("Nombre inválido. No puede estar vacío.")

while True:
    celular = input("Ingrese el número de su celular: (Ejemplo: 912345678)").strip()

    if not celular.isdigit():
        print("Error: el celular debe contener solo números.")
        continue

    if len(celular) == 8:
        celular = "569" + celular
    elif len(celular) == 9 and celular.startswith("9"):
        celular = "56" + celular
    elif len(celular) == 11 and celular.startswith("569"):
        pass
    else:
        print("Error: formato de celular inválido.")
        continue

    break

while True:
    correo = input("Ingrese correo: ").strip()
    if (
        "@" in correo
        and correo.count("@") == 1
        and "." in correo.split("@")[1]
        and not correo.startswith("@")
        and not correo.endswith(".")
    ):
        break
    else:
        print("Error: correo inválido. Ejemplo: ejemplo@correo.cl")

while True:
    print("Seleccione estado del cliente:")
    for key, value in estados_validos.items():
        print(key, "-", value)

    opcion = input("Ingrese opción (número): ").strip()

    if opcion.isdigit() and int(opcion) in estados_validos:
        estado = estados_validos[int(opcion)]
        break
    else:
        print("Opción inválida. Intente nuevamente.")

cliente = {
    "id": id_cliente,
    "nombre": nombre,
    "telefono": celular,
    "correo": correo,
    "estado": estado
}

clientes.append(cliente)

#Salida con FORMATO
print("\n=== BASE DE CLIENTES ===")

for cliente in clientes:
    print("----------------------------")
    print("ID:              ", cliente["id"])
    print("Nombre completo: ", cliente["nombre"])
    print("Teléfono:        ", cliente["telefono"])
    print("Correo:          ", cliente["correo"])
    print("Estado cliente:  ", cliente["estado"])

print("----------------------------")

#Salida sin FORMATO
'''print("Base de clientes:")
print(clientes)'''