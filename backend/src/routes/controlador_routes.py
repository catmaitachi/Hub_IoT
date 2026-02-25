from fastapi import APIRouter, HTTPException, Body
from src.models.controlador_model import BulbState
from src.services.controlador_service import ControladorService

router = APIRouter()
service = ControladorService()

@router.post("/")
def varredura():

    try:

        service.pesquisar_por_novos_dispositivos()
        return {"message": "Varredura concluída. Lista de controladores atualizada."}

    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def obter_controladores():

    try: return service.obter_todos_controladores()

    except FileNotFoundError: raise HTTPException(status_code=204, detail="Não foram encontrados controladores.")
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def obter_controlador_por_id(id: str):

    try: return service.obter_controlador_por_id(id)

    except FileNotFoundError: raise HTTPException(status_code=204, detail=f"Controlador com ID {id} não encontrado.")
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}")
def atualizar_estado_controlador(id: str, state: BulbState = Body(...)):

    try:

        service.atualizar_estado_controlador(id, state)
        return {"message": "Estado do controlador atualizado com sucesso."}

    except FileNotFoundError: raise HTTPException(status_code=404, detail=f"Controlador com ID {id} não encontrado.")
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e: raise HTTPException(status_code=503, detail=str(e))
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))