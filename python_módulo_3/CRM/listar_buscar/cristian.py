clientes = [
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

print("=== SISTEMA DE CLIENTES ===")
opcion = input("¿Desea LISTAR o BUSCAR clientes? (escriba 'listar' o 'buscar'): ").strip().lower()

# --- OPCIÓN LISTAR ---
if opcion == "listar":
    print("1. Listar todos los clientes")
    print("2. Listar por estado de cliente")
    opcion_listar = input("Seleccione una opción (1 o 2): ").strip()

    if opcion_listar == "1":
        print("\n=== LISTADO COMPLETO DE CLIENTES ===")
        for cliente in clientes:
            print(cliente)

    elif opcion_listar == "2":
        estado_buscar = input("\nIngrese el estado de cliente a filtrar: ").strip()
        encontrados = []
        for cliente in clientes:
            if cliente["estado"].lower() == estado_buscar.lower():
                encontrados.append(cliente)

        print(f"\n=== CLIENTES CON ESTADO '{estado_buscar}' ===")
        if encontrados:
            for c in encontrados:
                print(c)
        else:
            print("No se encontraron clientes con ese estado.")
    else:
        print("Opción inválida.")

# --- OPCIÓN BUSCAR ---
elif opcion == "buscar":
    print("\n1. Buscar por nombre")
    print("2. Buscar por ID")
    print("3. Buscar por correo")
    print("4. Buscar por teléfono")
    opcion_buscar = input("Seleccione una opción (1-4): ").strip()

    if opcion_buscar == "1":
        nombre_buscar = input("\nIngrese el nombre del cliente a buscar: ").strip().lower()
        resultados = []
        for cliente in clientes:
            if nombre_buscar in cliente["nombre_completo"].lower():
                resultados.append(cliente)
        print(f"\n=== RESULTADOS POR NOMBRE '{nombre_buscar}' ===")
        if resultados:
            for c in resultados:
                print(c)
        else:
            print("No se encontraron clientes con ese nombre.")

    elif opcion_buscar == "2":
        try:
            id_buscar = int(input("\nIngrese el ID del cliente: "))
            resultados = []
            for cliente in clientes:
                if cliente["id"] == id_buscar:
                    resultados.append(cliente)
            print(f"\n=== RESULTADOS POR ID '{id_buscar}' ===")
            if resultados:
                for c in resultados:
                    print(c)
            else:
                print("No se encontró ningún cliente con ese ID.")
        except ValueError:
            print("El ID debe ser un número válido.")

    elif opcion_buscar == "3":
        correo_buscar = input("\nIngrese el correo del cliente: ").strip().lower()
        resultados = []
        for cliente in clientes:
            if cliente["correo"].lower() == correo_buscar:
                resultados.append(cliente)
        print(f"\n=== RESULTADOS POR CORREO '{correo_buscar}' ===")
        if resultados:
            for c in resultados:
                print(c)
        else:
            print("No se encontraron clientes con ese correo.")

    elif opcion_buscar == "4":
        telefono_buscar = input("\nIngrese el teléfono del cliente (ej: +56911111111): ").strip()
        resultados = []
        for cliente in clientes:
            if cliente["telefono"] == telefono_buscar:
                resultados.append(cliente)
        print(f"\n=== RESULTADOS POR TELÉFONO '{telefono_buscar}' ===")
        if resultados:
            for c in resultados:
                print(c)
        else:
            print("No se encontraron clientes con ese teléfono.")
    else:
        print("Opción inválida.")

else:
    print("Opción no reconocida. Debe escribir 'listar' o 'buscar'.")