'''def calcular_valor_pan():
    # Valor por kilo de pan
    VALOR_POR_KILO = 1000
    
    try:
        # Solicitar el peso en kilogramos
        peso = float(input("Ingrese el peso del pan en kilogramos: "))
        
        # Validar que el peso sea positivo
        if peso <= 0:
            return "Error: El peso debe ser mayor a 0."
        
        # Solicitar el tipo de pan
        tipo_pan = input("Ingrese el tipo de pan: ").strip()
        
        # Calcular el valor total
        valor_total = peso * VALOR_POR_KILO
        
        # Mostrar el resultado
        resultado = f"""
        ===== RECIBO =====
        Tipo de pan: {tipo_pan}
        Peso: {peso} kg
        Precio por kilo: ${VALOR_POR_KILO}
        Total a pagar: ${valor_total:,.0f}
        ==================
        """
        return resultado
        
    except ValueError:
        return "Error: Debe ingresar un número válido para el peso."

# Ejemplo de uso
print(calcular_valor_pan())'''

'''
def precio_pan(peso, tipo):
    precios = {'marraqueta': 2220, 'hallulla': 2100}  
    return peso * precios.get(tipo.lower(), 0)

peso = float(input("Peso (kg): "))
tipo = input("Tipo (marraqueta/hallulla): ")
total = precio_pan(peso, tipo)
print(f"Valor a pagar: ${total:,.0f} CLP" if total else "Tipo inválido.")'''


'''def calcular_total():
    precios = {
        "blanco": 2000,
        "integral": 2500,
        "centeno": 3000
    }

    peso = float(input("Ingrese el peso en kilos: "))
    tipo_pan = input("Ingrese el tipo de pan (blanco/integral/centeno): ").lower()

    if tipo_pan not in precios:
        return "Tipo de pan no válido"

    total = peso * precios[tipo_pan]
    return total'''
'''
print("Total a pagar:", calcular_total())

def valor_pan_pagar(kilos_pan, tipo_pan):
    if tipo_pan == "1":
        return kilos_pan * 1990
    elif tipo_pan == "2":
        return kilos_pan * 2450
    else:
        return "Tipo de pan no válido"


kilos_pan = int(input("Ingrese la cantidad de kilos de pan: "))
tipo_pan = input("Ingrese el tipo de pan:\n 1) Hallula\n 2) Marraqueta\n ")

precio_final = valor_pan_pagar(kilos_pan, tipo_pan)
print("El precio final es:", precio_final)'''

'''
def calcular_pago_pan(peso_kg, tipo_pan):
    # Precios referenciales por kilo (CLP)
    precios = {
        "pan batido": 2000,
        "hallulla": 2200,
        "amasado": 3000,
        "colisa": 1500
    }
    
    # Convertir a minúsculas para evitar errores de tipeo
    tipo = tipo_pan.lower()
    
    if tipo in precios:
        total = peso_kg * precios[tipo]
        return f"El valor a pagar por {peso_kg}kg de {tipo} es: ${round(total)}"
    else:
        return "Lo sentimos, ese tipo de pan no está en nuestro inventario."

resultado = calcular_pago_pan(1.5, "colisa")
print(resultado)
'''

'''
def calcular_precio_pan(tipo_pan, peso_pan):
    # Precios por kilogramo
    precios = {
        "marraqueta": 1.5,  # Precio por kg de marraqueta
        "hallulla": 1.2      # Precio por kg de hallulla
    }
    
    # Verificar si el tipo de pan es válido
    if tipo_pan in precios:
        # Calcular el precio
        precio = precios[tipo_pan] * peso_pan
        return precio
    else:
        return "Tipo de pan no válido. Usa 'marraqueta' o 'hallulla'."

# Solicitar al usuario el tipo de pan y el peso
tipo_pan = input("Ingrese el tipo de pan (marraqueta, hallulla): ").lower()
peso_pan = float(input("Ingrese el peso del pan en kg: "))

# Calcular y mostrar el precio
precio_total = calcular_precio_pan(tipo_pan, peso_pan)
print(f"El precio total del pan es: ${precio_total:.2f}")'''

# 1. BASE DE DATOS: Definimos los precios
'''precios = {
    "hallulla": 2190,
    "marraqueta": 2190,
    "dobladita": 2790
}

print("--- CIBERPAN ---")
print(precios)


# 2. ENTRADA DE DATOS (INPUTS)
# Aquí el programa se DETIENE y espera que escribas el nombre
tipo_pan = input("Ingrese el tipo de pan: ")

# Aquí pedimos el peso.
# IMPORTANTE: input() siempre entrega Texto.
# Debemos envolverlo en float() para convertir ese texto en un Número Decimal.
peso_ingresado = float(input("Ingrese el peso en Kg (ej: 0.5): "))

# 3. PROCESO Y SALIDA
if tipo_pan in precios:
    # Buscamos el precio en la base de datos
    precio_por_kilo = precios[tipo_pan]
    
    # Hacemos la multiplicación
    total = precio_por_kilo * peso_ingresado
    
    # Mostramos el resultado
    # int(total) sirve para mostrar el precio sin decimales (CLP)
    print(f"Lleva {peso_ingresado} kg de {tipo_pan}.")
    print(f"Total a pagar: ${int(total)}")
else:
    print("Error: No nos queda de ese pan, salga de CIBERPAN y vuelva a entrar por favor.")'''



'''
def calcular_precio(peso, tipo_pan):
    precios = {
        "marraqueta": 2300,
        "hallulla": 2100,
        "integral": 2800
    }

    tipo_pan = tipo_pan.lower()

    if tipo_pan in precios:
        total = peso * precios[tipo_pan]
        return total
    else:
        return "Tipo de pan no válido"

peso = float(input("Ingrese el peso en kilos: "))
tipo = input("Ingrese el tipo de pan: ")

resultado = calcular_precio(peso, tipo)

print("Total a pagar: $", resultado)'''
