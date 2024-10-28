
import json
from sys import getsizeof
from .cipher import Cipher


class Transaction:
    def __init__(self, sender, sensor, receiver, data):
        self.sender = sender
        self.sensor = sensor
        self.receiver = receiver
        self.data = data

    def __getitem__(self, i):
        if i == 'sensor':
            return self.sensor
        elif i == 'data':
            return self.data

    def __str__(self):
        return str({
            'sender': self.sender,
            'sensor': self.sensor,
            'receiver': self.receiver,
            'data': self.data,
        })

    def __repr__(self):
        return str({
            'sender': self.sender,
            'sensor': self.sensor,
            'receiver': self.receiver,
            'data': self.data,
        })

    def toJson(self):
        cabecalho= {
            'sender': self.sender,
            'sensor': self.sensor,
            'receiver': self.receiver,
        }
        # print(f'---------------- Tansações------------')
        # print(f'tamanho cabeçalho transação : {getsizeof(json.dumps(cabecalho))} bytes')
            
        data= {
            'sender': self.sender,
            'sensor': self.sensor,
            'receiver': self.receiver,
            'data': self.data,
        }
        # print(f'tamanho dado transação : {getsizeof(json.dumps(self.data))} bytes')
        # print(f'tamanho transação completo : {getsizeof(json.dumps(data))} bytes')
            
        return {
            'sender': self.sender,
            'sensor': self.sensor,
            'receiver': self.receiver,
            'data': self.data,
        }

    @classmethod
    def fromJson(self, data):
        if isinstance(data, dict):
            return Transaction(data['sender'], data['sensor'], data['receiver'], data['data'])
        return data

    @classmethod
    def fromJsonDecrypt(self, transaction):
        cipher = Cipher()
        try:
            if isinstance(transaction, dict):
                temp = transaction['data'].replace("b'", "'")
                temp = str.encode(temp)
                decriptedTemp = cipher.decrypt(temp)
                
                transactionJson = json.loads(decriptedTemp)
                transactionJson = json.dumps(transactionJson)
                return Transaction(transaction['sender'], transaction['sensor'], transaction['receiver'], transactionJson)
            else:
                temp = transaction.data.replace("b'", "'")
                temp = str.encode(temp)
                decriptedTemp = cipher.decrypt(temp)
                
                dataJson = json.loads(decriptedTemp)
                transaction.data = json.dumps(dataJson)
                return transaction
        except Exception as e:
            print(e)
