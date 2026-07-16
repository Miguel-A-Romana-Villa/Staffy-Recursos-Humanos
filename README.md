# Staffy - Sistema de Gestion de Recursos Humanos

Aplicacion full stack para pequenas empresas. Permite registrar empleados, controlar asistencia, registrar bonos y descuentos, calcular sueldo, generar boletas y revisar reportes.

## Tecnologias

- Frontend: React, TypeScript, Vite, Tailwind CSS, React Router DOM y Axios.
- Backend: Python, FastAPI, Pydantic y SQLAlchemy.
- Base de datos: SQLite local o PostgreSQL/Supabase usando `DATABASE_URL`.
- Pruebas: pytest.

## Estructura

- `frontend/`: interfaz web y consumo de endpoints.
- `backend/app/domain/`: clases y reglas principales de negocio.
- `backend/app/services/`: casos de uso que coordinan dominio y persistencia.
- `backend/app/routes/`: endpoints FastAPI.
- `backend/app/db/`: modelos SQLAlchemy.
- `backend/tests/`: pruebas unitarias.
- `docs/`: arquitectura y diagrama UML.

## Ejecucion

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Tests:

```bash
cd backend
python -m pytest
```

## Flujo principal

1. Registrar empleado.
2. Registrar asistencia.
3. Registrar bono o descuento.
4. Calcular sueldo.
5. Generar boleta.
6. Ver reportes.

## Programacion Orientada a Objetos

- Herencia: `EmpleadoTiempoCompleto` y `EmpleadoMedioTiempo` heredan de `Empleado`.
- Polimorfismo: cada tipo de empleado calcula su sueldo base con su propia implementacion.
- Encapsulamiento: `Boleta` valida sus datos y calcula sueldo base, bonos, descuentos y sueldo neto.
- Asociacion y composicion: `Boleta` recibe un `Empleado` y conserva los objetos `ConceptoPago` usados en el calculo.
- Singleton: `GestorEmpleados` mantiene una unica instancia.
- Factory Method: `EmpleadoFactory` crea empleados segun el tipo recibido.
- Excepciones personalizadas: errores de datos, duplicados y empleado no encontrado.

El diagrama PlantUML esta en `docs/diagrama_clases.puml`.
