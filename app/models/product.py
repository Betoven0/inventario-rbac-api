from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True, index = True)
    
    #1 SKU (Stock keeping Unit): codigo unico de almacen (ej. "LAP-DELL-001")
    
    sku: Mapped[str] = mapped_column(
        String(50), unique = True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    
    #2 Precio unitario exacto en Decimal(Numeric 10,2)
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable = False, default=Decimal("0.00")
    )
    
    #3 Control de existencias y umbral de alerta de StockBajo
    
    stock: Mapped[int] = mapped_column(Integer, default= 0, nullable= False)
    min_stock: Mapped[int] = mapped_column(Integer, default= 5, nullable= False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )