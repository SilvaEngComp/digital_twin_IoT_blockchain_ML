
from sys import getsizeof
import pandas as pd
from src.suport_layer.cipher import Cipher
import json
from src.suport_layer.transaction import Transaction
from src.utils.time_register import TimeRegister
from src.proposed_model.smart_contract_1 import SC1
from time import sleep
class Msg:
    def __init__(self,payload) -> None:
        self.payload = payload
        
cipher = Cipher()
dataset = pd.read_csv('../intel_lab.csv', usecols=['temperature','humidity'], delimiter=",")
cont=0
sub_device = "h3"
blockWidth=1
sc1 = SC1(sub_device, blockWidth)
for data in dataset.iterrows():
    if cont>blockWidth:
        break
    temperature = str(data[1][0])
    print(f'tamanho de uma amostra de temperatura = {temperature} : {getsizeof(temperature)} bytes')
    humidity = str(data[1][1])
    print(f'tamanho de uma amostra de umidade = {humidity} : {getsizeof(humidity)} bytes')
    sensorNode = {'temperature':temperature,'humidity':humidity}
    dataBytes = json.dumps(sensorNode).encode("utf-8")
    encrypted = cipher.encrypt(dataBytes)
    responseModel = {"code":"post","post":'sc01',"method":"flow","header":{"sensor":'node Temperature and Humidity',"device":'h1',"time":{"collect":10000, "publish": 10000}}, "data":encrypted.decode()}
    
    responseModel = json.dumps(responseModel)
    print(f'tamanho cabeçalho+dados  JSON : {getsizeof(responseModel)} bytes')
    
    msg = Msg(responseModel)
    print(f'tamanho pacote mensagem publicada MQTT : {getsizeof(msg)} bytes')

    isCompleted = sc1.dataTreating(msg)
    if isCompleted is True:
        sc1.restart()
        # sleep(5)
    cont+=1

