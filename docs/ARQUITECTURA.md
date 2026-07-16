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

La clase `Boleta` valida el periodo, recibe un empleado y sus conceptos de pago, usa el polimorfismo del empleado para obtener el sueldo base y calcula bonos, descuentos y sueldo neto. `BoletaService` se limita a consultar y guardar la boleta generada.

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

Cada boleta conserva el codigo, nombre, DNI y cargo que tenia el empleado al momento de su generacion. Tambien se evita generar mas de una boleta para el mismo empleado y periodo.

## Flujo

```text
React -> FastAPI routes -> services -> domain -> SQLAlchemy -> database
```

El flujo funcional de la aplicacion es:

```text
registrar empleado -> registrar asistencia -> registrar bono/descuento -> calcular sueldo -> generar boleta -> ver reporte
```
