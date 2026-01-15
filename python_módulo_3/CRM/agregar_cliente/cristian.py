base_clientes = []  

while True:
    print("\n--- Agregar nuevo cliente ---")
    cliente = {}

    
    cliente["id"] = input("Ingrese el ID del cliente: ")
    cliente["nombre_completo"] = input("Ingrese el nombre completo: ")

    
    while True:
        telefono = input("Ingrese el teléfono (sin prefijo, solo números): ")
        if telefono.isdigit() and len(telefono) == 9:
            cliente["telefono"] = "+56" + telefono
            break
        else:
            print("Teléfono inválido. Debe contener solo números y tener 9 dígitos.")

    
    while True:
        correo = input("Ingrese el correo electrónico: ")
        if "@" in correo and ".cl" or ".com" in correo:
            cliente["correo"] = correo
            break
        else:
            print("Correo inválido. Debe contener '@' y '.cl' o '.com' Intente nuevamente.")

    
    estados = {
        "1": "Cliente potencial",
        "2": "Alto interés",
        "3": "En proceso de compra",
        "4": "Cliente efectivo",
        "5": "Súper cliente"
    }

    while True:
        print("Seleccione el estado del cliente:")
        print("1. Cliente potencial")
        print("2. Alto interés")
        print("3. En proceso de compra")
        print("4. Cliente efectivo")
        print("5. Súper cliente")

        opcion = input("Opción (1-5): ")

        if opcion in estados and opcion != "0":
            cliente["estado"] = estados[opcion]
            break
        else:
            print(" Opción inválida. Debe elegir un número del 1 al 5.")

    
    base_clientes.append(cliente)

    continuar = input("\n¿Desea agregar otro cliente? (s/n): ").lower()
    if continuar != "s":
        break


print("\n--- Base de clientes registrada ---")
for c in base_clientes:
    print(c)