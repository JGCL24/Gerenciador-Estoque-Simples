from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float = 0.0
    quantity: int = 0
    min_quantity: int = 0

class ProductCreate(SQLModel):
    name: str
    description: Optional[str] = None
    price: float = 0.0
    quantity: int = 0
    min_quantity: int = 0

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    min_quantity: Optional[int] = None

class Movement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    type: str  # 'entrada' or 'saida'
    quantity: int
    note: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MovementCreate(SQLModel):
    product_id: int
    type: str
    quantity: int
    note: Optional[str] = None
