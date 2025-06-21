# app/schemas.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from app.models import UserRole # Importa el Enum definido en models.py

# Base Schema para propiedades comunes del usuario
class UserBase(BaseModel):
    """
    Esquema base para las propiedades del usuario.
    Utilizado para campos que son comunes tanto en la creación como en la actualización.
    """
    email: EmailStr = Field(..., description="Correo electrónico único del usuario")
    first_name: Optional[str] = Field(None, description="Nombre del usuario")
    last_name: Optional[str] = Field(None, description="Apellido del usuario")
    phone_number: Optional[str] = Field(None, description="Número de teléfono de contacto")
    address: Optional[str] = Field(None, description="Dirección del usuario")
    city: Optional[str] = Field(None, description="Ciudad de residencia")
    country: Optional[str] = Field(None, description="País de residencia")
    role: UserRole = Field(UserRole.NORMAL, description="Rol del usuario en el sistema")
    is_verified: bool = Field(False, description="Indica si la identidad del usuario ha sido verificada")
    is_active: bool = Field(True, description="Indica si la cuenta del usuario está activa")
    is_suspended: bool = Field(False, description="Indica si el usuario ha sido suspendido por un administrador")

    class Config:
        # Permite que el ORM (SQLAlchemy) funcione correctamente con Pydantic.
        # Esto significa que Pydantic intentará leer los datos como atributos
        # de un objeto ORM en lugar de un diccionario.
        from_attributes = True

# Esquema para crear un usuario (incluye la contraseña en texto plano)
class UserCreate(UserBase):
    """
    Esquema para crear un nuevo usuario.
    Hereda de UserBase y añade el campo 'password' (requerido para la creación).
    """
    password: str = Field(..., min_length=8, description="Contraseña en texto plano para el usuario")

# Esquema para actualizar un usuario (todos los campos son opcionales)
class UserUpdate(UserBase):
    """
    Esquema para actualizar un usuario existente.
    Hereda de UserBase y hace que todos los campos sean opcionales
    para permitir actualizaciones parciales.
    """
    email: Optional[EmailStr] = Field(None, description="Correo electrónico único del usuario")
    password: Optional[str] = Field(None, min_length=8, description="Nueva contraseña en texto plano (opcional)")
    role: Optional[UserRole] = Field(None, description="Nuevo rol del usuario en el sistema")
    is_verified: Optional[bool] = Field(None, description="Estado de verificación del usuario")
    is_active: Optional[bool] = Field(None, description="Estado de actividad de la cuenta")
    is_suspended: Optional[bool] = Field(None, description="Estado de suspensión del usuario")

# Esquema para la respuesta pública de un usuario (excluye campos sensibles como la contraseña hasheada)
class UserPublic(UserBase):
    """
    Esquema para la representación pública de un usuario (respuesta de la API).
    Hereda de UserBase y añade el 'id' y las marcas de tiempo.
    Excluye la contraseña hasheada.
    """
    id: int = Field(..., description="Identificador único del usuario")
    created_at: datetime = Field(..., description="Fecha y hora de creación del usuario")
    updated_at: datetime = Field(..., description="Última fecha y hora de actualización del usuario")

# Esquema interno para un usuario en la base de datos (incluye la contraseña hasheada)
class UserInDB(UserBase):
    """
    Esquema interno para la representación de un usuario tal como está en la base de datos.
    Incluye el 'id' y la 'hashed_password'. No se expone directamente en las respuestas públicas.
    """
    id: int = Field(..., description="Identificador único del usuario")
    hashed_password: str = Field(..., description="Contraseña encriptada (hash)")
    created_at: datetime = Field(..., description="Fecha y hora de creación del usuario")
    updated_at: datetime = Field(..., description="Última fecha y hora de actualización del usuario")
