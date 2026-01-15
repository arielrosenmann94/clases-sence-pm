clients = [
    {"id": 1, "nombre_completo": "Ana Torres", "correo": "ana.torres@correo.com", "telefono": "+56 9 42351234", "estado": "Cliente potencial"},
    {"id": 2, "nombre_completo": "Luis Ramírez", "correo": "luis.ramirez@correo.com", "telefono": "+56 9 93481234", "estado": "Alto interés"},
    {"id": 3, "nombre_completo": "Claudia Soto", "correo": "claudia.soto@correo.com", "telefono": "+56 9 78123456", "estado": "Cliente efectivo"},
    {"id": 4, "nombre_completo": "Jorge Fuentes", "correo": "jorge.fuentes@correo.com", "telefono": "+56 9 63547812", "estado": "En proceso de compra"},
    {"id": 5, "nombre_completo": "Marta Herrera", "correo": "marta.herrera@correo.com", "telefono": "+56 9 98124578", "estado": "Super cliente"},
    {"id": 6, "nombre_completo": "Carlos Díaz", "correo": "carlos.diaz@correo.com", "telefono": "+56 9 71234598", "estado": "Alto interés"},
    {"id": 7, "nombre_completo": "Francisca Rojas", "correo": "francisca.rojas@correo.com", "telefono": "+56 9 91234871", "estado": "Cliente efectivo"},
    {"id": 8, "nombre_completo": "Pedro Gutiérrez", "correo": "pedro.gutierrez@correo.com", "telefono": "+56 9 84567213", "estado": "Cliente potencial"},
    {"id": 9, "nombre_completo": "Valentina Bravo", "correo": "valentina.bravo@correo.com", "telefono": "+56 9 78341236", "estado": "Super cliente"},
    {"id": 10, "nombre_completo": "Diego Castro", "correo": "diego.castro@correo.com", "telefono": "+56 9 93456781", "estado": "En proceso de compra"},
    {"id": 11, "nombre_completo": "Camila Paredes", "correo": "camila.paredes@correo.com", "telefono": "+56 9 91234578", "estado": "Cliente potencial"},
    {"id": 12, "nombre_completo": "Andrés Molina", "correo": "andres.molina@correo.com", "telefono": "+56 9 89451236", "estado": "Cliente efectivo"},
    {"id": 13, "nombre_completo": "Patricia Silva", "correo": "patricia.silva@correo.com", "telefono": "+56 9 74382910", "estado": "Alto interés"},
    {"id": 14, "nombre_completo": "Matías Reyes", "correo": "matias.reyes@correo.com", "telefono": "+56 9 87234561", "estado": "En proceso de compra"},
    {"id": 15, "nombre_completo": "Isidora Méndez", "correo": "isidora.mendez@correo.com", "telefono": "+56 9 98127345", "estado": "Super cliente"},
    {"id": 16, "nombre_completo": "Sebastián Núñez", "correo": "sebastian.nunez@correo.com", "telefono": "+56 9 65432178", "estado": "Cliente efectivo"},
    {"id": 17, "nombre_completo": "Fernanda Loyola", "correo": "fernanda.loyola@correo.com", "telefono": "+56 9 72345681", "estado": "Alto interés"},
    {"id": 18, "nombre_completo": "Tomás Aravena", "correo": "tomas.aravena@correo.com", "telefono": "+56 9 83451234", "estado": "Cliente potencial"},
    {"id": 19, "nombre_completo": "Josefa Espinoza", "correo": "josefa.espinoza@correo.com", "telefono": "+56 9 96432187", "estado": "Cliente efectivo"},
    {"id": 20, "nombre_completo": "Ricardo Vergara", "correo": "ricardo.vergara@correo.com", "telefono": "+56 9 78912345", "estado": "Super cliente"}
]

opcion = ""

while opcion != "3":
    print("\nMENU PRINCIPAL")
    print("1. Listar clientes")
    print("2. Buscar cliente")
    print("3. Salir")

    opcion = input("Seleccione una opción: ").strip()

    match opcion:
        case "1":
            print("\nLISTAR CLIENTES POR:")
            print("1. Todos")
            print("2. Estado")

            subopcion = input("Seleccione opción: ").strip()

            match subopcion:
                case "1":
                    for cliente in clients:
                        print(cliente)

                case "2":
                    estado_buscar = input("Ingrese el estado: ").strip().lower()
                    encontrados = False

                    for cliente in clients:
                        if estado_buscar in cliente["estado"].lower():
                            print(cliente)
                            encontrados = True

                    if not encontrados:
                        print("No se encontraron clientes con ese estado.")

                case _:
                    print("Opción inválida.")

        case "2":
            print("\nBUSCAR CLIENTE POR:")
            print("1. Nombre")
            print("2. ID")
            print("3. Correo")
            print("4. Teléfono")
            print("5. Estado")

            subopcion = input("Seleccione opción: ").strip()

            match subopcion:
                case "1":
                    nombre = input("Ingrese nombre: ").strip().lower()
                    encontrados = False

                    for cliente in clients:
                        if nombre in cliente["nombre_completo"].lower():
                            print(cliente)
                            encontrados = True

                    if not encontrados:
                        print("No se encontraron clientes con ese nombre.")

                case "2":
                    id_buscar = input("Ingrese el ID: ").strip()
                    encontrados = False

                    for cliente in clients:
                        if str(cliente["id"]) == id_buscar:
                            print(cliente)
                            encontrados = True

                    if not encontrados:
                        print("No se encontró cliente con ese ID.")

                case "3":
                    correo = input("Ingrese el correo: ").strip().lower()
                    encontrados = False

                    for cliente in clients:
                        if cliente["correo"].lower() == correo:
                            print(cliente)
                            encontrados = True

                    if not encontrados:
                        print("No se encontró cliente con ese correo.")

                case "4":
                    telefono = input("Ingrese el teléfono: ").strip()
                    encontrados = False

                    for cliente in clients:
                        if cliente["telefono"] == telefono:
                            print(cliente)
                            encontrados = True

                    if not encontrados:
                        print("No se encontró cliente con ese teléfono.")

                case "5":
                    estado = input("Ingrese el estado: ").strip().lower()
                    encontrados = False

                    for cliente in clients:
                        if estado in cliente["estado"].lower():
                            print(cliente)
                            encontrados = True

                    if not encontrados:
                        print("No se encontraron clientes con ese estado.")

                case _:
                    print("Opción inválida.")

        case "3":
            print("Saliendo del sistema.")

        case _:
            print("Opción inválida.")