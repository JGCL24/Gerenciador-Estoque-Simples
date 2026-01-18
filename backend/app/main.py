from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from typing import List
from .database import create_db_and_tables, get_session
from .models import Product, ProductCreate, ProductUpdate, Movement, MovementCreate
from datetime import datetime

app = FastAPI(title="Gerenciador de Estoque API")

produtos_router = APIRouter(prefix="/products", tags=["Products"])
movimentacoes_router = APIRouter(prefix="/movements", tags=["Movements"])

# CORS - Permitir acesso de qualquer origem (necessário para ngrok e deploy)
import os
ALLOW_ALL_ORIGINS = os.getenv("ALLOW_ALL_ORIGINS", "false").lower() == "true"

if ALLOW_ALL_ORIGINS:
    # Modo produção/ngrok - Permite qualquer origem
    origins = ["*"]
else:
    # Modo desenvolvimento - Apenas localhost
    origins = ["http://localhost:5173", "http://localhost:3000", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    import os

    create_db_and_tables()

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    display_host = host if host != "0.0.0.0" else "localhost"
    app_url = f"http://{display_host}:{port}"
    docs_url = f"{app_url}/docs"

    print("")
    print("App:", app_url)
    print("Docs:", docs_url)
    print("")

@produtos_router.get("", response_model=List[Product])
def listar_produtos(*, session=Depends(get_session)):
    """Lista todos os produtos cadastrados."""
    products = session.exec(select(Product)).all()
    return products

@produtos_router.post("", response_model=Product, status_code=201)
def criar_produto(*, product: ProductCreate, session=Depends(get_session)):
    """Cria um novo produto e registra automaticamente uma movimentação de entrada."""
    if product.price < 0 or product.quantity < 0 or product.min_quantity < 0:
        raise HTTPException(status_code=400, detail="Negative values are not allowed")
    db_product = Product(**product.model_dump())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    if db_product.quantity > 0:
        movimento_entrada = Movement(
            product_id=db_product.id,
            type="entrada",
            quantity=db_product.quantity,
            note="Cadastro inicial do produto",
            timestamp=datetime.utcnow()
        )
        session.add(movimento_entrada)
        session.commit()
    return Product.model_validate(db_product)


@produtos_router.get("/{product_id}", response_model=Product)
def obter_produto(*, product_id: int, session=Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@produtos_router.put("/{product_id}", response_model=Product)
def atualizar_produto(*, product_id: int, product: ProductUpdate, session=Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data = product.model_dump(exclude_unset=True)
    if any(v is not None and v < 0 for v in (product_data.get("price"), product_data.get("quantity"), product_data.get("min_quantity"))):
        raise HTTPException(status_code=400, detail="Negative values are not allowed")
    for key, value in product_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@produtos_router.delete("/{product_id}", status_code=204)
def deletar_produto(*, product_id: int, session=Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    delete_movement = Movement(
        product_id=product.id,
        type="excluido",
        quantity=product.quantity,
        note=product.name,
        timestamp=datetime.utcnow()
    )
    session.add(delete_movement)
    session.delete(product)
    session.commit()
    return None

@movimentacoes_router.get("", response_model=List[Movement])
def listar_movimentacoes(*, session=Depends(get_session)):
    """Lista todas as movimentações (ordenadas por data decrescente)."""
    movements = session.exec(select(Movement).order_by(Movement.timestamp.desc())).all()
    return movements

@movimentacoes_router.post("", response_model=Movement, status_code=201)
def criar_movimentacao(*, movement: MovementCreate, session=Depends(get_session)):
    """Cria uma nova movimentação (entrada ou saída)."""
    product = session.get(Product, movement.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if movement.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

    if movement.type not in ("entrada", "saida"):
        raise HTTPException(status_code=400, detail="Type must be 'entrada' or 'saida'")

    if movement.type == 'entrada':
        product.quantity = product.quantity + movement.quantity
    else:
        if product.quantity - movement.quantity < 0:
            raise HTTPException(status_code=400, detail="Cannot remove more than current quantity")
        product.quantity = product.quantity - movement.quantity

    db_movement = Movement(
        product_id=movement.product_id,
        type=movement.type,
        quantity=movement.quantity,
        note=movement.note,
        timestamp=datetime.utcnow()
    )
    session.add(db_movement)
    session.add(product)
    session.commit()
    session.refresh(db_movement)
    session.refresh(product)

    return Movement.model_validate(db_movement)

app.include_router(produtos_router)
app.include_router(movimentacoes_router)