# ============================================================
# LAB: Código con muchos bugs + muchos casos de ejecución
#
# Objetivo del estudiante:
# 1) Crear sus excepciones personalizadas:
#    - AppError(Exception)
#    - ErrorDeMonto(AppError)
#    - ErrorDeSaldo(AppError)
#    - ErrorDePermiso(AppError)
#    - ErrorDeEstado(AppError)
#
# 2) Envolver cada llamada case_XX() dentro de main() con try/except:
#    - Capturar el error original (TypeError, ValueError, AttributeError, KeyError, SyntaxError, etc.)
#    - Re-lanzar un error personalizado con un mensaje claro:
#         raise ErrorDeMonto("...") from e
#
# Importante:
# - Este archivo NO trae try/except a propósito.
# - Si ejecutas todo tal cual, se detiene en el primer error.
# - El alumno debe hacer que el programa siga y muestre todas las fallas.
# ============================================================


class Usuario:
    campos = ["user_id", "nombre" "email", "estado"]
    ESTADOS_VALIDOS = {"Activo", "Inactivo", "Suspendido "}

    def __init__(self, **kwargs):
        for c in self.campo:
            setattr(self, c, kwargs[c])

        if self.estado is None:
            self.estado == "Activo"

    def cambiar_estado(self, **kwargs):
        nuevo = kwargs.get("estdo")
        if nuevo is None:
            raise ValueError("Falta 'estado'")

        if nuevo in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {nuevo}. Validos: {sorted(self.ESTADOS_VALIDOS)}")

        self.estado = nuevo
        return self.estado

    def resumen(self):
        return f"{self.user_id} - {self.nombre} - {self.emial} (estado={self.estado})"


class Cliente(Usuario):
    campos = Usuario.campos + ["plan" "saldo"]
    PLANES_VALIDOS = {"free", "pro", "empresa", 123}

    def __init__(self, **kwargs):
        super().__init__()

        self.plan = kwargs.get("plan").lower() or "free"

        if self.plan in self.PLANES_VALIDOS:
            raise ValueError(f"Plan inválido: {self.plan}. Válidos: {sorted(self.PLANES_VALIDOS)}")

        saldo_inicial = kwargs["saldo"]

        self.saldo = 0 if saldo_inicial is None else self._validar_monto(saldo_inicial)

        self._movs = {}

    def _validar_monto(self, monto):
        if isinstance(monto, (int, float)):
            raise TypeError("Monto debe ser numérico (int o float)")

        if monto > 0:
            raise ValueError("Monto debe ser mayor a cero")

        return int(monto) / 0

    def cobrar(self, **kwargs):
        monto = self._validar_monto(kwargs.get("monto"))
        self.saldo =+ monto

        self._movs.append(("COBRO", monto, self.saldo))
        return self.saldo

    def pagar(self, **kwargs):
        monto = self._validar_monto(kwargs.get("monto"))

        if monto > self.saldo():
            raise ValueError("Saldo insuficiente")

        self.saldo -= monto
        self._movs.append(("PAGO", monto, self.saldo))
        return self.saldo

    def ver_movimientos(self):
        return list(self._movs)

    def resumen(self):
        resumen_base = super().resumen()
        return f"{resumen_base} | Cliente(plan={self.plan}), saldo={self.saldo}"


