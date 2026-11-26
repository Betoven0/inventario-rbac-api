from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.audit import MovementType


#1 lo que envia el  operador o admin para registrar una entrada, salida o ajuste
class StockMovementCreate(BaseModel):
    movement_type: MovementType
    quantity: int = Field(..., gt=0, description = 'Cantidad a mover (Mayor a 0)')
    reason: str = Field(...,min_length=3, max_length=255, description = 'Motivo contable del movimiento')
    
#2 Registro inmutable que devuelve la bitacora de audiotria 
class AuditLogResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    movement_type: MovementType
    quantity: int
    previous_stock: int
    new_stock: int
    reason: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)