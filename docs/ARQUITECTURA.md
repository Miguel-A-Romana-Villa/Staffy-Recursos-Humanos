# Arquitectura

Staffy separa frontend, API, dominio y persistencia.

## Frontend

React solo consume endpoints y muestra la informacion. Las pantallas principales son:

- Dashboard.
- Empleados.
- Asistencia.
- Bonos y descuentos.
- Sueldos.
- Boletas.
- Reportes.

## Backend

- `domain/`: reglas de negocio y clases POO.
- `services/`: coordinan casos de uso.
- `routes/`: reciben peticiones HTTP y devuelven respuestas.
- `schemas/`: contratos Pydantic.
- `db/`: tablas SQLAlchemy.

Las rutas no calculan sueldo ni contienen reglas de negocio. Esas reglas estan en `domain/` y se usan desde `services/`.

## Persistencia

En desarrollo local se usa SQLite:

```text
DATABASE_URL=sqlite:///./app/data/db.sqlite3
```

Para Supabase o PostgreSQL:

```text
DATABASE_URL=postgresql+psycopg://usuario:password@host:5432/staffy
```

Tablas principales:

- `usuarios`.
- `empleados`.
- `asistencias`.
- `conceptos_pago`.
- `boletas`.

## Flujo

```text
React -> FastAPI routes -> services -> domain -> SQLAlchemy -> database
```

El flujo funcional de la aplicacion es:

```text
registrar empleado -> registrar asistencia -> registrar bono/descuento -> calcular sueldo -> generar boleta -> ver reporte
```
