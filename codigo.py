# Esse é um código de teste para analisar a competencia da biblioteca criada
from EnvioJSON import *
import time 
from BOARD import *

BOARD.setup()
BOARD.SpiDev()

lora = Lora()
lora.set_mode(MODE.STDBY)
#criação do pacote JSON para uma transmissão de testes
dados = {
    "nome": "Joao",
    "idade": 30,
    "cidade": "Sao Paulo"
}

#transmissão do pacote JSON
lora.set_freq(915.0)
dados_tratados = json_to_bytes(dados)
print(dados_tratados)
lora.escrita(dados)
#Limpa do spi_bus para desligamento do sistema SPI
lora.descanso()
