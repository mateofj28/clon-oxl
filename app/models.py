# app/models.py

import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.sql import func # Para las funciones de fecha y hora
from app.database import Base

# Definición del Enum para los roles de usuario.
# Esto se mapeará a un tipo ENUM en la base de datos (o su equivalente).
class UserRole(enum.Enum):
    NORMAL = "normal"
    ADMIN = "admin"

class User(Base):
    """
    Modelo de SQLAlchemy para la tabla de usuarios.
    Representa a los usuarios registrados en la aplicación.
    """
    __tablename__ = "users" # Nombre de la tabla en la base de datos.

    id = Column(Integer, primary_key=True, index=True) # Identificador único, clave primaria.
    email = Column(String, unique=True, index=True, nullable=False) # Correo electrónico único, no nulo.
    hashed_password = Column(String, nullable=False) # Contraseña encriptada, no nula.

    # Campos opcionales
    first_name = Column(String, nullable=True) # Nombre del usuario.
    last_name = Column(String, nullable=True) # Apellido del usuario.
    phone_number = Column(String, nullable=True) # Número de teléfono.
    address = Column(String, nullable=True) # Dirección.
    city = Column(String, nullable=True) # Ciudad.
    country = Column(String, nullable=True) # País.

    # Campos con valores por defecto o específicos
    role = Column(Enum(UserRole), default=UserRole.NORMAL, nullable=False) # Rol del usuario.
    is_verified = Column(Boolean, default=False) # Indica si la identidad ha sido verificada.
    is_active = Column(Boolean, default=True) # Indica si la cuenta está activa.
    is_suspended = Column(Boolean, default=False) # Indica si el usuario ha sido suspendido.

    # Campos de fecha y hora. 'onupdate=func.now()' actualiza el campo
    # automáticamente cada vez que se modifica la fila.
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        """
        Representación de cadena del objeto User, útil para depuración.
        """
        return f"<User(id={self.id}, email='{self.email}')>"
