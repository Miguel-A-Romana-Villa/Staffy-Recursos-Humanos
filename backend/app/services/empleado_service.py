from datetime import date

from sqlalchemy.orm import Session

from app.db.models import EmpleadoDB
from app.schemas.empleado_schema import EmpleadoCreate, EmpleadoUpdate


class EmpleadoService:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, search: str | None = None) -> list[EmpleadoDB]:
        query = self.db.query(EmpleadoDB)
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                (EmpleadoDB.nombres.ilike(pattern))
                | (EmpleadoDB.apellidos.ilike(pattern))
                | (EmpleadoDB.dni.ilike(pattern))
                | (EmpleadoDB.codigo.ilike(pattern))
            )

        return query.order_by(EmpleadoDB.id).all()

    def listar_activos_por_periodo(self, periodo: str) -> list[EmpleadoDB]:
        inicio_periodo, fin_periodo = obtener_rango_periodo(periodo)
        return (
            self.db.query(EmpleadoDB)
            .filter((EmpleadoDB.fecha_inicio.is_(None)) | (EmpleadoDB.fecha_inicio <= fin_periodo))
            .filter((EmpleadoDB.fecha_cese.is_(None)) | (EmpleadoDB.fecha_cese >= inicio_periodo))
            .order_by(EmpleadoDB.id)
            .all()
        )

    def crear(self, payload: EmpleadoCreate) -> EmpleadoDB:
        empleado = EmpleadoDB(**payload.model_dump())
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def actualizar(self, empleado_id: int, payload: EmpleadoUpdate) -> EmpleadoDB | None:
        empleado = self.db.query(EmpleadoDB).filter(EmpleadoDB.id == empleado_id).first()
        if empleado is None:
            return None

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(empleado, key, value)

        self.db.commit()
        self.db.refresh(empleado)
        return empleado


def obtener_rango_periodo(periodo: str) -> tuple[date, date]:
    anio, mes = [int(part) for part in periodo.split("-")]
    inicio = date(anio, mes, 1)
    if mes == 12:
        fin = date(anio, 12, 31)
    else:
        siguiente_mes = date(anio, mes + 1, 1)
        fin = date.fromordinal(siguiente_mes.toordinal() - 1)

    return inicio, fin
