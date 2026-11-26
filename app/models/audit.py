from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


#1 Tipos de movimientos en el almacen
class MovementType(StrEnum):
    IN = "IN"           # Entrada de Mercancia (compra a proveedor/ devolucion)
    OUT = "OUT"         # Salida de Mercancia (Venta/Merma)
    ADJUST = "ADJUST"   # Ajuste directo por conteo fisico de auditoria

#2 Tabla de bitacora de Auditoria ( Kardex del Invetario )

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True, index= True)
    
    #Que producto de movio y quien lo hizo
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"), nullable=False, index = True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index = True
    )
    
    movement_type: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    #Fotografia contable: cuanto habia ante y cuanto quedo despues
    previous_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    new_stock: Mapped[int] = mapped_column(Integer, nullable= False)
    
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )