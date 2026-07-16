class StaffyError(Exception):
    pass


class DatoInvalidoError(StaffyError):
    pass


class EmpleadoNoEncontradoError(StaffyError):
    def __init__(self, referencia: str):
        super().__init__(f"Empleado no encontrado: {referencia}")


class EmpleadoDuplicadoError(StaffyError):
    def __init__(self, referencia: str):
        super().__init__(f"Ya existe un empleado con {referencia}")


class BoletaDuplicadaError(StaffyError):
    def __init__(self, empleado_codigo: str, periodo: str):
        super().__init__(f"Ya existe una boleta para el empleado {empleado_codigo} en el periodo {periodo}")
