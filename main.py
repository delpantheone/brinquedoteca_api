from api.routes.criancas import router as criancas_router
from api.routes.brinquedos import router as brinquedos_router
from api.routes.emprestimos import router as emprestimos_router

from fastapi import FastAPI

app = FastAPI()

app.include_router(criancas_router)
app.include_router(brinquedos_router)
app.include_router(emprestimos_router)

@app.get('/')
def home():
    return {'message': 'API Online'}
