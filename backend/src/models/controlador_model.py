from pydantic import BaseModel, Field

class DeviceData(BaseModel):

    """Informações relevante para criar um BulbDevice ( obtido na snapshot.json )."""

    id   : str
    ip   : str
    key  : str
    ver  : str
    name : str

class BulbState(BaseModel):

    """Representação do estado atual da lâmpada."""

    mode    : str
    bright  : int = Field(100, ge=0, le=100)
    temp    : int = Field(100, ge=0, le=100)
    r       : int = Field(255, ge=0, le=255)
    g       : int = Field(255, ge=0, le=255)
    b       : int = Field(255, ge=0, le=255)

class BulbController:

    """Controlador da lâmpada, responsável por manter o estado atual e realizar as operações."""

    def __init__(self, device_data: DeviceData):

        try: 

            from src.services.tuya_service import criar_bulbdevice, testar_conexao

            self.id               = device_data.id
            self.name             = device_data.name
            self.key              = device_data.key
            self.bulb             = criar_bulbdevice(device_data)
            self.connected: bool  = testar_conexao(self.bulb)
            self.state: BulbState = None

        except Exception as e: raise Exception(f"Erro ao criar BulbController: {str(e)}")
