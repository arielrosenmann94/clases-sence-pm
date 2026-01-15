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

print("=== CRM CLIENTES ===")
print("1 - LISTAR clientes")
print("2 - BUSCAR cliente")

opcion = input("Seleccione una opción: ").strip()

# ================= LISTAR =================
if opcion == "1":
    print("--- MENÚ LISTAR ---")
    print("a - TODOS los clientes")
    print("b - POR ESTADO de los clientes")

    opcion_listar = input("Seleccione una opción: ").strip().lower()

    if opcion_listar not in ["a", "b"]:
        print("Opción inválida.")
    
    # Listar TODOS
    elif opcion_listar == "a":
        if len(clients) == 0:
            print("No hay clientes registrados.")
        else:
            print("=== LISTADO DE CLIENTES ===")
            for cliente in clients:
                print("----------------------------")
                print("ID:", cliente["id"])
                print("Nombre:", cliente["nombre_completo"])
                print("Teléfono:", cliente["telefono"])
                print("Correo:", cliente["correo"])
                print("Estado:", cliente["estado"])

    # Listar POR ESTADO (con estados numerados)
    elif opcion_listar == "b":

        print("Estados disponibles:")

        estados_validos = {}
        contador = 1

        for cliente in clients:
            estado = cliente["estado"]
            if estado.lower() not in estados_validos.values():
                estados_validos[contador] = estado.lower()
                print(contador, "-", estado)
                contador += 1

        opcion_estado = input("Seleccione el número del estado: ").strip()

        if not opcion_estado.isdigit() or int(opcion_estado) not in estados_validos:
            print("Opción de estado inválida.")
        else:
            estado_seleccionado = estados_validos[int(opcion_estado)]
            encontrado = False

            for cliente in clients:
                if cliente["estado"].lower() == estado_seleccionado:
                    print("----------------------------")
                    print("ID:", cliente["id"])
                    print("Nombre:", cliente["nombre_completo"])
                    print("Teléfono:", cliente["telefono"])
                    print("Correo:", cliente["correo"])
                    print("Estado:", cliente["estado"])
                    encontrado = True

            if not encontrado:
                print("No se encontraron clientes con ese estado.")
# ================= BUSCAR =================

elif opcion == "2":
    print("--- MENÚ BUSCAR ---")
    print("1 - Buscar por NOMBRE")
    print("2 - Buscar por ID")
    print("3 - Buscar por CORREO")
    print("4 - Buscar por TELÉFONO")

    opcion_buscar = input("Seleccione una opción: ").strip()

    # ================= BUSCAR POR NOMBRE =================
    if opcion_buscar == "1":
        nombre_buscar = input("Ingrese nombre a buscar: ").strip().lower()
        encontrados = 0

        for cliente in clients:
            if nombre_buscar in cliente["nombre_completo"].lower():
                print(cliente)
                encontrados += 1

        if encontrados == 0:
            print("No se encontraron clientes con ese nombre.")
        elif encontrados > 1:
            print("Aviso: existen varios clientes con ese nombre. Total encontrados: ", encontrados)

    # ================= BUSCAR POR ID =================
    elif opcion_buscar == "2":
        id_buscar = input("Ingrese ID: ").strip()

        if not id_buscar.isdigit():
            print("ID inválido. Debe ser numérico.")
        else:
            encontrado = False
            for cliente in clients:
                if cliente["id"] == int(id_buscar):
                    print(cliente)
                    encontrado = True
                    break

            if not encontrado:
                print("Cliente no encontrado.")

    # ================= BUSCAR POR CORREO =================
    elif opcion_buscar == "3":
        correo_buscar = input("Ingrese correo: ").strip()

        if "@" not in correo_buscar or "." not in correo_buscar:
            print("Correo inválido.")
        else:
            coincidencias = 0
            for cliente in clients:
                if cliente["correo"].lower() == correo_buscar.lower():
                    print(cliente)
                    coincidencias += 1

            if coincidencias == 0:
                print("Cliente no encontrado.")
            elif coincidencias > 1:
                print("Aviso: hay correos duplicados. Total duplicados: ", coincidencias)

    # ================= BUSCAR POR TELÉFONO =================
    elif opcion_buscar == "4":
        telefono_buscar = input("Ingrese teléfono: ").strip()

        if len(telefono_buscar) < 8:
            print("Teléfono inválido.")
        else:
            encontrado = False
            for cliente in clients:
                if cliente["telefono"] == telefono_buscar:
                    print(cliente)
                    encontrado = True
                    break

            if not encontrado:
                print("Cliente no encontrado.")

    else:
        print("Opción inválida.")

else:
    print("Opción inválida.")