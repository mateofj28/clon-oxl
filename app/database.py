# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Crea el motor de la base de datos.
# 'connect_args={"check_same_thread": False}' es necesario para SQLite
# cuando se usa con FastAPI, ya que SQLite maneja conexiones de forma diferente.
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crea una clase SessionLocal.
# Cada instancia de SessionLocal será una sesión de base de datos.
# El 'autocommit=False' significa que no se guardarán los cambios automáticamente.
# El 'autoflush=False' significa que los objetos no se volcarán a la base de datos
# hasta que se haga un commit o un refresh.
# 'bind=engine' asocia esta sesión con el motor de la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una instancia Base.
# Esta es la base de la cual heredarán todos nuestros modelos SQLAlchemy
# para convertirlos en clases de modelos ORM.
Base = declarative_base()

def get_db():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    Crea una sesión, la usa, y luego se asegura de cerrarla.
    """
    db = SessionLocal() # Crea una nueva sesión.
    try:
        yield db # Retorna la sesión a la función de ruta.
    finally:
        db.close() # Cierra la sesión después de que la solicitud haya terminado.
