from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import EmpleadoDB
from app.domain.empleado_factory import EmpleadoFactory
from app.domain.exceptions import EmpleadoDuplicadoError
from app.schemas.empleado_schema import EmpleadoCreate, EmpleadoUpdate


class EmpleadoService:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, search: Optional[str] = None) -> list[EmpleadoDB]:
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
        data = payload.model_dump()
        EmpleadoFactory.crear(data)
        self._validar_duplicado(data["codigo"], data["dni"])
        empleado = EmpleadoDB(**data)
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def actualizar(self, empleado_id: int, payload: EmpleadoUpdate) -> Optional[EmpleadoDB]:
        empleado = self.db.query(EmpleadoDB).filter(EmpleadoDB.id == empleado_id).first()
        if empleado is None:
            return None

        cambios = payload.model_dump(exclude_unset=True)
        data = self._to_dict(empleado)
        data.update(cambios)
        EmpleadoFactory.crear(data)

        if "codigo" in cambios or "dni" in cambios:
            self._validar_duplicado(data["codigo"], data["dni"], empleado_id)

        for key, value in cambios.items():
            setattr(empleado, key, value)

        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def obtener(self, empleado_id: int) -> Optional[EmpleadoDB]:
        return self.db.query(EmpleadoDB).filter(EmpleadoDB.id == empleado_id).first()

    def obtener_por_codigo(self, codigo: str) -> Optional[EmpleadoDB]:
        return self.db.query(EmpleadoDB).filter(EmpleadoDB.codigo.ilike(codigo.strip())).first()

    def _validar_duplicado(self, codigo: str, dni: str, empleado_id: Optional[int] = None) -> None:
        query = self.db.query(EmpleadoDB).filter((EmpleadoDB.codigo == codigo) | (EmpleadoDB.dni == dni))
        if empleado_id is not None:
            query = query.filter(EmpleadoDB.id != empleado_id)
        if query.first() is not None:
            raise EmpleadoDuplicadoError("codigo o DNI")

    def _to_dict(self, empleado: EmpleadoDB) -> dict:
        return {
            "id": empleado.id,
            "codigo": empleado.codigo,
            "dni": empleado.dni,
            "correo": empleado.correo,
            "telefono": empleado.telefono,
            "nombres": empleado.nombres,
            "apellidos": empleado.apellidos,
            "cargo": empleado.cargo,
            "sueldo_base": empleado.sueldo_base,
            "tipo": empleado.tipo,
            "horas_trabajadas": empleado.horas_trabajadas,
            "tarifa_por_hora": empleado.tarifa_por_hora,
            "hijos": empleado.hijos,
            "fecha_nacimiento": empleado.fecha_nacimiento,
            "fecha_inicio": empleado.fecha_inicio,
            "fecha_cese": empleado.fecha_cese,
            "regimen_pensionario": empleado.regimen_pensionario,
            "foto_url": empleado.foto_url,
            "activo": empleado.activo,
        }


def obtener_rango_periodo(periodo: str) -> tuple[date, date]:
    anio, mes = [int(part) for part in periodo.split("-")]
    inicio = date(anio, mes, 1)
    if mes == 12:
        fin = date(anio, 12, 31)
    else:
        siguiente_mes = date(anio, mes + 1, 1)
        fin = date.fromordinal(siguiente_mes.toordinal() - 1)

    return inicio, fin
