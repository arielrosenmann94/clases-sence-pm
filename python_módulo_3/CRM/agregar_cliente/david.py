base_clientes = []

while True:
    print("INGRESO DE CLIENTE")

    while True:
        id_cliente = input("ID Cliente: ").strip()
        if len(id_cliente) > 0:
            break
        print("Error: El ID es obligatorio.")

    while True:
        nombre = input("Nombre completo: ").strip()
        if len(nombre) > 0 and nombre.replace(" ", "").isalpha():
            break
        print("Error: Ingrese un nombre valido.")

    while True:
        telefono = input("Telefono (movil 9 digitos): ")
        if telefono.isdigit() and len(telefono) == 9 and telefono.startswith("9"):
            telefono = "+56" + telefono
            break
        else:
            print("Error: Ingrese un numero chileno valido (Ej: 912345678).")

    while True:
        correo = input("Correo electronico: ").strip()
        if "@" in correo and "." in correo:
            break
        print("Error: Correo invalido.")

    print("Seleccione estado:")
    print("1. Cliente potencial")
    print("2. Alto interes")
    print("3. En proceso de compra")
    print("4. Cliente efectivo")
    print("5. Super cliente")
    
    estado = ""
    while True:
        opcion = input("Opcion: ")
        
        if opcion == "1":
            estado = "Cliente potencial"
            break
        elif opcion == "2":
            estado = "Alto interes"
            break
        elif opcion == "3":
            estado = "En proceso de compra"
            break
        elif opcion == "4":
            estado = "Cliente efectivo"
            break
        elif opcion == "5":
            estado = "Super cliente"
            break
        else:
            print("Opcion incorrecta.")

    nuevo_cliente = {
        "id": id_cliente,
        "nombre": nombre,
        "telefono": telefono,
        "correo": correo,
        "estado": estado
    }
    
    base_clientes.append(nuevo_cliente)
    
    print("BASE DE DATOS:")
    print(base_clientes)

    continuar = input("Desea agregar otro cliente? (s/n): ")
    if continuar.lower() != "s":
        break