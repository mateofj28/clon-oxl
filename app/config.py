# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Clase de configuración para la aplicación FastAPI.
    Define variables de entorno y proporciona valores por defecto.
    """
    # URL de la base de datos para SQLAlchemy.
    # Por defecto, usa una base de datos SQLite llamada 'sql_app.db'
    # en la misma carpeta que el proyecto.
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    # Configuración del modelo Pydantic.
    # Indica que las variables se cargarán desde un archivo .env si existe.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Crea una instancia de Settings para ser importada y utilizada en otros módulos.
settings = Settings()
