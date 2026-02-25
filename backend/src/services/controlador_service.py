import threading
from src.models.controlador_model import BulbState, BulbController
from src.repositories.controlador_repo import ControladorRepo

class ControladorService:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):

        with cls._lock:

            if cls._instance is None:

                cls._instance = super().__new__(cls)
                cls._instance.repo = ControladorRepo()

        return cls._instance

    def obter_todos_controladores(self) -> list:

        try: 

            controladores = self.repo.obter_controladores()

            return [ self.para_dict(c) for c in controladores ]

        except Exception as e: raise Exception(f"Erro ao obter todos os controladores: {str(e)}")

    def obter_controlador_por_id(self, id: str) -> dict:

        try: 

            c = self.repo.obter_controlador_por_id(id)

            return self.para_dict(c)

        except Exception as e: raise Exception(f"Erro ao obter controlador por ID: {str(e)}")

    def pesquisar_por_novos_dispositivos(self):

        try: self.repo.atualizar_lista_de_controladores()
        
        except Exception as e: raise Exception(f"Erro ao atualizar controladores: {str(e)}")

    def atualizar_estado_controlador(self, id: str, state: BulbState):

        try: self.repo.atualizar_estado_controlador(id, state)

        except (FileNotFoundError, ValueError, ConnectionError): raise
        except Exception as e: raise Exception(f"Erro ao atualizar estado do controlador: {str(e)}")
        
    def para_dict( self, c: BulbController ) -> dict:

        return {

            "id"        : c.id,
            "name"      : c.name if c.name else None,
            "mode"      : c.state.mode if c.state else None,
            "bright"    : c.state.bright if c.state else None,
            "temp"      : c.state.temp if c.state else None,
            "r"         : c.state.r if c.state else None,
            "g"         : c.state.g if c.state else None,
            "b"         : c.state.b if c.state else None,
            "connected" : c.connected

        }

