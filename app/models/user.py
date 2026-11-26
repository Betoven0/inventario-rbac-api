from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


#1 Jerarquia de Roles empresariales (RBAC: Role-based Access Control)
class UserRole(StrEnum):
    ADMIN = "ADMIN"  #Control total: Crea productos, ajusta stock y exporta reportes 
    OPERATOR = "OPERATOR" #Almacen: Registra entradas y salidas de mercancia 
    VIEWER = "VIEWER" #Audotor/Consulta: solo puede ver inventario, no puede modificar 

#2 Tabla de Usuarios en SQL

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    #Rol del usuario
    role: Mapped[str] = mapped_column(
        String(255), default=UserRole.VIEWER, nullable=False, index = True
        )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable= False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )