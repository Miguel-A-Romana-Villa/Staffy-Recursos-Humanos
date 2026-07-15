from sqlalchemy.orm import Session

from app.db.models import BoletaDB, EmpleadoDB
from app.domain.boleta import Boleta
from app.schemas.boleta_schema import BoletaCreate
from app.services.sueldo_service import SueldoService


class BoletaService:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[dict]:
        boletas = self.db.query(BoletaDB).order_by(BoletaDB.id.desc()).all()
        return [self._to_response(item) for item in boletas]

    def listar_por_empleado(self, empleado_codigo: str) -> list[dict]:
        boletas = (
            self.db.query(BoletaDB)
            .join(EmpleadoDB, BoletaDB.empleado_id == EmpleadoDB.id)
            .filter(EmpleadoDB.codigo.ilike(empleado_codigo.strip()))
            .order_by(BoletaDB.id.desc())
            .all()
        )
        return [self._to_response(item) for item in boletas]

    def generar(self, payload: BoletaCreate) -> dict:
        sueldo_service = SueldoService(self.db)
        resultado = sueldo_service.calcular(
            empleado_codigo=payload.empleado_codigo,
            periodo=payload.periodo,
            bonos_extra=payload.bonos,
            descuentos_extra=payload.descuentos,
        )
        empleado = sueldo_service.obtener_empleado(payload.empleado_codigo)
        boleta = BoletaDB(
            empleado_id=empleado.id,
            periodo=resultado["periodo"],
            sueldo_base=resultado["sueldo_base"],
            bonos=resultado["bonos"],
            descuentos=resultado["descuentos"],
            sueldo_neto=resultado["sueldo_neto"],
        )
        self.db.add(boleta)
        self.db.commit()
        self.db.refresh(boleta)
        return self._to_response(boleta)

    def _to_response(self, item: BoletaDB) -> dict:
        boleta = Boleta(
            id=item.id,
            empleado_codigo=item.empleado.codigo,
            empleado_nombre=f"{item.empleado.nombres} {item.empleado.apellidos}",
            dni=item.empleado.dni,
            cargo=item.empleado.cargo,
            periodo=item.periodo,
            sueldo_base=item.sueldo_base,
            bonos=item.bonos,
            descuentos=item.descuentos,
        )
        return boleta.to_dict()
