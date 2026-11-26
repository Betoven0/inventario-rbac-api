from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl= f"{settings.API_V1_STR}/auth/login")

#1 Cadenero Base: Verifica que el token JWT se  valido y el susuario este activo
async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(reusable_oauth2)]
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms= [settings.ALGORITHM]
        )
        token_delta = TokenPayload(**payload)
        if token_delta.sub is None:
            raise jwt.InvalidTokenError('Falta el cambo sub')
        user_id = int(token_delta.sub)
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidTokenError,
        ValidationError,
        ValueError
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalido o expirado',
            headers={"WWW-Authenticate": "Bearer"}
        )
    user= await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = 'Usuario no encontrado'
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = 'Cuenta Desactivada'
        )
    return user

#2 Fabrica de Cadeneros por el rol (RBAC)
def require_roles(*allowed_roles: UserRole):
    '''
    Genera una dependencia de FastAPI que solo deja pasar a los roles permitidos
    Ejemplo de uso en un endpoint:
        current_user: Annotated[User, Depends (require_roles(UserRole.ADMIN))]
    '''
    async def role_checker(
        current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:
        if current_user.role not in allowed_roles:
            allowed_str = ', '.join(r.value for r in allowed_roles)
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail= f"Acceso denegado. Tu rol ({current_user.role}) no tiene permiso. Se requiere: {allowed_str}",
            )
        return current_user
    return role_checker