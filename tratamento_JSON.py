import json
import spidev
# Usado para ler uma string JSON  e retornar uma lista de bytes 
#que podem ser transmitios pela intefazer SPI
def json_to_bytes(json_string):
    """Lê uma string JSON e retorna uma lista de bytes"""
    # Converte a string JSON para um objeto Python
    obj_analisado = json.dumps(json_string)
    # Converte o objeto Python para uma lista de bytes 
    return bytes(obj_analisado, 'utf-8')
def bytes_to_json(bytes):
    """Lê uma lista de bytes e retorna uma string JSON"""
    # Converte a lista de bytes para uma string
    obj_analisado = str(bytes, 'utf-8')
    # Converte a string para um objeto Python
    return json.loads(obj_analisado)
