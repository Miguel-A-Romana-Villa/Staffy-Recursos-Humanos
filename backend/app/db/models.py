from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombres: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    rol: Mapped[str] = mapped_column(String(40), default="RRHH", nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class EmpleadoDB(Base):
    __tablename__ = "empleados"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    dni: Mapped[str] = mapped_column(String(12), unique=True, index=True, nullable=False)
    correo: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    nombres: Mapped[str] = mapped_column(String(120), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(120), nullable=False)
    cargo: Mapped[str] = mapped_column(String(80), nullable=False)
    sueldo_base: Mapped[float] = mapped_column(Float, nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), default="tiempo_completo", nullable=False)
    horas_trabajadas: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    tarifa_por_hora: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    hijos: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    fecha_nacimiento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_cese: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    regimen_pensionario: Mapped[str] = mapped_column(String(40), default="AFP", nullable=False)
    foto_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    asistencias: Mapped[list["AsistenciaDB"]] = relationship(back_populates="empleado")
    boletas: Mapped[list["BoletaDB"]] = relationship(back_populates="empleado")
    conceptos: Mapped[list["ConceptoPagoDB"]] = relationship(back_populates="empleado")


class AsistenciaDB(Base):
    __tablename__ = "asistencias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    empleado_id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    minutos_tardanza: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    comentario: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    empleado: Mapped[EmpleadoDB] = relationship(back_populates="asistencias")


class BoletaDB(Base):
    __tablename__ = "boletas"
    __table_args__ = (UniqueConstraint("empleado_id", "periodo", name="uq_boletas_empleado_periodo"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    empleado_id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), nullable=False)
    empleado_codigo: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    empleado_nombre: Mapped[Optional[str]] = mapped_column(String(240), nullable=True)
    dni: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    cargo: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    periodo: Mapped[str] = mapped_column(String(20), nullable=False)
    sueldo_base: Mapped[float] = mapped_column(Float, nullable=False)
    bonos: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    descuentos: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    sueldo_neto: Mapped[float] = mapped_column(Float, nullable=False)

    empleado: Mapped[EmpleadoDB] = relationship(back_populates="boletas")


class ConceptoPagoDB(Base):
    __tablename__ = "conceptos_pago"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    empleado_id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    concepto: Mapped[str] = mapped_column(String(120), nullable=False)
    monto: Mapped[float] = mapped_column(Float, nullable=False)
    periodo: Mapped[str] = mapped_column(String(20), nullable=False)

    empleado: Mapped[EmpleadoDB] = relationship(back_populates="conceptos")
