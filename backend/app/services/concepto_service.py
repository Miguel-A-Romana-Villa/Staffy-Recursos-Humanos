from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import ConceptoPagoDB, EmpleadoDB
from app.domain.concepto_pago import ConceptoPago
from app.domain.exceptions import DatoInvalidoError, EmpleadoNoEncontradoError
from app.schemas.concepto_schema import ConceptoPagoCreate


class ConceptoPagoService:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, empleado_id: Optional[int] = None, periodo: Optional[str] = None) -> list[ConceptoPagoDB]:
        query = self.db.query(ConceptoPagoDB)
        if empleado_id is not None:
            query = query.filter(ConceptoPagoDB.empleado_id == empleado_id)
        if periodo:
            query = query.filter(ConceptoPagoDB.periodo == periodo.strip())
        return query.order_by(ConceptoPagoDB.id.desc()).all()

    def registrar(self, payload: ConceptoPagoCreate) -> ConceptoPagoDB:
        data = payload.model_dump()
        data["tipo"] = data["tipo"].upper()
        data["periodo"] = data["periodo"].strip()
        data["concepto"] = data["concepto"].strip()
        self._validar(data)

        concepto = ConceptoPagoDB(**data)
        self.db.add(concepto)
        self.db.commit()
        self.db.refresh(concepto)
        return concepto

    def _validar(self, data: dict) -> None:
        if self.db.query(EmpleadoDB).filter(EmpleadoDB.id == data["empleado_id"]).first() is None:
            raise EmpleadoNoEncontradoError(str(data["empleado_id"]))
        if data["tipo"] not in ["BONO", "DESCUENTO"]:
            raise DatoInvalidoError("El tipo debe ser BONO o DESCUENTO")
        if not data["concepto"]:
            raise DatoInvalidoError("El concepto es obligatorio")
        if not data["periodo"]:
            raise DatoInvalidoError("El periodo es obligatorio")
        if data["monto"] <= 0:
            raise DatoInvalidoError("El monto debe ser mayor a cero")
        ConceptoPago(**data)
