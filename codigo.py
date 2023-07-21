# Esse é um código de teste para analisar a competencia da biblioteca criada
from EnvioJSON import *
import time 
from BOARD import *

BOARD.setup()
BOARD.SpiDev()

lora = Lora()
lora.set_mode(MODE.STDBY)
#criação do pacote JSON para uma transmissão de testes
jsonString = "{";
jsonString += "\"equipe\": 42,";
jsonString += "\"bateria\": 62,";
jsonString = "}";
pacote = jsonString
#transmissão do pacote JSON
lora.set_freq(915.0)
lora.escrita(pacote)
#Limpa do spi_bus para desligamento do sistema SPI
lora.descanso()
