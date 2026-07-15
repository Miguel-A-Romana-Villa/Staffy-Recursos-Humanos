from sqlalchemy.orm import Session

from app.db.models import ConceptoPagoDB, EmpleadoDB
from app.domain.calculadora_sueldo import CalculadoraSueldo
from app.domain.concepto_pago import ConceptoPago
from app.domain.empleado_factory import EmpleadoFactory
from app.domain.exceptions import EmpleadoNoEncontradoError


class SueldoService:
    def __init__(self, db: Session):
        self.db = db

    def obtener_empleado(self, empleado_codigo: str) -> EmpleadoDB:
        empleado = self.db.query(EmpleadoDB).filter(EmpleadoDB.codigo.ilike(empleado_codigo.strip())).first()
        if empleado is None:
            raise EmpleadoNoEncontradoError(empleado_codigo)
        return empleado

    def calcular(
        self,
        empleado_codigo: str,
        periodo: str,
        bonos_extra: float = 0,
        descuentos_extra: float = 0,
    ) -> dict:
        empleado_db = self.obtener_empleado(empleado_codigo)
        empleado = EmpleadoFactory.crear(self._empleado_to_dict(empleado_db))
        conceptos = self._conceptos(empleado_db.id, periodo)
        resultado = CalculadoraSueldo().calcular(
            empleado=empleado,
            periodo=periodo,
            conceptos=conceptos,
            bonos_extra=bonos_extra,
            descuentos_extra=descuentos_extra,
        )
        resultado["conceptos"] = [
            {"tipo": item.tipo, "concepto": item.concepto, "monto": item.monto, "periodo": item.periodo}
            for item in conceptos
        ]
        return resultado

    def _conceptos(self, empleado_id: int, periodo: str) -> list[ConceptoPago]:
        conceptos = (
            self.db.query(ConceptoPagoDB)
            .filter(ConceptoPagoDB.empleado_id == empleado_id)
            .filter(ConceptoPagoDB.periodo == periodo.strip())
            .all()
        )
        return [
            ConceptoPago(
                id=item.id,
                empleado_id=item.empleado_id,
                tipo=item.tipo,
                concepto=item.concepto,
                monto=item.monto,
                periodo=item.periodo,
            )
            for item in conceptos
        ]

    def _empleado_to_dict(self, empleado: EmpleadoDB) -> dict:
        return {
            "id": empleado.id,
            "codigo": empleado.codigo,
            "dni": empleado.dni,
            "nombres": empleado.nombres,
            "apellidos": empleado.apellidos,
            "cargo": empleado.cargo,
            "sueldo_base": empleado.sueldo_base,
            "correo": empleado.correo,
            "telefono": empleado.telefono,
            "hijos": empleado.hijos,
            "fecha_nacimiento": empleado.fecha_nacimiento,
            "fecha_inicio": empleado.fecha_inicio,
            "fecha_cese": empleado.fecha_cese,
            "regimen_pensionario": empleado.regimen_pensionario,
            "foto_url": empleado.foto_url,
            "activo": empleado.activo,
            "tipo": empleado.tipo,
            "horas_trabajadas": empleado.horas_trabajadas,
            "tarifa_por_hora": empleado.tarifa_por_hora,
        }
