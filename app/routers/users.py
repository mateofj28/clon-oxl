# app/routers/users.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db

# Crea un APIRouter con un prefijo para todas las rutas de usuarios.
# 'tags' ayuda a organizar la documentación de Swagger UI.
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.UserPublic, status_code=status.HTTP_201_CREATED)
def create_user_route(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en el sistema.
    Requiere un `UserCreate` con email y contraseña.
    Retorna el `UserPublic` del usuario creado.
    """
    # Verifica si ya existe un usuario con el mismo correo electrónico.
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.UserPublic])
def read_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los usuarios.
    Soporta paginación con `skip` y `limit`.
    Retorna una lista de `UserPublic`.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.UserPublic)
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un usuario específico por su ID.
    Retorna el `UserPublic` del usuario o un error 404 si no se encuentra.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    return db_user

@router.get("/email/{email}", response_model=schemas.UserPublic)
def read_user_by_email_route(email: str, db: Session = Depends(get_db)):
    """
    Obtiene un usuario específico por su correo electrónico.
    Retorna el `UserPublic` del usuario o un error 404 si no se encuentra.
    """
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    return db_user

@router.put("/{user_id}", response_model=schemas.UserPublic)
def update_user_route(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un usuario existente por su ID.
    Requiere un `UserUpdate` con los campos a modificar.
    Retorna el `UserPublic` actualizado o un error 404/400.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    # Si el email se va a actualizar y ya existe otro usuario con ese email
    if user.email and user.email != db_user.email:
        existing_user_with_email = crud.get_user_by_email(db, email=user.email)
        if existing_user_with_email and existing_user_with_email.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está en uso por otro usuario."
            )

    return crud.update_user(db=db, db_user=db_user, user_update=user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario por su ID.
    Retorna un estado 204 No Content si la eliminación fue exitosa,
    o un error 404 si el usuario no se encuentra.
    """
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    return {"message": "Usuario eliminado exitosamente."}
