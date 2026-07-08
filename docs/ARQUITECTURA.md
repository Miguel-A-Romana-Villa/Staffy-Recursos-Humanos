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
