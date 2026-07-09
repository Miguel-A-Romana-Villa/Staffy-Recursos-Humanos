from pathlib import Path

import pytest
from fastapi import HTTPException

from app.services.boleta_service import BoletaService
from app.services.json_store import JsonStore
from app.services.reporte_service import ReporteService


@pytest.fixture
def store(tmp_path: Path):
    store = JsonStore(tmp_path / "db.json")
    store.write(
        {
            "empleados": [
                {
                    "id": 1,
                    "codigo": "EMP001",
                    "dni": "45879632",
                    "nombres": "Juan",
                    "apellidos": "Ramirez",
                    "cargo": "Asistente",
                    "sueldo_base": 1800,
                    "activo": True,
                },
                {
                    "id": 2,
                    "codigo": "EMP002",
                    "dni": "42157896",
                    "nombres": "Maria",
                    "apellidos": "Lopez",
                    "cargo": "Analista",
                    "sueldo_base": 2400,
                    "activo": True,
                },
            ],
            "asistencias": [
                {"id": 1, "empleado_codigo": "EMP001", "fecha": "2026-06-24", "estado": "ASISTIO"},
                {"id": 2, "empleado_codigo": "EMP001", "fecha": "2026-06-25", "estado": "TARDE"},
                {"id": 3, "empleado_codigo": "EMP002", "fecha": "2026-06-25", "estado": "FALTO"},
            ],
            "boletas": [],
            "reportes": [],
        }
    )
    return store


def test_generar_boleta(store):
    boleta = BoletaService(store).generar(
        {
            "empleado_codigo": "EMP001",
            "periodo": "Junio 2026",
            "bonos": 150,
            "descuentos": 30,
        }
    )

    assert boleta["sueldo_neto"] == 1920
    assert boleta["empleado_nombre"] == "Juan Ramirez"
    assert len(BoletaService(store).listar()) == 1


def test_boleta_valida_empleado_existente(store):
    with pytest.raises(HTTPException) as error:
        BoletaService(store).generar(
            {
                "empleado_codigo": "NO-EXISTE",
                "periodo": "Junio 2026",
                "bonos": 0,
                "descuentos": 0,
            }
        )

    assert error.value.status_code == 404


def test_reportes_resumen_y_asistencias(store):
    BoletaService(store).generar(
        {
            "empleado_codigo": "EMP001",
            "periodo": "Junio 2026",
            "bonos": 150,
            "descuentos": 30,
        }
    )

    reportes = ReporteService(store)

    assert reportes.resumen()["total_pagos"] == 1920
    assert reportes.resumen()["total_tardanzas"] == 1
    assert reportes.resumen()["total_faltas"] == 1
    assert reportes.asistencias_por_empleado()[0]["asistio"] == 1


def test_reportes_pagos_por_periodo(store):
    service = BoletaService(store)
    service.generar({"empleado_codigo": "EMP001", "periodo": "Junio 2026", "bonos": 0, "descuentos": 0})
    service.generar({"empleado_codigo": "EMP002", "periodo": "Junio 2026", "bonos": 100, "descuentos": 0})

    pagos = ReporteService(store).pagos_por_periodo()

    assert pagos == [{"periodo": "Junio 2026", "cantidad_boletas": 2, "total_pagado": 4300}]
