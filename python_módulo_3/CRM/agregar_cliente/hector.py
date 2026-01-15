clientes = []

estados = {
    "1": "Cliente potencial",
    "2": "Alto interés",
    "3": "En proceso de compra",
    "4": "Cliente efectivo",
    "5": "Súper cliente"
    }
id = 0

while True:
    try:    
        agregar = (input("Desea agregar un nuevo cliente? (s/n): "))
        if agregar == "s":
            id += 1

            cliente = {
            "id": id,
            "nombre_cliente": "",
            "telefono": "",
            "correo": "",
            "estado_cliente": ""
        }
            cliente["id"] = id
            cliente["nombre_cliente"] = input("Ingrese el nombre del cliente: ")

            try:
                telefono = int(input("Ingrese el telefono del cliente: "))
                cliente["telefono"] = telefono
            except ValueError:
                print("El telefono debe ser un numero")
                continue

            cliente["correo"] = input("Ingrese el correo del cliente: ")
            try:
                print(
                    "Seleccione el estado del cliente:\n"
                    "1) Cliente potencial\n"
                    "2) Alto interés\n"
                    "3) En proceso de compra\n"
                    "4) Cliente efectivo\n"
                    "5) Súper cliente"
                )
                estado_opcion = int(input("Ingrese el estado del cliente del 1 al 5: "))
                if estado_opcion < 1 or estado_opcion > 5:
                    print("Opción inválida")
                    continue
                opcion_elegida = str(estado_opcion)         
            except ValueError:
                print("Opción inválida")
                continue
            cliente["estado_cliente"] = estados [str(opcion_elegida)]
            clientes.append(cliente)
            continue
        elif agregar == "n":
            ("No se agregaron clientes")
            break   
    except ValueError:
        print("Opción inválida")
        continue

print(clientes)