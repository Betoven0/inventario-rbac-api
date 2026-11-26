from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from app.core.config import settings


#1 Encriptar y Verificar contraseñas con proteccion del limi te de 72 bytes de bcrypt
def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    if len(pwd_bytes)>72:
        raise ValueError("la contraseña excede 72 bytes")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt). decode('utf-8')

def verify_password(plain_password: str, hashed_password:str) -> bool:
    plain_bytes = plain_password.encode('utf-8')
    if len(plain_bytes) > 72:
        return False
    return bcrypt.checkpw(plain_bytes, hashed_password.encode('utf-8'))

#2 Señuelo anti-timing attack
DUMMY_PASSWORD_HASH = get_password_hash('dummy_password_for_timing_protection')

#3 Fabricar el token JWT incluytendo el rol de lusuario adentro del gafete
def create_access_token(
    subject: str | Any,
    role: str,
    expires_delta: timedelta | None = None
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta
        if expires_delta
        else timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "role": role,
        "iat": now,
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm= settings.ALGORITHM)