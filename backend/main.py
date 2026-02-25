import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.controlador_routes import router as controlador_router

app = FastAPI( title="Controlador Tuya", description="API para controle de lâmpadas inteligentes compatíveis com Tuya", version="1.0" )
app.include_router( controlador_router, prefix="/api/controladores", tags=["Controladores"] )

app.add_middleware(

    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True

)

@app.get("/")
def root():

    return {"message": "Controlador Tuya API - Acesse /docs para documentação"}

if __name__ == "__main__":
    
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)