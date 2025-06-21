# main.py

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users

# Crea todas las tablas en la base de datos.
# Esto se hará cada vez que se ejecute la aplicación,
# lo cual es útil para desarrollo. En producción, se usarán migraciones.
Base.metadata.create_all(bind=engine)

# Crea la instancia de la aplicación FastAPI.
app = FastAPI(
    title="API de Gestión de Usuarios",
    description="Una API CRUD simple para gestionar usuarios con FastAPI y SQLAlchemy.",
    version="1.0.0",
)

# Incluye el router de usuarios en la aplicación principal.
# Todas las rutas definidas en 'app/routers/users.py' estarán disponibles bajo '/users'.
app.include_router(users.router)

@app.get("/")
async def root():
    """
    Punto de entrada raíz de la API.
    """
    return {"message": "¡Bienvenido a la API de Gestión de Usuarios! Visita /docs para la documentación interactiva."}
