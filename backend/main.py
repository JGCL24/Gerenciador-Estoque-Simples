from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database import db
from routers import (
    usuarios, clientes, campos, reservas, produtos, estoque,
    mesas, comandas, compras, pagamentos
)

app = FastAPI(
    title="Arena Pinheiro API",
    description="API para gerenciamento da Arena Pinheiro",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuários"])
app.include_router(clientes.router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(campos.router, prefix="/api/campos", tags=["Campos"])
app.include_router(reservas.router, prefix="/api/reservas", tags=["Reservas"])
app.include_router(produtos.router, prefix="/api/produtos", tags=["Produtos"])
app.include_router(estoque.router, prefix="/api/estoque", tags=["Estoque"])
app.include_router(mesas.router, prefix="/api/mesas", tags=["Mesas"])
app.include_router(comandas.router, prefix="/api/comandas", tags=["Comandas"])
app.include_router(compras.router, prefix="/api/compras", tags=["Compras"])
app.include_router(pagamentos.router, prefix="/api/pagamentos", tags=["Pagamentos"])

@app.on_event("startup")
async def startup_event():
    """Inicializa a conexão com o banco ao iniciar a aplicação"""
    try:
        db.connect()
        print("Conexão com banco de dados estabelecida!")
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Fecha a conexão ao encerrar a aplicação"""
    db.close()
    print("Conexão com banco de dados fechada!")

@app.get("/")
async def root():
    return {
        "message": "API Arena Pinheiro",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Endpoint para verificar saúde da API"""
    try:
        db.get_connection()
        return {"status": "healthy", "database": "connected"}
    except:
        return {"status": "unhealthy", "database": "disconnected"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
