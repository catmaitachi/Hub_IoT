
```

 █████   █████ █████  █████ ███████████     █████          ███████████
░░███   ░░███ ░░███  ░░███ ░░███░░░░░███   ░░███          ░█░░░███░░░█
 ░███    ░███  ░███   ░███  ░███    ░███    ░███   ██████ ░   ░███  ░ 
 ░███████████  ░███   ░███  ░██████████     ░███  ███░░███    ░███    
 ░███░░░░░███  ░███   ░███  ░███░░░░░███    ░███ ░███ ░███    ░███    
 ░███    ░███  ░███   ░███  ░███    ░███    ░███ ░███ ░███    ░███    
 █████   █████ ░░████████   ███████████     █████░░██████     █████   
░░░░░   ░░░░░   ░░░░░░░░   ░░░░░░░░░░░     ░░░░░  ░░░░░░     ░░░░░    by Catmaitachi

```

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.11%2B-000000?logo=python&logoColor=white" alt="Python 3.11+ Badge"/>
    <img src="https://img.shields.io/badge/GUI-Tkinter-000000?logo=python&logoColor=white" alt="GUI - Tkinter Badge"/>
    <img src="https://img.shields.io/badge/Tuya%20IoT%20Platform-OpenAPI-000000?logo=tuya&logoColor=white" alt="Tuya IoT Platform - OpenAPI Badge"/>
    <img src="https://img.shields.io/badge/SDK%20Tuya%20(Python)-oficial-000000?logo=tuya&logoColor=white" alt="SDK Tuya (Python) - oficial Badge"/>
</p>

> Status: 🚧 Projeto em fase de idealização e desenvolvimento... 

## Visão Geral 👀
Hub em Python para controlar dispositivos de iluminação compatíveis com Tuya diretamente pelo PC. A ideia é centralizar operações como ligar/desligar, ajustar brilho/temperatura de cor (e cores, quando suportado), organizar cenas e acompanhar o status dos dispositivos de forma simples e rápida.

> Observação: Necessário ter dispositivos de iluminação inteligentes compatíveis com Tuya para utilizar este hub.

## Como Usar 💡
1. Crie uma conta na [Tuya Dev Platform](https://platform.tuya.com/).
2. Registre um novo projeto e obtenha seu `Access ID` e `Access Secret`.
3. Adicione seus dispositivos de iluminação ao projeto.

4. Clone este repositório:
   ```bash
   git clone https://github.com/Catmaitachi/Hub_IoT.git
   ```

5. Instale as dependências necessárias:
   ```bash
    pip install tinytuya requests tkinter
    ```

6. Configure a API Tuya no repositorio com seu `Access ID`, `Access Secret` e região:
    ```bash
    cd Hub_IoT
    python -m tinytuya wizard
    ```

7. Inicie a interface gráfica (primeira coisa a ser carregada):
    ```bash
    # Opção A
    python src/interface.py

    # Opção B (módulo)
    python -m src.interface
    ```

## Imagens 📸
Espaço reservado para futuras screenshots e fluxos do hub.

## Estrutura do Projeto 📁
Espaço reservado para futuras descrições da estrutura de diretórios e arquivos do projeto.