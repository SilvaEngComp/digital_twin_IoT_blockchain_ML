"""
    This is a Smart contract wich gets a block from in Data Blockchain
"""
from .blockchain import Blockchain
from src.suport_layer.block import Block
import random
from src.suport_layer.cipher import Cipher
from src.utils.time_register import TimeRegister
import json
import os
class SC2:
    @staticmethod
    def minerNotAssinedTransaction(node, transactions,blockType="data"):
        TimeRegister.addTime("Transaction completed - initing mining")
        blockchain = Blockchain(node)
        before = 0
        if blockchain.chain is not None:
             before = len(blockchain.chain)
             print(f"size before {before}")

        blockchain.createBlock(transactions,blockType)
        after = len(blockchain.chain)
       
        if(after>before):
            TimeRegister.addTime("Block minered")
            return True
        else:
            return False 
    
    @staticmethod
    def getLasDataBlock(node = None):
        if node is not None:
            fileName = str("lastBlockReaded_"+str(node)+'.json')
            try:
                with open(fileName, 'rb') as blockchainFile:
                    if os.path.getsize(fileName) > 0:
                        cipher = Cipher()
                        data = blockchainFile.read()
                        decripted = cipher.decrypt(data)
                        dataJson = json.loads(decripted)
                        dataJson= Block.fromJson(dataJson)
                        return dataJson
            except:
                print('not found local blockchain file: ',fileName)
                return []