# arquivo para enviar um pacote de dados JSON
import time 
import spidev
import RPi.GPIO as GPIO
import sys
from constantes import *
from tratamento_JSON import *
class Lora:
    """Incialização do módulo com o retorno do objetivo já ativado"""
    RST = 22
    DIO0 = 4
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
    def escrita(self, payload):
        """Escreve no módulo a lista de dados em bytes"""
        byte_payload = json_to_bytes(payload)
        tamanho_payload = len(byte_payload)
        if tamanho_payload > 4096:
            raise ValueError("Payload too large (%d bytes)" % tamanho_payload)
        self.def_mode(MODE.STDBY)
        
        return self.spi.xfer([REG.LORA.FIFO | 0x80, tamanho_payload] + byte_payload)[1:]
    def economia(self):
        self.def_mode(MODE.SLEEP)
    