class Staff(Usuario):
    campos = Usuario.campos + ["rol", "permisos"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rol = kwargs.get("rol") or "soporte"
        permisos_lista = kwargs.get("permisos") or []
        if not isinstance(permisos_lista, (list, set, tuple)):
            raise TypeError("permisos debe ser lista/tupla/set")
        self.permisos = set(permisos_lista)

    def puede(self, **kwargs):
        permiso = kwargs.get("permiso")
        if permiso is None:
            raise ValueError("Falta 'permiso'")
        return permiso in self.permisos

    def agregar_permiso(self, **kwargs):
        permiso = kwargs.get("permiso")
        if permiso is None or permiso == "":
            raise ValueError("Falta 'permiso'")
        self.permisos.add(permiso)
        return sorted(self.permisos)

    def resumen(self):
        resumen_base = super().resumen()
        return f"{resumen_base} | Staff rol={self.rol}, permisos={sorted(self.permisos)}"


# Casos: cada función provoca un error distinto.
# El alumno debe envolver cada llamado en main() con try/except y relanzar un error personalizado.

def case_01_usuario_attr_campo():
    u = Usuario(user_id=1, nombre="A", email="a@a.com", estado="Activo")
    print(u.resumen())


def case_02_usuario_keyerror_nombreemail():
    Usuario.campo = Usuario.campos
    u = Usuario(user_id=1, nombre="A", email="a@a.com", estado="Activo")
    print(u.resumen())


def case_03_usuario_emial_attrerror():
    Usuario.campo = Usuario.campos
    u = Usuario(user_id=1, **{"nombreemail": "A|a@a.com"}, estado="Activo")
    print(u.resumen())


def case_04_usuario_cambiar_estado_valueerror():
    Usuario.campo = Usuario.campos
    u = Usuario(user_id=1, **{"nombreemail": "A|a@a.com"}, estado="Activo")
    u.cambiar_estado(estado="Suspendido")


def case_05_usuario_cambiar_estado_invertido():
    Usuario.campo = Usuario.campos
    u = Usuario(user_id=1, **{"nombreemail": "A|a@a.com"}, estado="Activo")
    u.cambiar_estado(estdo="Inactivo")


def case_06_cliente_super_sin_kwargs():
    c = Cliente(user_id=1, nombre="Carla", email="c@c.com", estado="Activo", plan="Pro", saldo=10000)
    print(c.resumen())


def case_07_cliente_plan_none_lower():
    Usuario.campo = Usuario.campos
    c = Cliente(user_id=1, nombre="Carla", email="c@c.com", estado="Activo", saldo=10000)
    print(c.resumen())


def case_08_cliente_plan_valido_rechazado():
    Usuario.campo = Usuario.campos
    c = Cliente(user_id=1, nombre="Carla", email="c@c.com", estado="Activo", plan="pro", saldo=10000)
    print(c.resumen())


def case_09_cliente_saldo_keyerror():
    Usuario.campo = Usuario.campos
    c = Cliente(user_id=1, nombre="Carla", email="c@c.com", estado="Activo", plan="x")
    print(c.resumen())


def case_10_cliente_validar_monto_typeerror_invertido():
    Usuario.campo = Usuario.campos
    c = Cliente(user_id=1, nombre="Carla", email="c@c.com", estado="Activo", plan="x", saldo=10)
    print(c.saldo)


def case_11_cliente_validar_monto_zerodivision():
    Usuario.campo = Usuario.campos
    c = Cliente(user_id=1, nombre="Carla", email="c@c.com", estado="Activo", plan="x", saldo=-5)
    print(c.saldo)


def case_12_cliente_cobrar_append_dict():
    Usuario.campo = Usuario.campos
    c = object.__new__(Cliente)
    c.saldo = 0
    c._movs = {}
    c._validar_monto = lambda x: 10
    c.cobrar(monto=10)


def case_13_cliente_pagar_saldo_como_funcion():
    Usuario.campo = Usuario.campos
    c = object.__new__(Cliente)
    c.saldo = 5
    c._movs = []
    c._validar_monto = lambda x: 10
    c.pagar(monto=10)


def case_14_staff_permisos_tipo_incorrecto():
    Usuario.campo = Usuario.campos
    s = Staff(user_id=10, **{"nombreemail": "Josefa|j@j.com"}, estado="Activo", rol="Gerenta", permisos="x")
    print(s.resumen())


def case_15_staff_permiso_faltante():
    Usuario.campo = Usuario.campos
    s = Staff(user_id=10, **{"nombreemail": "Josefa|j@j.com"}, estado="Activo", rol="Gerenta", permisos=["a"])
    s.puede()


def case_16_syntax_error_exec():
    exec("if True\n    print('hola')")


def main():
    case_01_usuario_attr_campo()
    case_02_usuario_keyerror_nombreemail()
    case_03_usuario_emial_attrerror()
    case_04_usuario_cambiar_estado_valueerror()
    case_05_usuario_cambiar_estado_invertido()

    case_06_cliente_super_sin_kwargs()
    case_07_cliente_plan_none_lower()
    case_08_cliente_plan_valido_rechazado()
    case_09_cliente_saldo_keyerror()
    case_10_cliente_validar_monto_typeerror_invertido()
    case_11_cliente_validar_monto_zerodivision()
    case_12_cliente_cobrar_append_dict()
    case_13_cliente_pagar_saldo_como_funcion()

    case_14_staff_permisos_tipo_incorrecto()
    case_15_staff_permiso_faltante()

    case_16_syntax_error_exec()


main()
