# --- BASE DE DATOS INICIAL ---
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

# --- INICIO DEL PROGRAMA PRINCIPAL (Sin funciones, con match-case) ---

while True:
    print("\n" + "═" * 60)
    print("SISTEMA DE GESTIÓN DE CLIENTES (CRM)".center(60))
    print("═" * 60)
    print(" 1. 📋 LISTAR clientes")
    print(" 2. 🔍 BUSCAR cliente")
    print(" 3. ➕ REGISTRAR nuevo cliente")
    print(" 4. 🚪 SALIR")
    
    accion_principal = input("\n>> ¿Qué desea hacer? (1-4): ").strip()

    match accion_principal:
        
        # ==========================================
        # CASO 1: LISTAR
        # ==========================================
        case "1":
            print("\n" + "-" * 60)
            print("MENÚ LISTAR".center(60))
            print("-" * 60)
            print(" 1. Listar TODOS los clientes")
            print(" 2. Listar por ESTADO (filtro)")
            print(" 3. Volver atrás")

            opcion_listar = input("\n>> Ingrese opción: ").strip()
            lista_resultados = [] 
            mostrar_resultados = False
            titulo_tabla = ""

            match opcion_listar:
                case "1":
                    lista_resultados = clients
                    mostrar_resultados = True
                    titulo_tabla = "LISTADO COMPLETO"

                case "2":
                    print("\n[SELECCIONE ESTADO A FILTRAR]:")
                    print(" 1. Cliente potencial")
                    print(" 2. Alto interés")
                    print(" 3. En proceso de compra")
                    print(" 4. Cliente efectivo")
                    print(" 5. Super cliente")
                    
                    op_filtro = input("\n>> Ingrese número de opción (1-5): ").strip()
                    estado_filtro = ""

                    match op_filtro:
                        case "1": estado_filtro = "Cliente potencial"
                        case "2": estado_filtro = "Alto interés"
                        case "3": estado_filtro = "En proceso de compra"
                        case "4": estado_filtro = "Cliente efectivo"
                        case "5": estado_filtro = "Super cliente"
                        case _:
                            print("❌ Opción no válida.")

                    if estado_filtro:
                        # Filtro exacto por selección de menú
                        lista_resultados = []
                        for c in clients:
                            if c["estado"] == estado_filtro:
                                lista_resultados.append(c)
                        
                        mostrar_resultados = True
                        titulo_tabla = f"FILTRADO POR: '{estado_filtro}'"

                case "3":
                    pass # Volver al inicio
                
                case _:
                    print("❌ Opción no válida.")

            # Bloque de impresión de tabla
            if mostrar_resultados:
                print("\n" + "═" * 115)
                print(titulo_tabla.center(115))
                print("═" * 115)
                if not lista_resultados:
                    print(f"\n⚠️  No se encontraron resultados para '{estado_filtro}'.")
                else:
                    # Encabezado
                    print(f"{'ID':<5} | {'NOMBRE':<25} | {'CORREO':<30} | {'TELÉFONO':<15} | {'ESTADO':<20}")
                    print("-" * 115)
                    # Filas
                    for c in lista_resultados:
                        print(f"{str(c['id']):<5} | {c['nombre_completo']:<25} | {c['correo']:<30} | {c['telefono']:<15} | {c['estado']:<20}")
                    print("-" * 115)
                    print(f"Total registros encontrados: {len(lista_resultados)}")
                
                input("\nPresione ENTER para continuar...")

        # ==========================================
        # CASO 2: BUSCAR
        # ==========================================
        case "2":
            print("\n" + "-" * 60)
            print("MENÚ BUSCAR".center(60))
            print("-" * 60)
            print(" 1. Buscar por Nombre")
            print(" 2. Buscar por ID")
            print(" 3. Buscar por Correo")
            print(" 4. Buscar por Teléfono")
            print(" 5. Volver atrás")

            opcion_buscar = input("\n>> Ingrese opción: ").strip()
            
            match opcion_buscar:
                case "5":
                    continue 
                
                case "1" | "2" | "3" | "4":
                    termino = input(">> Ingrese el término de búsqueda: ").strip().lower()
                    lista_resultados = []
                    criterio_txt = ""

                    match opcion_buscar:
                        case "1": # Nombre (Búsqueda por palabras clave)
                            criterio_txt = "NOMBRE (Palabras clave)"
                            palabras_clave = termino.split() # Separa "Ana Torres" -> ["ana", "torres"]
                            
                            for c in clients:
                                nombre_cliente = c["nombre_completo"].lower()
                                # Verifica si TODAS las palabras ingresadas están presentes en el nombre
                                todas_presentes = True
                                for palabra in palabras_clave:
                                    if palabra not in nombre_cliente:
                                        todas_presentes = False
                                        break
                                
                                if todas_presentes:
                                    lista_resultados.append(c)
                        
                        case "2": # ID
                            criterio_txt = "ID"
                            for c in clients:
                                # ID es exacto
                                if termino == str(c["id"]):
                                    lista_resultados.append(c)

                        case "3": # Correo
                            criterio_txt = "CORREO"
                            for c in clients:
                                if termino in c["correo"].lower():
                                    lista_resultados.append(c)

                        case "4": # Teléfono
                            criterio_txt = "TELÉFONO"
                            # Limpiamos espacios y simbolos para buscar solo los números
                            termino_limpio = termino.replace(" ", "").replace("+", "")
                            for c in clients:
                                telefono_db_limpio = c["telefono"].replace(" ", "").replace("+", "")
                                if termino_limpio in telefono_db_limpio:
                                    lista_resultados.append(c)
                    
                    # Imprimir resultados búsqueda
                    print("\n" + "═" * 115)
                    print(f"RESULTADOS BÚSQUEDA POR {criterio_txt}: '{termino}'".center(115))
                    print("═" * 115)
                    
                    if not lista_resultados:
                        print("\n⚠️  No se encontraron coincidencias.")
                    else:
                        print(f"{'ID':<5} | {'NOMBRE':<25} | {'CORREO':<30} | {'TELÉFONO':<15} | {'ESTADO':<20}")
                        print("-" * 115)
                        for c in lista_resultados:
                            print(f"{str(c['id']):<5} | {c['nombre_completo']:<25} | {c['correo']:<30} | {c['telefono']:<15} | {c['estado']:<20}")
                        print("-" * 115)
                    
                    input("\nPresione ENTER para continuar...")

                case _:
                    print("❌ Opción no válida.")

        # ==========================================
        # CASO 3: REGISTRAR (Normalizado)
        # ==========================================
        case "3":
            print("\n" + "-" * 60)
            print("REGISTRO DE NUEVO CLIENTE".center(60))
            print("-" * 60)

            # 1. Validación ID
            id_nuevo = 0
            while True:
                entrada_id = input("Ingrese ID (Numérico): ").strip()
                if entrada_id.isdigit():
                    id_temp = int(entrada_id)
                    existe = False
                    for c in clients:
                        if c['id'] == id_temp:
                            existe = True
                            break
                    if existe:
                        print("❌ Error: Ese ID ya está registrado.")
                    else:
                        id_nuevo = id_temp
                        break
                else:
                    print("❌ Error: Debe ingresar solo números.")

            # 2. Validación Nombre (Normalización: Title Case)
            nombre_nuevo = ""
            while True:
                entrada_nombre = input("Nombre Completo: ").strip()
                # Verifica que tenga caracteres válidos (letras y espacios)
                if len(entrada_nombre) > 2 and entrada_nombre.replace(" ", "").isalpha():
                    nombre_nuevo = entrada_nombre.title() # Ej: "juan perez" -> "Juan Perez"
                    break
                else:
                    print("❌ Error: Ingrese un nombre válido (solo letras).")

            # 3. Validación Teléfono (Flexible)
            telefono_nuevo = ""
            while True:
                entrada_tel = input("Teléfono: ").strip()
                # Quitamos + y espacios para validar que el resto sean digitos
                check_digits = entrada_tel.replace(" ", "").replace("+", "")
                
                if check_digits.isdigit() and len(check_digits) >= 8:
                    telefono_nuevo = entrada_tel # Guardamos el formato original ingresado por el usuario
                    break
                print("❌ Error: Teléfono inválido (mínimo 8 dígitos).")

            # 4. Validación Correo (Normalización: Lower Case)
            correo_nuevo = ""
            while True:
                entrada_correo = input("Correo: ").strip()
                if "@" in entrada_correo and "." in entrada_correo:
                    correo_nuevo = entrada_correo.lower() # Ej: "Ana@Gmail.com" -> "ana@gmail.com"
                    break
                print("❌ Error: Formato de correo inválido (debe incluir '@' y '.').")

            # 5. Validación Estado
            print("\nSeleccione Estado:")
            print(" 1. Cliente potencial")
            print(" 2. Alto interés")
            print(" 3. En proceso de compra")
            print(" 4. Cliente efectivo")
            print(" 5. Super cliente")
            
            estado_nuevo = ""
            while True:
                op_estado = input(">> Opción (1-5): ").strip()
                match op_estado:
                    case "1":
                        estado_nuevo = "Cliente potencial"
                        break
                    case "2":
                        estado_nuevo = "Alto interés"
                        break
                    case "3":
                        estado_nuevo = "En proceso de compra"
                        break
                    case "4":
                        estado_nuevo = "Cliente efectivo"
                        break
                    case "5":
                        estado_nuevo = "Super cliente"
                        break
                    case _:
                        print("❌ Opción incorrecta. Intente nuevamente.")

            # Guardar
            nuevo_cliente = {
                "id": id_nuevo,
                "nombre_completo": nombre_nuevo,
                "correo": correo_nuevo,
                "telefono": telefono_nuevo,
                "estado": estado_nuevo
            }
            clients.append(nuevo_cliente)
            
            print("\n" + "═" * 60)
            print("✅ ¡CLIENTE REGISTRADO CON ÉXITO!".center(60))
            print("═" * 60)
            print(f"ID: {id_nuevo} | Nombre: {nombre_nuevo}")
            #time.sleep(1.5)

        # ==========================================
        # CASO 4: SALIR
        # ==========================================
        case "4":
            print("\nCerrando sistema... ¡Hasta pronto!")
            break

        # ==========================================
        # CASO POR DEFECTO
        # ==========================================
        case _:
            print("❌ Opción no reconocida. Por favor ingrese un número del 1 al 4.")