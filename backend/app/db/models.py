from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
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
    correo: Mapped[str | None] = mapped_column(String(120), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    nombres: Mapped[str] = mapped_column(String(120), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(120), nullable=False)
    cargo: Mapped[str] = mapped_column(String(80), nullable=False)
    sueldo_base: Mapped[float] = mapped_column(Float, nullable=False)
    hijos: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    fecha_nacimiento: Mapped[date | None] = mapped_column(Date, nullable=True)
    fecha_inicio: Mapped[date | None] = mapped_column(Date, nullable=True)
    fecha_cese: Mapped[date | None] = mapped_column(Date, nullable=True)
    regimen_pensionario: Mapped[str] = mapped_column(String(40), default="AFP", nullable=False)
    foto_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    asistencias: Mapped[list["AsistenciaDB"]] = relationship(back_populates="empleado")
    boletas: Mapped[list["BoletaDB"]] = relationship(back_populates="empleado")


class AsistenciaDB(Base):
    __tablename__ = "asistencias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    empleado_id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    minutos_tardanza: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comentario: Mapped[str | None] = mapped_column(Text, nullable=True)

    empleado: Mapped[EmpleadoDB] = relationship(back_populates="asistencias")


class BoletaDB(Base):
    __tablename__ = "boletas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    empleado_id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), nullable=False)
    periodo: Mapped[str] = mapped_column(String(20), nullable=False)
    sueldo_base: Mapped[float] = mapped_column(Float, nullable=False)
    bonos: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    descuentos: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    sueldo_neto: Mapped[float] = mapped_column(Float, nullable=False)

    empleado: Mapped[EmpleadoDB] = relationship(back_populates="boletas")
