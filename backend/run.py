"""
Arquivo para executar a aplicação FastAPI

Opções de execução:
1. Da raiz do projeto: python -m backend.run
2. Da pasta backend: cd backend && python run.py
3. Com uvicorn direto: uvicorn backend.main:app --reload
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="127.0.0.1",  # Mude de "0.0.0.0" para "127.0.0.1"
        port=8000, 
        reload=True
    )