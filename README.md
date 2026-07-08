# Sistema de Gestion de Personal

Aplicacion de recursos humanos para pequenas empresas.

## Tecnologias

- Frontend: React, Vite, TypeScript, Tailwind CSS, React Router DOM, Axios.
- Backend: Python, FastAPI, Pydantic, SQLAlchemy.
- Base de datos: PostgreSQL, preparada para Supabase.

## Estructura

- `frontend/`: interfaz web de la aplicacion.
- `backend/`: API REST y logica de negocio orientada a objetos.
- `docs/`: documentacion tecnica del proyecto.

## Comandos sugeridos

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Backend:

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```
