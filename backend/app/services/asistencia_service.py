from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import AsistenciaDB, EmpleadoDB
from app.domain.asistencia import Asistencia
from app.domain.exceptions import DatoInvalidoError, EmpleadoNoEncontradoError
from app.schemas.asistencia_schema import AsistenciaCreate
from app.services.empleado_service import obtener_rango_periodo


class AsistenciaService:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, empleado_id: Optional[int] = None, periodo: Optional[str] = None) -> list[AsistenciaDB]:
        query = self.db.query(AsistenciaDB)

        if empleado_id is not None:
            query = query.filter(AsistenciaDB.empleado_id == empleado_id)

        if periodo:
            inicio_periodo, fin_periodo = obtener_rango_periodo(periodo)
            query = query.filter(AsistenciaDB.fecha >= inicio_periodo).filter(AsistenciaDB.fecha <= fin_periodo)

        return query.order_by(AsistenciaDB.fecha).all()

    def registrar_o_actualizar(self, payload: AsistenciaCreate) -> AsistenciaDB:
        self._validar(payload)
        asistencia = (
            self.db.query(AsistenciaDB)
            .filter(AsistenciaDB.empleado_id == payload.empleado_id)
            .filter(AsistenciaDB.fecha == payload.fecha)
            .first()
        )

        if asistencia is None:
            asistencia = AsistenciaDB(**payload.model_dump())
            self.db.add(asistencia)
        else:
            asistencia.estado = payload.estado
            asistencia.minutos_tardanza = payload.minutos_tardanza
            asistencia.comentario = payload.comentario

        self.db.commit()
        self.db.refresh(asistencia)
        return asistencia

    def eliminar_por_fecha(self, empleado_id: int, fecha: date) -> bool:
        asistencia = (
            self.db.query(AsistenciaDB)
            .filter(AsistenciaDB.empleado_id == empleado_id)
            .filter(AsistenciaDB.fecha == fecha)
            .first()
        )

        if asistencia is None:
            return False

        self.db.delete(asistencia)
        self.db.commit()
        return True

    def _validar(self, payload: AsistenciaCreate) -> None:
        empleado = self.db.query(EmpleadoDB).filter(EmpleadoDB.id == payload.empleado_id).first()
        if empleado is None:
            raise EmpleadoNoEncontradoError(str(payload.empleado_id))

        estado = payload.estado.upper()
        if estado not in ["ASISTIO", "TARDE", "FALTO"]:
            raise DatoInvalidoError("El estado de asistencia no es valido")
        if payload.minutos_tardanza is not None and payload.minutos_tardanza < 0:
            raise DatoInvalidoError("Los minutos de tardanza no pueden ser negativos")

        payload.estado = estado
        Asistencia(
            empleado_id=payload.empleado_id,
            fecha=payload.fecha,
            estado=payload.estado,
            minutos_tardanza=payload.minutos_tardanza,
            comentario=payload.comentario,
        )
