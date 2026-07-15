from pydantic import BaseModel, ConfigDict, Field


class ConceptoPagoBase(BaseModel):
    empleado_id: int
    tipo: str
    concepto: str
    monto: float = Field(gt=0)
    periodo: str


class ConceptoPagoCreate(ConceptoPagoBase):
    pass


class ConceptoPagoResponse(ConceptoPagoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
