# Esse é um código de teste para analisar a competencia da biblioteca criada
from EnvioJSON import *
from time import sleep
from BOARD import *
from constantes import *

lora = Lora()
lora.__init__
lora.set_mode(MODE.STDBY)
lora.set_freq(915.0)    
lora.set_fifo_tx_base_addr(0xFF)
lora.spi.xfer([REG.LORA.PA_DAC | 0x01, 0x84])

#criação do pacote JSON para uma transmissão de testes
dados = {
    "nome": "Joao",
    "idade": 30,
    "cidade": "Sao Paulo"
}
#dados = "ola mundo"
#transmissão do pacote JSON
while True:
    print(dados)
    lora.escrita(dados)
    sleep(2)
#Limpa do spi_bus para desligamento do sistema SPI
lora.descanso()