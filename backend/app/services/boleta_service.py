from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import BoletaDB, EmpleadoDB
from app.domain.boleta import Boleta
from app.domain.exceptions import BoletaDuplicadaError
from app.schemas.boleta_schema import BoletaCreate
from app.services.sueldo_service import SueldoService


class BoletaService:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[dict]:
        boletas = self.db.query(BoletaDB).order_by(BoletaDB.id.desc()).all()
        return [self._to_response(item) for item in boletas]

    def listar_por_empleado(self, empleado_codigo: str) -> list[dict]:
        codigo = empleado_codigo.strip()
        boletas = (
            self.db.query(BoletaDB)
            .join(EmpleadoDB, BoletaDB.empleado_id == EmpleadoDB.id)
            .filter(or_(EmpleadoDB.codigo.ilike(codigo), BoletaDB.empleado_codigo.ilike(codigo)))
            .order_by(BoletaDB.id.desc())
            .all()
        )
        return [self._to_response(item) for item in boletas]

    def generar(self, payload: BoletaCreate) -> dict:
        sueldo_service = SueldoService(self.db)
        periodo = Boleta.normalizar_periodo(payload.periodo)
        empleado = sueldo_service.obtener_empleado(payload.empleado_codigo)
        existente = (
            self.db.query(BoletaDB)
            .filter(BoletaDB.empleado_id == empleado.id, BoletaDB.periodo == periodo)
            .first()
        )
        if existente is not None:
            raise BoletaDuplicadaError(empleado.codigo, periodo)

        boleta = sueldo_service.calcular_boleta(
            empleado_codigo=payload.empleado_codigo,
            periodo=periodo,
            bonos_extra=payload.bonos,
            descuentos_extra=payload.descuentos,
        )
        registro = BoletaDB(
            empleado_id=empleado.id,
            empleado_codigo=boleta.empleado_codigo,
            empleado_nombre=boleta.empleado_nombre,
            dni=boleta.dni,
            cargo=boleta.cargo,
            periodo=boleta.periodo,
            sueldo_base=boleta.sueldo_base,
            bonos=boleta.bonos,
            descuentos=boleta.descuentos,
            sueldo_neto=boleta.calcular_sueldo_neto(),
        )
        self.db.add(registro)
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise BoletaDuplicadaError(empleado.codigo, periodo) from exc
        self.db.refresh(registro)
        boleta.id = registro.id
        return boleta.to_dict()

    def _to_response(self, item: BoletaDB) -> dict:
        boleta = Boleta(
            id=item.id,
            empleado_codigo=item.empleado_codigo or item.empleado.codigo,
            empleado_nombre=item.empleado_nombre or f"{item.empleado.nombres} {item.empleado.apellidos}",
            dni=item.dni or item.empleado.dni,
            cargo=item.cargo or item.empleado.cargo,
            periodo=item.periodo,
            sueldo_base=item.sueldo_base,
            bonos=item.bonos,
            descuentos=item.descuentos,
        )
        return boleta.to_dict()
