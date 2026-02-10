import json
from pathlib import Path
from tinytuya import BulbDevice, scan
from dispositivo import Dispositivo

def ler_snapshot() -> list:

    try:

        path = Path(__file__).resolve().parent.parent / 'snapshot.json'

        with open(path, 'r') as f:

            data = json.load(f)

            return data.get('devices', [])
    
    except Exception as e:

        return []
    
def dispositivos_salvos() -> list[Dispositivo]:

    snapshot: list = ler_snapshot()

    dispositivos: list[Dispositivo] = []

    for dispositivo in snapshot:

        try:

            bulb = BulbDevice(dispositivo['id'], dispositivo['ip'], dispositivo['key'])
            bulb.set_version(dispositivo['ver'])
            bulb.set_socketPersistent(True)

            dispositivos.append(Dispositivo(bulb))

        except Exception as e:

            continue

    return dispositivos

def varredura() -> bool:

    try:

        scan()

        snapshot: list = ler_snapshot()

        if not snapshot: return False

        else: return True

    except Exception as e:

        return False
    
def testar_conexao( dispositivo: Dispositivo ) -> bool:

    try:

        dispositivo.get_bulb().state()

        return True
    
    except Exception as e:

        return False