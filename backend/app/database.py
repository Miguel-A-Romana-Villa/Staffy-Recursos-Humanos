from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    ensure_schema_updates()


def ensure_schema_updates():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if "empleados" in tables:
        empleado_columns = {column["name"] for column in inspector.get_columns("empleados")}
        add_column_if_missing("empleados", empleado_columns, "correo", "VARCHAR(120)")
        add_column_if_missing("empleados", empleado_columns, "telefono", "VARCHAR(20)")
        add_column_if_missing("empleados", empleado_columns, "hijos", "INTEGER DEFAULT 0")
        add_column_if_missing("empleados", empleado_columns, "fecha_nacimiento", "DATE")
        add_column_if_missing("empleados", empleado_columns, "fecha_inicio", "DATE")
        add_column_if_missing("empleados", empleado_columns, "fecha_cese", "DATE")
        add_column_if_missing("empleados", empleado_columns, "regimen_pensionario", "VARCHAR(40) DEFAULT 'AFP'")
        add_column_if_missing("empleados", empleado_columns, "foto_url", "VARCHAR(255)")

    if "asistencias" in tables:
        asistencia_columns = {column["name"] for column in inspector.get_columns("asistencias")}
        add_column_if_missing("asistencias", asistencia_columns, "minutos_tardanza", "INTEGER")
        add_column_if_missing("asistencias", asistencia_columns, "comentario", "TEXT")


def add_column_if_missing(table_name: str, existing_columns: set[str], column_name: str, definition: str):
    if column_name in existing_columns:
        return

    with engine.begin() as connection:
        connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}"))
