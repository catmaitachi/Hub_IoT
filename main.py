import sys
from pathlib import Path

# Garante que o diretório 'src' esteja no sys.path para importações diretas
ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
	sys.path.insert(0, str(SRC))

from src.interface import InterfaceApp


def main():
	app = InterfaceApp()
	app.run()


if __name__ == '__main__':
	main()
