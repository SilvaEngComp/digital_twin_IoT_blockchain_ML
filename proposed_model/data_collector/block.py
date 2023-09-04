
import datetime
import json
from transaction import Transaction
from hostTrainer import HostTrainer
class Block:
    def __init__(self, transactions=[],typeBlock="data_blockchain", index=1, proof=1, previousHash='0', timestamp = None, hostTrainer=None):
        self.transactions = transactions
        self.index = index
        self.proof = proof
        self.previousHash = previousHash
        self.timestamp = self.configTimestamp(timestamp)
        self.hostTrainer = hostTrainer
        self.typeBlock = typeBlock
        
    def configTimestamp(self, timestamp):
        if timestamp is None:
            now = datetime.datetime.now()
            dateFormat = "%Y-%m-%d %H:%M:%S"
            return now.strftime(dateFormat)
        return timestamp
        
        
    def __getitem__(self, i):
        if i == 'transactions':
            return self.transactions
    
    def __str__(self):
        return str({
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'typeBlock':self.typeBlock,
            'previousHash': self.previousHash,
            'hostTrainer': self.hostTrainer,
            'transactions': self.transactions
            })
    def __repr__(self):
        return str({
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'typeBlock':self.typeBlock,
            'previousHash': self.previousHash ,
            'hostTrainer': self.hostTrainer,
            'transactions': self.transactions
            })
    
    def toJson(self):
        transactions = []
        for transaction in self.transactions:
            if isinstance(transaction, Transaction):
                transactions.append(transaction.toJson())
            else:
                transactions.append(transaction)
        
        if(self.typeBlock=='data_blockchain' or self.hostTrainer is None):
            jsonData = {
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'typeBlock':self.typeBlock,
            'previousHash': self.previousHash, 
            'transactions': transactions
            }
        else:
            jsonData = {
            'index': self.index,
            'timestamp': self.timestamp,
            'proof':self.proof,
            'typeBlock':self.typeBlock,
            'previousHash': self.previousHash, 
            'hostTrainer': self.hostTrainer.toJson(),
            'transactions': transactions
            }
        
        return jsonData
        
    @classmethod
    def fromJson(self,jsonBlock):
        if isinstance(jsonBlock, dict):
            pool = []
            for transaction in jsonBlock['transactions']:
                pool.append(Transaction.fromJson(transaction))

            if(jsonBlock['typeBlock']=='data_blockchain'):
                block = Block(pool,jsonBlock['typeBlock'], jsonBlock['index'],jsonBlock['proof'],
                          jsonBlock['previousHash'], jsonBlock['timestamp'] )
            else:    
                     
                block = Block(pool,HostTrainer.fromJson(jsonBlock['hostTrainer']),jsonBlock['typeBlock'], jsonBlock['index'],jsonBlock['proof'],
                          jsonBlock['previousHash'], jsonBlock['timestamp'] )
            return block
        
        return jsonBlock