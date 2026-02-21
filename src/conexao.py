import json
from pathlib import Path
from dispositivo import Dispositivo
from tinytuya import BulbDevice, scan
from concurrent.futures import ThreadPoolExecutor, as_completed

def _ler_snapshot() -> list:
    
    """
    
    💡 Lê o arquivo snapshot.json e retorna a lista de dispositivos salvos.

        ⚙️ Funcionamento:
            1. Constrói o caminho para o arquivo snapshot.json usando o módulo pathlib.
            2. Abre o arquivo snapshot.json em modo de leitura.
            3. Carrega o conteúdo do arquivo usando json.load() e extrai a lista de dispositivos.
            4. Retorna a lista de dispositivos.
    
        ⁉️ Raises:
            - *FileNotFoundError*: Caso o arquivo snapshot.json não seja encontrado.
            - *ValueError*: Se o arquivo snapshot.json contiver um formato inválido.
            - *Exception*: Para quaisquer outros erros que possam ocorrer durante a leitura do arquivo.

        🎁 Retornos:
            - list: Uma lista de dicionários representando os dispositivos salvos no snapshot.json.

    """

    try:

        path = Path(__file__).resolve().parent.parent / 'snapshot.json'

        with open(path, 'r') as f:

            data = json.load(f)

            return data.get('devices', [])
    
    except FileNotFoundError as e: raise FileNotFoundError("O arquivo snapshot.json não foi encontrado.")
    except json.JSONDecodeError as e: raise ValueError("O arquivo snapshot.json contém um formato inválido.")
    except Exception as e: raise Exception("Ocorreu um erro ao ler o arquivo snapshot.json: " + str(e))


def _criar_dispositivo( dispositivo: dict ) -> Dispositivo | None:

    """
    
    💡 Cria um objeto Dispositivo a partir de um dicionário de informações do dispositivo ( obtido do snapshot.json ).

        ⚙️ Funcionamento:
            1. Recebe um dicionário contendo as informações do dispositivo (id, ip, key, ver).
            2. Tenta criar um objeto BulbDevice ( da biblioteca da Tinytuya ) usando as informações fornecidas.
            3. Configura a versão e a persistência do socket do BulbDevice.
            4. Retorna um objeto Dispositivo encapsulando o BulbDevice criado.

        🧩 Parâmetros:
            - dispositivo (dict): Um dicionário contendo as informações do dispositivo, com as seguintes chaves: id, ip, key, ver.

        🎁 Retornos:
            - Dispositivo: Um objeto Dispositivo criado a partir das informações fornecidas.
            - None: Se ocorrer um erro durante a criação do objeto BulbDevice ou ao configurar o dispositivo.

    """

    try:

        bulb = BulbDevice(dispositivo['id'], dispositivo['ip'], dispositivo['key'])
        bulb.set_version(dispositivo['ver'])
        bulb.set_socketPersistent(True)

        return Dispositivo(bulb)
    
    except Exception as e: return None

def dispositivos_salvos() -> list[Dispositivo]:

    """
    
    💡 Lê o snapshot.json, cria objetos Dispositivo para cada dispositivo salvo e retorna uma lista desses objetos.

        ⚙️ Funcionamento:
            1. Chama a função _ler_snapshot() para obter a lista de dispositivos salvos no snapshot.json.
            2. Inicializa uma lista de dispositivos com o mesmo tamanho da lista obtida do snapshot.
            3. Utiliza ThreadPoolExecutor para criar objetos Dispositivo em paralelo, chamando a função _criar_dispositivo() para cada dispositivo do snapshot.
            4. Armazena os objetos Dispositivo criados na lista de dispositivos, mantendo a ordem original do snapshot.
            5. Retorna a lista de objetos Dispositivo criados.

        🎁 Retornos:
            - list[Dispositivo]: Uma lista de objetos Dispositivo criados a partir das informações do snapshot.json.

    """

    snapshot: list = _ler_snapshot()

    dispositivos: list[Dispositivo | None] = [None] * len(snapshot)

    with ThreadPoolExecutor(max_workers=10) as executor:

        futures = {}

        for i, dispositivo in enumerate(snapshot):

            future = executor.submit(_criar_dispositivo, dispositivo)

            futures[future] = i

        for future in as_completed(futures):

            i = futures[future]

            dispositivos[i] = future.result()

    return dispositivos

def varredura() -> bool:

    """
    
    💡 Realiza uma varredura na rede usando scan() para detectar dispositivos compatíveis e verifica se algum dispositivo foi encontrado.

        ⚙️ Funcionamento:
            1. Chama a função scan() da biblioteca Tinytuya para realizar uma varredura na rede em busca de dispositivos compatíveis.
            2. Lê o snapshot.json usando a função _ler_snapshot() para obter a lista de dispositivos salvos.
            3. Verifica se a lista de dispositivos obtida do snapshot.json está vazia ou não.
            4. Retorna True se houver dispositivos encontrados (ou seja, se a lista não estiver vazia) e False caso contrário.

        🎁 Retornos:
            - bool: True se houver dispositivos encontrados, False caso contrário.

    """

    try:

        scan()

        snapshot: list = _ler_snapshot()

        if not snapshot: return False

        else: return True

    except Exception as e:

        return False