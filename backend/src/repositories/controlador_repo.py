import threading, json
from pathlib import Path
from src.models.controlador_model import DeviceData, BulbController, BulbState
from src.services.tuya_service import varredura, testar_conexao

class ControladorRepo:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):

        with cls._lock:

            if cls._instance is None:

                cls._instance = super().__new__(cls)
                cls._instance._controladores = {}
                cls._instance.atualizar_lista_de_controladores()

        return cls._instance
    
    def _pesquisar_dispositivos(self) -> list[DeviceData]:

        try:

            if varredura():

                snapshot = Path(__file__).resolve().parent.parent.parent / 'snapshot.json'

                with snapshot.open() as f: data = json.load(f)
                
                devices = data.get("devices", [])

                device_data_list = []

                for device in devices:

                    device_data = DeviceData(

                        id    = device.get("id"),
                        ip    = device.get("ip"),
                        key   = device.get("key") or device.get("local_key") or "",
                        ver   = device.get("ver"),
                        name  = device.get("name")
                        
                    )

                    device_data_list.append(device_data)

                return device_data_list                
                
        except Exception as e: raise Exception(f"Erro ao pesquisar dispositivos: {str(e)}")

    def atualizar_lista_de_controladores(self):

        try:

            dt_list = self._pesquisar_dispositivos()

            for dt in dt_list:

                if dt.id not in self._controladores:

                    self._controladores[dt.id] = BulbController(dt)

        except Exception as e: raise Exception(f"Erro ao atualizar lista de controladores: {str(e)}")

    def atualizar_estado_controlador(self, id: str, state: BulbState):

        c = self._controladores.get(id)

        if not c: raise FileNotFoundError(f"Controlador com ID {id} não encontrado")

        if not c.key:

            raise ValueError("Dispositivo sem local key. Atualize o campo 'key' no snapshot com a chave local da Tuya.")

        try:

            if state.mode == "white":

                c.bulb.set_mode("white", True)
                c.bulb.set_brightness_percentage(state.bright)
                c.bulb.set_colourtemp_percentage(state.temp)

            elif state.mode == "colour":

                c.bulb.set_mode("colour", True)
                c.bulb.set_colour(state.r, state.g, state.b)

            else:

                raise ValueError("Modo inválido. Use 'white' ou 'colour'.")

            c.state = state
            c.connected = True

        except Exception as e:

            msg = str(e).lower()

            if "device key" in msg or "local key" in msg or "decrypt" in msg:

                raise ValueError("Falha de autenticação Tuya. Verifique a local key do dispositivo.")

            if not testar_conexao(c.bulb):

                c.connected = False
                raise ConnectionError("Lâmpada desconectada. Verifique a conexão e tente novamente.")

            raise Exception(f"Erro ao atualizar estado do controlador: {str(e)}")

    def obter_controladores(self) -> list[BulbController]:

        try: 
            
            l = list(self._controladores.values())

            if not l: raise FileNotFoundError("Nenhum controlador encontrado")

            return l
        
        except Exception as e: raise Exception(f"Erro ao obter controladores: {str(e)}")

    def obter_controlador_por_id(self, id: str) -> BulbController:

        try: 
            
            c = self._controladores.get(id)

            if not c: raise FileNotFoundError(f"Controlador com ID {id} não encontrado")

            return c
        
        except Exception as e: raise Exception(f"Erro ao obter controlador por ID: {str(e)}")