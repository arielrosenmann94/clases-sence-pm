def precio_pan(kg, tipo):
    # precios por kilo
    valor_hallulla = 1500
    valor_marraqueta = 2000
    valor_amasado = 3000

    tipo = tipo.strip().lower()

    if tipo == "marraqueta":
        return valor_marraqueta * kg
    elif tipo == "hallulla":
        return valor_hallulla * kg
    elif tipo == "amasado":
        return valor_amasado * kg
    else:
        return None  

def mostrar_menu():
    print("\n=== MENÚ PANADERÍA ===")
    print("1) Calcular precio")
    print("2) Salir")


def pedir_kg():
    while True:
        entrada = input("Ingrese kilos: ").strip()
        try:
            kg = float(entrada)
            if kg <= 0:
                print("Los kilos deben ser mayores a 0.")
                continue
            return kg
        except ValueError:
            print("Entrada inválida. Debes escribir un número (ej: 1.5).")


def pedir_tipo():
    while True:
        tipo = input("Tipo de pan (marraqueta/hallulla/amasado): ").strip().lower()
        if tipo in ("marraqueta", "hallulla", "amasado"):
            return tipo
        print("Tipo inválido. Opciones: marraqueta, hallulla, amasado.")


def main():
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            kg = pedir_kg()
            tipo = pedir_tipo()

            total = precio_pan(kg, tipo)
            if total is None:
                print("Tipo de pan no reconocido.")
            else:
                print(f"Total por {kg} kg de {tipo}: ${int(total)}")

        elif opcion == "2":
            print("Saliendo... gracias.")
            break
        else:
            print("Opción inválida. Elige 1 o 2.")


main()
