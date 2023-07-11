# arquivo para enviar um pacote de dados JSON
import serial 
import time 
import spidev
import RPi.GPIO as GPIO
import sys

class Lora:
    """Incialização do módulo com o retorno do objetivo já ativado"""
    RST = 22
    GPIO.setup(RST, GPIO.OUT)
    FrequenciaSPI = 5000000

    def descanso():
        """limpa os dados do GPIO e fecha o objeto SpiDev"""
        GPIO.cleanup()
        Lora.spi.close()
    
    def open_spidev():
        """Inicia o objeto SpiDev"""
        Lora.spi = spidev.SpiDev()
        Lora.spi.open(0,0)
        Lora.spi.max_speed_hz = Lora.FrequenciaSPI
        return Lora.spi
    def def_mode(self, mode):
        """Defini o modo de operaçõa do módulo
        para o parametro, deve ser usado os parametros definidos
        na classe de modos declarados no arquivo de constantes
        """
        if mode== self.mode:
            return mode
        if self.verbose:
            sys.stderr.write("Mode <- %s\n" % MODE.lookup[mode])
        self.mode = mode
        return self.spi.xfer([REG.LORA.OP_MODE | 0x80, mode])[1]
    