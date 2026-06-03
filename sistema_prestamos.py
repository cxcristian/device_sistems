""" Excepciones personalizadas """

class ErrorSistemaPrestamos(Exception):
    """ Excepción para préstamos inválidos """
    pass

class EquipoNoDisponible(ErrorSistemaPrestamos):
    """Se lanza cuando el equipo ya está prestado."""
    def __init__(self, codigo: str):
        super().__init__(f"El equipo '{codigo}' no está disponible para préstamo.")
        self.codigo = codigo

class EquipoNoEncontrado(ErrorSistemaPrestamos):
    """Se lanza cuando el código de equipo no existe."""
    def __init__(self, codigo: str):
        super().__init__(f"El equipo '{codigo}' no existe en el inventario.")
        self.codigo = codigo

class PrestamoNoEncontrado(ErrorSistemaPrestamos):
    """Se lanza cuando no hay préstamo activo para un equipo."""
    def __init__(self, codigo: str):
        super().__init__(f"No hay préstamo activo para el equipo '{codigo}'.")
        self.codigo = codigo


# Inventario en memoria (diccionario principal)
inventario: dict[str, dict] = {
    "PC-001": {"nombre": "Dell Inspiron 15",  "disponible": True,  "historial": []},
    "PC-002": {"nombre": "HP ProBook 440",    "disponible": True,  "historial": []},
    "PC-003": {"nombre": "Lenovo ThinkPad",   "disponible": False, "historial": ["Ana López"]},
}

def validar_equipo(codigo: str) -> dict:
    """Valida que el equipo exista y retorna sus datos."""
    try:
        equipo = inventario[codigo]          # KeyError si no existe
    except KeyError:
        raise EquipoNoEncontrado(codigo)
    return equipo

def registrar_prestamo(codigo: str, usuario: str) -> None:
    """Registra un préstamo validando disponibilidad."""
    equipo = validar_equipo(codigo)          # puede lanzar EquipoNoEncontrado

    if not equipo["disponible"]:
        raise EquipoNoDisponible(codigo)

    equipo["disponible"] = False
    equipo["historial"].append(usuario)
    print(f"✅  Préstamo registrado: {codigo} → {usuario}")


def registrar_devolucion(codigo: str) -> None:
    """Registra la devolución de un equipo."""
    equipo = validar_equipo(codigo)

    if equipo["disponible"]:
        raise PrestamoNoEncontrado(codigo)

    equipo["disponible"] = True
    print(f"🔄  Devolución registrada: {codigo}")


# ── PRUEBA RÁPIDA ──────────────────────────────────
if __name__ == "__main__":
    operaciones = [
        ("préstamo",    "PC-001", "Carlos Ruiz"),
        ("préstamo",    "PC-001", "María García"),   # debe fallar
        ("préstamo",    "PC-999", "Juan Pérez"),     # debe fallar
        ("devolución",  "PC-001", None),
        ("devolución",  "PC-002", None),             # debe fallar
    ]

    for tipo, codigo, usuario in operaciones:
        try:
            if tipo == "préstamo":
                registrar_prestamo(codigo, usuario)
            else:
                registrar_devolucion(codigo)
        except ErrorSistemaPrestamos as e:
            print(f"[ERROR] {e}")
        finally:
            print(f"  → Operación '{tipo}' procesada para {codigo}\n")