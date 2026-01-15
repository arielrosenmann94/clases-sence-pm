MAPEO_ESTADOS = {
    "1": "Cliente potencial",
    "2": "Alto interés",
    "3": "En proceso de compra",
    "4": "Cliente efectivo",
    "5": "Super cliente"
}

base_de_clientes = []

print("Registro de Nuevo Cliente\n")

# Validación ID (debe tener 6 dígitos exactos)
while True:
    id_cliente = input("ID (6 dígitos): ").strip()
    if id_cliente.isdigit() and len(id_cliente) == 6:
        id_cliente = int(id_cliente)
        break
    print("Error: El ID debe tener exactamente 6 números.")

# Validación Nombre (mínimo 2 palabras)
while True:
    nombre_completo = input("Nombre completo: ").strip()
    if len(nombre_completo.split()) >= 2:
        break
    print("Error: Ingrese al menos nombre y apellido.")

# 3. Validación Teléfono (Numérico y min 8 dígitos)
while True:
    telefono = input("Teléfono (min 8 dígitos): ").strip()
    if telefono.isdigit() and len(telefono) >= 8:
        break
    print("Error: Teléfono inválido (solo números, min 8 dígitos).")

# 4. Validación Correo (Debe tener @ y .)
while True:
    correo = input("Correo electrónico: ").strip()
    if "@" in correo and "." in correo:
        break
    print("Error: Formato de correo no válido.")

# 5. Validación de Estado (Mapeo numérico)
while True:
    print("\nSeleccione el estado del cliente:")
    for num, texto in MAPEO_ESTADOS.items():
        print(f"{num}: {texto}")
    
    opcion = input("Seleccione una opción (1-5): ")
    if opcion in MAPEO_ESTADOS:
        estado_texto = MAPEO_ESTADOS[opcion]
        break
    print("Error: Opción no válida.")

# Registro final
nuevo_cliente = {
    "id": id_cliente,
    "nombre_completo": nombre_completo,
    "telefono": telefono,
    "correo": correo,
    "estado": estado_texto
}

base_de_clientes.append(nuevo_cliente)

print(f"\nCliente '{nombre_completo}' agregado con éxito.")
print("Diccionario generado:", nuevo_cliente)