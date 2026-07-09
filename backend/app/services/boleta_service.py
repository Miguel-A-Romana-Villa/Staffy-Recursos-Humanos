from fastapi import HTTPException
from typing import Optional

from app.models.boleta import Boleta
from app.services.json_store import JsonStore


class BoletaService:
    def __init__(self, store: Optional[JsonStore] = None):
        self.store = store or JsonStore()

    def listar(self) -> list[dict]:
        return self.store.read()["boletas"]

    def listar_por_empleado(self, empleado_codigo: str) -> list[dict]:
        return [
            boleta
            for boleta in self.listar()
            if boleta["empleado_codigo"].lower() == empleado_codigo.lower()
        ]

    def generar(self, payload: dict) -> dict:
        data = self.store.read()
        empleado = self._buscar_empleado(data["empleados"], payload["empleado_codigo"])
        periodo = payload["periodo"].strip()
        bonos = float(payload.get("bonos", 0) or 0)
        descuentos = float(payload.get("descuentos", 0) or 0)

        if not periodo:
            raise HTTPException(status_code=400, detail="El periodo es obligatorio.")
        if bonos < 0 or descuentos < 0:
            raise HTTPException(status_code=400, detail="Bonos y descuentos deben ser mayores o iguales a cero.")

        boleta = Boleta(
            id=self.store.next_id("boletas"),
            empleado_codigo=empleado["codigo"],
            empleado_nombre=f'{empleado["nombres"]} {empleado["apellidos"]}',
            dni=empleado["dni"],
            cargo=empleado["cargo"],
            periodo=periodo,
            sueldo_base=float(empleado["sueldo_base"]),
            bonos=bonos,
            descuentos=descuentos,
        ).to_dict()

        data["boletas"].append(boleta)
        self.store.write(data)
        return boleta

    def _buscar_empleado(self, empleados: list[dict], codigo: str) -> dict:
        empleado = next(
            (item for item in empleados if item["codigo"].lower() == codigo.strip().lower()),
            None,
        )
        if empleado is None:
            raise HTTPException(status_code=404, detail="Empleado no encontrado.")
        return empleado
