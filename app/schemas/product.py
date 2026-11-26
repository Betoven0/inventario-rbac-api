from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
)


#1 Datos comunes de un producto
class ProductBase(BaseModel):
    sku: str = Field(..., min_length=3, max_length=50, description="Código único de almacén")
    name: str = Field(..., min_length=2, max_length=150)
    category: str = Field(..., min_length=2, max_length=80)
    unit_price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    min_stock: int = Field(default=5, ge=0, description="Nivel mínimo antes de encender alerta")
    
    @field_validator('sku')
    @classmethod
    def normalize_sku(cls, value: str) -> str:
        return value.upper().strip()
    
#2 al crear un producto(ADMIN), puede nacer con stock inicial >= 0
class ProductCreate(ProductBase):
    initial_stock: int = Field(default=0, ge=0)

#3 Respuesta del producto con alerta automatica de stock bajo(@computed_field)
class ProductResponse(ProductBase):
    id: int 
    stock: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes = True)
    @field_serializer('unit_price')
    def serialize_price(self, value: Decimal) -> float:
        return float(value)
    @computed_field
    @property
    def low_stock_alert(self) -> bool:
        '''Devuelve True automaticamente  si el estock actual cayo al minimo o por debajo'''
        return self.stock <= self.min_stock
#4