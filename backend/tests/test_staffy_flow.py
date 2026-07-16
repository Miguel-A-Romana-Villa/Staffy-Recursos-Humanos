from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.domain.boleta import Boleta
from app.domain.concepto_pago import ConceptoPago
from app.domain.empleado import EmpleadoMedioTiempo, EmpleadoTiempoCompleto
from app.domain.empleado_factory import EmpleadoFactory
from app.domain.exceptions import BoletaDuplicadaError, DatoInvalidoError
from app.domain.gestor_empleados import GestorEmpleados
from app.routes.reportes import descargar_reporte_pdf
from app.schemas.asistencia_schema import AsistenciaCreate
from app.schemas.boleta_schema import BoletaCreate
from app.schemas.concepto_schema import ConceptoPagoCreate
from app.schemas.empleado_schema import EmpleadoCreate
from app.services.asistencia_service import AsistenciaService
from app.services.boleta_service import BoletaService
from app.services.concepto_service import ConceptoPagoService
from app.services.empleado_service import EmpleadoService
from app.services.reporte_pdf_service import ReportePdfService
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


def test_boleta_encapsula_calculo_y_conceptos():
    empleado = EmpleadoFactory.crear(empleado_payload())
    conceptos = [
        ConceptoPago(empleado_id=1, tipo="BONO", concepto="Productividad", monto=100, periodo="2026-06"),
        ConceptoPago(empleado_id=1, tipo="DESCUENTO", concepto="Tardanza", monto=40, periodo="2026-06"),
        ConceptoPago(empleado_id=1, tipo="BONO", concepto="Otro periodo", monto=500, periodo="2026-05"),
    ]

    boleta = Boleta.generar(
        empleado=empleado,
        periodo="2026-06",
        conceptos=conceptos,
        bonos_extra=25,
        descuentos_extra=5,
    )

    assert boleta.sueldo_base == 1800
    assert boleta.bonos == 125
    assert boleta.descuentos == 45
    assert boleta.calcular_sueldo_neto() == 1880
    assert len(boleta.conceptos) == 2


def test_boleta_valida_sus_reglas():
    empleado = EmpleadoFactory.crear(empleado_payload())

    with pytest.raises(DatoInvalidoError):
        Boleta.generar(empleado, "2026-13", [])

    with pytest.raises(DatoInvalidoError):
        Boleta.generar(empleado, "2026-06", [], bonos_extra=-1)

    with pytest.raises(DatoInvalidoError):
        Boleta.generar(empleado, "2026-06", [], descuentos_extra=2000)


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

    reporte_pdf = ReportePdfService(db).generar()
    assert reporte_pdf.startswith(b"%PDF-")
    assert len(reporte_pdf) > 1000

    respuesta = descargar_reporte_pdf(db)
    assert respuesta.media_type == "application/pdf"
    assert respuesta.body.startswith(b"%PDF-")
    assert respuesta.headers["content-disposition"].startswith('attachment; filename="reporte-staffy-')


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
    boleta = BoletaService(db).generar(
        BoletaCreate(empleado_codigo="EMP003", periodo="2026-06", bonos=0, descuentos=0)
    )

    assert sueldo["sueldo_base"] == 1200
    assert sueldo["sueldo_neto"] == 1200
    assert boleta["sueldo_base"] == 1200
    assert boleta["sueldo_neto"] == 1200


def test_boleta_no_se_duplica_y_conserva_datos_historicos(db):
    empleado = EmpleadoService(db).crear(EmpleadoCreate(**empleado_payload()))
    service = BoletaService(db)
    payload = BoletaCreate(empleado_codigo="EMP001", periodo="2026-06", bonos=0, descuentos=0)

    boleta = service.generar(payload)
    empleado.nombres = "Nombre modificado"
    empleado.cargo = "Otro cargo"
    db.commit()
    guardada = service.listar_por_empleado("EMP001")[0]

    assert guardada["empleado_nombre"] == boleta["empleado_nombre"]
    assert guardada["cargo"] == boleta["cargo"]
    with pytest.raises(BoletaDuplicadaError):
        service.generar(payload)


def test_validacion_dni():
    with pytest.raises(DatoInvalidoError):
        EmpleadoFactory.crear(empleado_payload(dni="ABC"))
