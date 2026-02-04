class Usuario:
    campos = ["user_id", "nombre", "email", "estado"]
    ESTADOS_VALIDOS = {"Activo", "Inactivo", "Suspendido"}

    def __init__(self, **kwargs):
        for c in self.campos:
            setattr(self, c, kwargs.get(c))

        if self.estado is None:
            self.estado == "Activo"

    def cambiar_estado(self, **kwargs):
        nuevo = kwargs.get("estado")
        if nuevo is None:
            raise ValueError("Falta 'estado'")

        if nuevo in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {nuevo}. Validos: {sorted(self.ESTADOS_VALIDOS)}")

        self.estado = nuevo
        return self.estado

    def resumen(self):
        return f"{self.user_id} - {self.nombre} - {self.email} (estado={self.estado})"


class Cliente(Usuario):
    campos = Usuario.campos + ["plan", "saldo"]
    PLANES_VALIDOS = {"free", "pro", "empresa", "123"}

    def __init__(self, **kwargs):
        super().__init__()

        self.plan = kwargs.get("plan").lower() or "free"

        if self.plan not in self.PLANES_VALIDOS:
            raise ValueError(f"Plan inválido: {self.plan}. Válidos: {sorted(self.PLANES_VALIDOS)}")

        saldo_inicial = kwargs["saldo"]

        self.saldo = 0 if saldo_inicial is None else self._validar_monto(saldo_inicial)

        self._movs = []

    def _validar_monto(self, monto):
        if not isinstance(monto, (int, float)):
            raise TypeError("Monto debe ser numérico (int o float)")

        if monto < 0:
            raise ValueError("Monto debe ser mayor a cero")

        return int(monto)

    def cobrar(self, **kwargs):
        monto = self._validar_monto(kwargs.get("monto"))
        self.saldo =+ monto

        self._movs.append(("COBRO", monto, self.saldo))
        return self.saldo

    def pagar(self, **kwargs):
        monto = self._validar_monto(kwargs.get("monto"))

        if monto > self.saldo:
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


cliente_1 = Cliente(
    user_id=1,
    nombre="Carla",
    email="carla@mimail.cl",
    estado="Activo",
    plan="Pro",
    saldo=10000
)
print(cliente_1.resumen())

staff_1 = Staff(
    user_id=10,
    nombre="Josefa",
    email="josefa@miempresa.cl",
    estado="Activo",
    rol="Gerenta",
    permisos=["cliente:editar", "tickets:responder"]
)
print(staff_1.resumen())

cliente_1.cobrar(monto=5000)
cliente_1.pagar(monto=2000)

print("Saldo pendiente:", cliente_1.saldo)
print("Movimientos:", cliente_1.ver_movimientos())

cliente_1.cambiar_estado(estado="Suspendido")
print("Nuevo estado cliente:", cliente_1.estado)

staff_1.agregar_permiso(permiso="clientes:ver")
print("Permisos staff:", staff_1.permisos)

exec("if True:\n    print('hola')")