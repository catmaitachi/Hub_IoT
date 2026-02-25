import time
from pathlib import Path
from tinytuya import BulbDevice, scan
from src.models.controlador_model import DeviceData

def varredura( timeout = 15 ) -> bool:

    try:

        snapshot = Path(__file__).resolve().parent.parent.parent / 'snapshot.json'

        scan()

        inicio = time.time()

        while time.time() - inicio < timeout:

            time.sleep(1)

            if snapshot.exists(): return True

        else: raise TimeoutError("Tempo de varredura esgotado. Nenhuma atualização detectada no snapshot.json.")

    except Exception as e: raise Exception(f"Erro durante a varredura: {str(e)}")

def criar_bulbdevice( device_data: DeviceData ) -> BulbDevice:

    try: 
        
        bd = BulbDevice(device_data.id, device_data.ip, device_data.key)
        bd.set_version(device_data.ver)
        bd.set_socketPersistent(True)

        return bd
    
    except Exception as e: raise Exception(f"Erro ao criar BulbDevice: {str(e)}")

def testar_conexao( bulb: BulbDevice ) -> bool:

    try: 
        
        state = bulb.state()

        if not state: return False
        if isinstance(state, dict) and (state.get("Err") or state.get("Error")): return False

        return True 
    
    except Exception as e: return False