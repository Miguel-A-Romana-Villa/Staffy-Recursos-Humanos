from typing import Iterable, Optional

from app.domain.empleado import Empleado
from app.domain.empleado_factory import EmpleadoFactory
from app.domain.exceptions import EmpleadoNoEncontradoError


class GestorEmpleados:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        cls._instance = None

    def crear_empleado(self, data: dict) -> Empleado:
        return EmpleadoFactory.crear(data)

    def convertir_lista(self, empleados: Iterable) -> list[Empleado]:
        return [self.crear_empleado(self._to_dict(item)) for item in empleados]

    def buscar_por_codigo(self, empleados: Iterable, codigo: str) -> Optional[Empleado]:
        codigo_limpio = codigo.strip().lower()
        for empleado in self.convertir_lista(empleados):
            if empleado.codigo.lower() == codigo_limpio:
                return empleado
        return None

    def obtener_por_codigo(self, empleados: Iterable, codigo: str) -> Empleado:
        empleado = self.buscar_por_codigo(empleados, codigo)
        if empleado is None:
            raise EmpleadoNoEncontradoError(codigo)
        return empleado

    def _to_dict(self, item) -> dict:
        if isinstance(item, dict):
            return item
        return {
            "id": item.id,
            "codigo": item.codigo,
            "dni": item.dni,
            "nombres": item.nombres,
            "apellidos": item.apellidos,
            "cargo": item.cargo,
            "sueldo_base": item.sueldo_base,
            "correo": item.correo,
            "telefono": item.telefono,
            "hijos": item.hijos,
            "fecha_nacimiento": item.fecha_nacimiento,
            "fecha_inicio": item.fecha_inicio,
            "fecha_cese": item.fecha_cese,
            "regimen_pensionario": item.regimen_pensionario,
            "foto_url": item.foto_url,
            "activo": item.activo,
            "tipo": getattr(item, "tipo", "tiempo_completo"),
            "horas_trabajadas": getattr(item, "horas_trabajadas", None),
            "tarifa_por_hora": getattr(item, "tarifa_por_hora", None),
        }
