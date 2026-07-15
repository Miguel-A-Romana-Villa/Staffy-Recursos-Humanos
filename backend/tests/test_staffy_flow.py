from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.domain.empleado import EmpleadoMedioTiempo, EmpleadoTiempoCompleto
from app.domain.empleado_factory import EmpleadoFactory
from app.domain.exceptions import DatoInvalidoError
from app.domain.gestor_empleados import GestorEmpleados
from app.schemas.asistencia_schema import AsistenciaCreate
from app.schemas.boleta_schema import BoletaCreate
from app.schemas.concepto_schema import ConceptoPagoCreate
from app.schemas.empleado_schema import EmpleadoCreate
from app.services.asistencia_service import AsistenciaService
from app.services.boleta_service import BoletaService
from app.services.concepto_service import ConceptoPagoService
from app.services.empleado_service import EmpleadoService
from app.services.reporte_service import ReporteService
from app.services.sueldo_service import SueldoService


@pytest.fixture()
def db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()


def empleado_payload(**extra):
    data = {
        "codigo": "EMP001",
        "dni": "45879632",
        "nombres": "Juan Carlos",
        "apellidos": "Ramirez Torres",
        "cargo": "Asistente Administrativo",
        "sueldo_base": 1800,
        "tipo": "tiempo_completo",
        "fecha_inicio": date(2026, 6, 1),
        "regimen_pensionario": "AFP",
    }
    data.update(extra)
    return data


def test_factory_herencia_y_singleton():
    completo = EmpleadoFactory.crear(empleado_payload())
    medio_tiempo = EmpleadoFactory.crear(
        empleado_payload(
            codigo="EMP002",
            dni="42157896",
            tipo="medio_tiempo",
            sueldo_base=1,
            horas_trabajadas=80,
            tarifa_por_hora=15,
        )
    )

    assert isinstance(completo, EmpleadoTiempoCompleto)
    assert isinstance(medio_tiempo, EmpleadoMedioTiempo)
    assert completo.calcular_sueldo_base() == 1800
    assert medio_tiempo.calcular_sueldo_base() == 1200
    assert GestorEmpleados.get_instance() is GestorEmpleados.get_instance()


def test_flujo_completo_rrhh(db):
    empleado = EmpleadoService(db).crear(EmpleadoCreate(**empleado_payload()))
    AsistenciaService(db).registrar_o_actualizar(
        AsistenciaCreate(empleado_id=empleado.id, fecha=date(2026, 6, 24), estado="TARDE", minutos_tardanza=20)
    )
    ConceptoPagoService(db).registrar(
        ConceptoPagoCreate(empleado_id=empleado.id, tipo="BONO", concepto="Puntualidad", monto=150, periodo="2026-06")
    )
    ConceptoPagoService(db).registrar(
        ConceptoPagoCreate(empleado_id=empleado.id, tipo="DESCUENTO", concepto="Tardanza", monto=30, periodo="2026-06")
    )

    sueldo = SueldoService(db).calcular("EMP001", "2026-06")
    boleta = BoletaService(db).generar(BoletaCreate(empleado_codigo="EMP001", periodo="2026-06", bonos=0, descuentos=0))
    resumen = ReporteService(db).resumen()

    assert sueldo["sueldo_neto"] == 1920
    assert boleta["sueldo_neto"] == 1920
    assert resumen["total_empleados"] == 1
    assert resumen["total_tardanzas"] == 1
    assert resumen["total_pagos"] == 1920


def test_sueldo_medio_tiempo_usa_polimorfismo(db):
    EmpleadoService(db).crear(
        EmpleadoCreate(
            **empleado_payload(
                codigo="EMP003",
                dni="73984561",
                tipo="medio_tiempo",
                sueldo_base=1,
                horas_trabajadas=80,
                tarifa_por_hora=15,
            )
        )
    )

    sueldo = SueldoService(db).calcular("EMP003", "2026-06")

    assert sueldo["sueldo_base"] == 1200
    assert sueldo["sueldo_neto"] == 1200


def test_validacion_dni():
    with pytest.raises(DatoInvalidoError):
        EmpleadoFactory.crear(empleado_payload(dni="ABC"))
