from app.domain.empleado import Empleado, EmpleadoMedioTiempo, EmpleadoTiempoCompleto
from app.domain.exceptions import DatoInvalidoError


class EmpleadoFactory:
    @staticmethod
    def crear(data: dict) -> Empleado:
        EmpleadoFactory.validar(data)
        tipo = data.get("tipo", "tiempo_completo")
        payload = {
            key: value
            for key, value in data.items()
            if key not in ["tipo", "horas_trabajadas", "tarifa_por_hora"]
        }
        payload.setdefault("id", None)

        if tipo == "medio_tiempo":
            return EmpleadoMedioTiempo(
                horas_trabajadas=data.get("horas_trabajadas") or 0,
                tarifa_por_hora=data.get("tarifa_por_hora") or 0,
                **payload,
            )

        return EmpleadoTiempoCompleto(**payload)

    @staticmethod
    def validar(data: dict) -> None:
        codigo = str(data.get("codigo", "")).strip()
        dni = str(data.get("dni", "")).strip()
        nombres = str(data.get("nombres", "")).strip()
        apellidos = str(data.get("apellidos", "")).strip()
        cargo = str(data.get("cargo", "")).strip()
        tipo = data.get("tipo", "tiempo_completo")
        sueldo_base = float(data.get("sueldo_base", 0) or 0)

        if not codigo:
            raise DatoInvalidoError("El codigo es obligatorio")
        if not dni or not dni.isdigit() or len(dni) != 8:
            raise DatoInvalidoError("El DNI debe tener 8 digitos")
        if not nombres or not apellidos:
            raise DatoInvalidoError("Los nombres y apellidos son obligatorios")
        if not cargo:
            raise DatoInvalidoError("El cargo es obligatorio")
        if sueldo_base <= 0:
            raise DatoInvalidoError("El sueldo base debe ser mayor a cero")
        if tipo not in ["tiempo_completo", "medio_tiempo"]:
            raise DatoInvalidoError("El tipo de empleado no es valido")
        if tipo == "medio_tiempo":
            if float(data.get("horas_trabajadas", 0) or 0) <= 0:
                raise DatoInvalidoError("Las horas trabajadas deben ser mayores a cero")
            if float(data.get("tarifa_por_hora", 0) or 0) <= 0:
                raise DatoInvalidoError("La tarifa por hora debe ser mayor a cero")
