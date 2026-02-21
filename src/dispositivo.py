from tinytuya import BulbDevice

class __Colorido__:

    def __init__(self, r: int, g: int, b: int):
        
        inconsistencia = False

        if r < 0 or r > 255: inconsistencia = True
        if g < 0 or g > 255: inconsistencia = True
        if b < 0 or b > 255: inconsistencia = True

        if inconsistencia: raise ValueError("Valores fora do intervalo permitido")

        self.r = r
        self.g = g
        self.b = b

class __Branco__:

    def __init__(self, temperatura: int, brilho: int):

        inconsistencia = False

        if temperatura < 0 or temperatura > 100: inconsistencia = True
        if brilho < 0 or brilho > 100: inconsistencia = True

        if inconsistencia: raise ValueError("Valores fora do intervalo permitido")

        self.temperatura = temperatura
        self.brilho = brilho

class Dispositivo:

    def __init__(self, bulb: BulbDevice):

        self.bulb = bulb
        self.conexao: bool = False
        self.memoria: __Branco__ | __Colorido__ = None

    def obter_bulb(self) -> BulbDevice:

        return self.bulb

    def obter_brilho(self) -> int:

        return self.bulb.get_brightness_percentage()

    def definir_brilho(self, porcentagem: int = 100):

        self.bulb.set_mode('white', True)
        self.bulb.set_brightness_percentage(porcentagem)

        self.salvar_estado()

    def obter_temperatura(self) -> int:

        return self.bulb.get_colourtemp_percentage()
    
    def definir_temperatura(self, temperatura: int = 100):

        self.bulb.set_mode('white', True)    
        self.bulb.set_colourtemp_percentage(temperatura) 

        self.salvar_estado()
    
    def obter_cor(self) -> tuple[int, int, int]:

        return self.bulb.colour_rgb()
    
    def definir_cor(self, r: int = 255, g: int = 255, b: int = 255):
        
        if r == 0 and g == 0 and b == 0: self.desligar()

        else:

            self.bulb.set_mode('colour', True)
            self.bulb.set_colour(r, g, b)

            self.salvar_estado()

    def obter_modo(self) -> str:

        return self.bulb.get_mode()

    def salvar_estado(self):

        try:

            if self.bulb.get_mode() == 'white':
                
                temperatura = self.bulb.get_colourtemp_percentage()
                brilho = self.bulb.get_brightness_percentage()

                branco = __Branco__( temperatura=temperatura, brilho=brilho )

                self.memoria = branco

            elif self.bulb.get_mode() == 'colour':

                r, g, b = self.bulb.colour_rgb()

                colorido = __Colorido__( r=r, g=g, b=b )

                self.memoria = colorido

        except Exception as e:

            print("Não foi possível salvar o estado do dispositivo")

    def recuperar_estado(self):

        try:

            if self.memoria:

                if isinstance(self.memoria, __Branco__):

                    self.definir_brilho(self.memoria.brilho)

                elif isinstance(self.memoria, __Colorido__):

                    self.definir_cor(self.memoria.r, self.memoria.g, self.memoria.b)

        except Exception as e:

            print("Não foi possível recuperar o estado do dispositivo")

    def desligar(self):
        
        self.bulb.set_brightness_percentage(0)

    def testar_conexao(self) -> bool:

        try:

            self.bulb.state()

            self.conexao = True
        
        except Exception as e:

            self.conexao = False