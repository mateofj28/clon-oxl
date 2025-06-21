# app/crud.py

from sqlalchemy.orm import Session
from passlib.context import CryptContext # Para hashing de contraseñas
from app import models, schemas
from typing import Optional


# Configura el contexto para el hashing de contraseñas.
# 'bcrypt' es un algoritmo de hashing seguro.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con una contraseña hasheada."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashea una contraseña en texto plano."""
    return pwd_context.hash(password)

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Obtiene un usuario por su ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Obtiene un usuario por su correo electrónico."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    """Obtiene una lista de usuarios con paginación."""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Crea un nuevo usuario en la base de datos."""
    # Hashea la contraseña antes de guardarla.
    hashed_password = get_password_hash(user.password)
    # Crea una instancia del modelo User con los datos del esquema y la contraseña hasheada.
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        address=user.address,
        city=user.city,
        country=user.country,
        role=user.role,
        is_verified=user.is_verified,
        is_active=user.is_active,
        is_suspended=user.is_suspended
    )
    db.add(db_user) # Añade el objeto a la sesión.
    db.commit() # Guarda los cambios en la base de datos.
    db.refresh(db_user) # Actualiza el objeto db_user con el ID generado por la BD y otros datos.
    return db_user

def update_user(db: Session, db_user: models.User, user_update: schemas.UserUpdate) -> models.User:
    """Actualiza un usuario existente en la base de datos."""
    # Itera sobre los campos del esquema de actualización que no son None.
    update_data = user_update.model_dump(exclude_unset=True)

    # Si se proporciona una nueva contraseña, hashearla.
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Actualiza los atributos del objeto db_user con los nuevos datos.
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user) # Añade el objeto actualizado a la sesión (opcional si ya está gestionado, pero es buena práctica).
    db.commit() # Guarda los cambios.
    db.refresh(db_user) # Actualiza el objeto con los datos de la BD.
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Elimina un usuario de la base de datos por su ID."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user) # Elimina el objeto.
        db.commit() # Guarda los cambios.
        return True # Indica que la eliminación fue exitosa.
    return False # Indica que el usuario no fue encontrado.
