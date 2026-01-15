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


while True:
    try:
        opcion =int(input("MENÚ DE CLIENTES\n"
        "1. Listar todos los clientes\n"
        "2. Listar clientes por estado\n"
        "3. Buscar cliente por nombre\n"
        "4. Buscar cliente por ID\n"
        "5. Buscar cliente por correo\n"
        "6. Buscar cliente por teléfono\n"
        "0. Salir / No realizar ninguna acción\n"))
        match opcion:   
            case 1:
                print(clients)
            case 2:
                try:
                    estado = input("Ingrese el estado del cliente \nCliente potencial \nAlto interés\nEn proceso de compra\nCliente efectivo\nSuper cliente): ")
                    for client in clients:
                        if client["estado"] == estado:
                            print(client)
                except ValueError:
                    print("estado no encontrado")
                    continue
            case 3:
                try:
                    nombre = input("Ingrese el nombre completo del cliente: ")
                    for client in clients:
                        if client["nombre_completo"] == nombre:
                            print(client)
                except ValueError:
                    print("cliente no encontrado")
                    continue
            case 4:
                try:
                    id = int(input("Ingrese el id del cliente: "))
                    for client in clients:
                        if client["id"] == id:
                            print(client)
                except ValueError:
                    print("el id debe ser un número , numeros validos son  del 1-20")
                    continue
            case 5:
                try:
                    correo = input("Ingrese el correo del cliente: ")
                    for client in clients:
                        if client["correo"] == correo:
                            print(client)
                except ValueError:
                    print("correo no encontrado")
                    continue
            case 6:
                try:
                    telefono = input("Ingrese el numerp del cliente (no olvide el +56 9): ")
                    for client in clients:
                        if client["telefono"] == telefono:
                            print(client)
                except ValueError:
                    print("telefono no encontrado")
                    continue

            case 0:
                print("Saliste del programa")
                break
            case _:
                print("Opción inválida")
                continue
    except ValueError:
        print("Opción inválida")
        continue