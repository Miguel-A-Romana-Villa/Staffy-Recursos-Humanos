# Arquitectura

El proyecto separa responsabilidades en dos aplicaciones:

- `frontend`: interfaz de usuario y consumo de API.
- `backend`: API REST, validacion de datos, modelos POO y persistencia.

## Backend

- `models/`: clases principales del dominio.
- `schemas/`: contratos de entrada y salida con Pydantic.
- `routes/`: endpoints HTTP.
- `services/`: casos de uso y coordinacion de la logica.
- `utils/`: validaciones y constantes compartidas.
- `data/`: datos locales temporales o archivos de apoyo.

## Modulo de acceso

El proyecto incluye una base inicial para autenticacion:

- Frontend: `pages/Login.tsx`, `services/authApi.ts`, `types/auth.types.ts`.
- Backend: `routes/auth.py`, `schemas/auth_schema.py`, `services/auth_service.py`, `models/usuario.py`.

Por ahora el login es un contrato inicial. La seguridad real, validacion de usuarios y tokens se implementara en una fase posterior.
