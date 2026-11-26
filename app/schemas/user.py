from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.user import UserRole


#1 Esquema base de Usuario con normalizacion automatica de correo
class UserBase(BaseModel):
    email : EmailStr
    full_name: str | None = Field(default=None, max_length = 150)
    role: UserRole = Field(default= UserRole.VIEWER)
    
    @field_validator('email')
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).lower().strip()
    
    #2 Datos para registrar un Usuario nuevo
class UserCreate(UserBase):
    password: str= Field(min_length=8, max_length=72)
    
    #3 Datos que devuelve la API(sin contraseña)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    #4 Esquemas del Token JWT (incluye el Rol adentro del Token)
    
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    role: UserRole
        
class TokenPayload(BaseModel):
    sub: str | None = None
    role: str | None = None
    exp: int | None = None