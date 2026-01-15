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


print("=== GESTOR DE CLIENTES ===")
while True:
    print("\nOpciones:")
    print("1. Listar todos los clientes")
    print("2. Listar por estado de cliente")
    print("3. Buscar por nombre")
    print("4. Buscar por ID")
    print("5. Buscar por correo")
    print("6. Buscar por teléfono")
    print("0. Salir")
    
    opcion = input("Elige una opción: ").strip()
    
    if opcion == "0":
        print("¡Hasta luego!")
        break
    
    elif opcion == "1":
        print("\n=== TODOS LOS CLIENTES ===")
        for cliente in clients:
            print(f"ID: {cliente['id']} | {cliente['nombre_completo']} | {cliente['estado']}")
    
    elif opcion == "2":
        print("\nEstados disponibles:")
        estados = []
        for cliente in clients:
            if cliente["estado"] not in estados:
                estados.append(cliente["estado"])
        for i, estado in enumerate(sorted(estados), 1):
            print(f"{i}. {estado}")
        estado = input("Ingresa el estado (exacto): ").strip().lower()
        print(f"\n=== CLIENTES '{estado.title()}' ===")
        encontrados = False
        for cliente in clients:
            if cliente["estado"].lower() == estado:
                print(f"ID: {cliente['id']} | {cliente['nombre_completo']} | Tel: {cliente['telefono']}")
                encontrados = True
        if not encontrados:
            print("No hay clientes con ese estado.")
    
    elif opcion == "3":
        nombre = input("Ingresa el nombre (sin tildes): ").strip().lower()
        print(f"\n=== BUSCANDO '{nombre.title()}' ===")
        encontrados = False
        for cliente in clients:
            nombre_cliente = cliente["nombre_completo"].lower()
            nombre_cliente = nombre_cliente.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
            nombre_cliente = nombre_cliente.replace("à", "a").replace("è", "e").replace("ì", "i").replace("ò", "o").replace("ù", "u")
            nombre_cliente = nombre_cliente.replace("ä", "a").replace("ë", "e").replace("ï", "i").replace("ö", "o").replace("ü", "u")
            nombre_cliente = nombre_cliente.replace("ñ", "n")
            if nombre in nombre_cliente:
                print(f"ID: {cliente['id']} | {cliente['nombre_completo']} | Estado: {cliente['estado']}")
                encontrados = True
        if not encontrados:
            print("No se encontró ese nombre.")
    
    elif opcion == "4":
        try:
            id_buscar = int(input("Ingresa el ID: "))
            cliente = None
            for c in clients:
                if c["id"] == id_buscar:
                    cliente = c
                    break
            if cliente:
                print("\n=== CLIENTE ENCONTRADO ===")
                print(f"Nombre: {cliente['nombre_completo']}")
                print(f"Correo: {cliente['correo']}")
                print(f"Teléfono: {cliente['telefono']}")
                print(f"Estado: {cliente['estado']}")
            else:
                print("ID no existe.")
        except ValueError:
            print("El ID debe ser un número.")
    
    elif opcion == "5":
        correo = input("Ingresa el correo (parcial): ").strip().lower()
        print("\n=== BUSCANDO CORREO ===")
        encontrados = False
        for cliente in clients:
            if correo in cliente["correo"].lower():
                print(f"ID: {cliente['id']} | {cliente['nombre_completo']} | Estado: {cliente['estado']}")
                encontrados = True
        if not encontrados:
            print("Correo no encontrado.")
    
    elif opcion == "6":
        telefono = input("Ingresa el teléfono (parcial): ").strip()
        print("\n=== BUSCANDO TELÉFONO ===")
        encontrados = False
        for cliente in clients:
            if telefono in cliente["telefono"]:
                print(f"ID: {cliente['id']} | {cliente['nombre_completo']} | Estado: {cliente['estado']}")
                encontrados = True
        if not encontrados:
            print("Teléfono no encontrado.")
    
    else:
        print("Opción inválida, elige 0-6.")

    