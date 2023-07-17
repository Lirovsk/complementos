# Esse é um código de teste para analisar a competencia da biblioteca criada
from EnvioJSON import *
import time 
from BOARD import *

BOARD.setup()
BOARD.SpiDev()

lora = Lora()
lora.set_mode(MODE.STDBY)
lora.set_freq(915)
lora.escrita(2023)
lora.descanso()
