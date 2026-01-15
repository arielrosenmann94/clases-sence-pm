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


continuar = True
switch_cliente = {
        "1": "listar_todos",
        "2": "listar_estado",
        "3": "buscar_nombre",
        "4": "buscar_id",
        "5": "buscar_correo",
        "6": "buscar_telefono",
        "7": "salir"
    }

while continuar:
    print("\n¿Qué acción desea realizar? \nSeleccione una opción(sólo el número):")
    print("1. Listar todos los clientes")
    print("2. Listar clientes por estado")
    print("3. Buscar por nombre")
    print("4. Buscar por ID")
    print("5. Buscar por correo")
    print("6. Buscar por teléfono")
    print("7. Salir\n")
    
    opcion = input("Seleccione una opción: ").strip()
    if not opcion.isdigit():
        print("Debe ingresar un número\n")
        continue
    elif opcion not in switch_cliente:
        print("\nOpción fuera de rango, elija una opción del 1 al 7.\n")
        continue


    accion = switch_cliente.get(opcion)

    if accion == "listar_todos":
        for c in clients:
            print(c)
    elif accion == "listar_estado":
        estado = input("\nIngrese estado del cliente: ").strip()
        if estado == "":
            print("El estado no puede estar vacío\n")
        else:
            encontrado = False
            for c in clients:
                if c["estado"].lower() == estado.lower():
                    print(c)
                    encontrado = True
            if not encontrado:
                print("No hay clientes con ese estado\n")
    elif accion == "buscar_nombre":
        nombre = input("\nIngrese nombre a buscar: ").strip()
        if nombre == "":
            print("El nombre no puede estar vacío\n")
        else:
            encontrado = False
            for c in clients:
                if nombre.lower() in c["nombre_completo"].lower():
                    print(c)
                    encontrado = True
            if not encontrado:
                print("Cliente no encontrado\n")
    elif accion == "buscar_id":
        id_buscar = input("\nIngrese ID a buscar: ").strip()
        if not id_buscar.isdigit():
            print("El ID debe ser numérico\n")
        else:
            id_buscar = int(id_buscar)
            encontrado = False
            for c in clients:
                if c["id"] == id_buscar:
                    print(c)
                    encontrado = True
                    break
            if not encontrado:
                print("ID no encontrado\n")
    elif accion == "buscar_correo":
        correo = input("\nIngrese correo a buscar: ").strip()
        if correo == "":
            print("El correo no puede estar vacío\n")
        else:
            encontrado = False
            for c in clients:
                if c["correo"].lower() == correo.lower():
                    print(c)
                    encontrado = True
                    break
            if not encontrado:
                print("Correo no encontrado\n")
    elif accion == "buscar_telefono":
        telefono = input("\nIngrese teléfono: ").strip()
        if telefono == "":
            print("El teléfono no puede estar vacío\n")
        else:
            encontrado = False
            for c in clients:
                if c["telefono"] == telefono:
                    print(c)
                    encontrado = True
                    break
            if not encontrado:
                print("Teléfono no encontrado \n")
    elif accion == "salir":
        print("\nSaliendo del sistema...")
        continuar = False