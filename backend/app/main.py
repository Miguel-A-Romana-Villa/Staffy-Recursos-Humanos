from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import asistencia, auth, boletas, empleados, health, reportes

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(empleados.router, prefix="/api/empleados", tags=["empleados"])
app.include_router(asistencia.router, prefix="/api/asistencia", tags=["asistencia"])
app.include_router(boletas.router, prefix="/api/boletas", tags=["boletas"])
app.include_router(reportes.router, prefix="/api/reportes", tags=["reportes"])
