# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:22:31 2021

@author: silva
"""
import random
from src.suport_layer.cipher import Cipher
from src.suport_layer.hostTrainer import HostTrainer
import hashlib
import json
import os
from src.suport_layer.block import Block
from src.suport_layer.transaction import Transaction
import re
from src.dashboard.cenary4.blockchain import Blockchain

class CorruptedBlockchain:
    

    @staticmethod      
    def getLocalBLockchainFile(node=None):
        prefix = os.path.dirname(os.path.abspath(__file__))
        if node is not None:
            fileName = str(prefix +"/"  + node)

            try:
                with open(fileName, 'rb') as blockchainFile:
                    
                    if os.path.getsize(fileName) > 0:
                        cipher = Cipher()
                        data = blockchainFile.read()
                        decripted = cipher.decrypt(data)
                        dataJson = json.loads(decripted)
                        dataJson = Blockchain.toJsonDecrypted(dataJson['chain'])
                        return dataJson
            except Exception as e:
                print('229 - not found local blockchain file: ', node)
                print(e)
                return []
    
    @staticmethod  
    def getBlockchainFileNames():
        prefix = os.path.dirname(os.path.abspath(__file__))
        fileNames = []
        for file in os.listdir(prefix):
            if file.endswith(".json"):
                x = re.search("^data_blockchain.*json$", file)
                if(x):
                    fileNames.append(file)
        return fileNames
    
    @staticmethod 
    def register(corruptedBlockchain, node):
        try:
            with open(node,"w") as blockchainFile:
                print('corrupting {}...  '.format(node))
                cipher = Cipher()
                dataBytes = json.dumps(Blockchain.toJson(corruptedBlockchain)).encode("utf-8")
                encrypted = cipher.encrypt(dataBytes)
                json.dump(encrypted.decode(), blockchainFile)
        except Exception as e:
            print('File registring error...')
            print(e)
            
    @staticmethod          
    def corruptBlockchain():
        try:            
            nodes = CorruptedBlockchain.getBlockchainFileNames()
            print(nodes)
            if(nodes):
                for node in nodes:
                    if("data_blockchainh3.json" == node):
                        continue
                        
                    chain = CorruptedBlockchain.getLocalBLockchainFile(node)
                    if(len(chain['chain'])>0):
                        cipher = Cipher()
                        corruptedChain=[]
                        for block in chain['chain']:
                            corruptedTransactions=[]
                            # print(block)
                            for item in block['transactions']:
                                # print(item)
                                temperature = str(random.randint(1, 1000))
                                humidity = str(random.randint(1, 1000))
                                
                                sensorNode = {"temperature":temperature,"humidity":humidity}
                                # print(sensorNode)
                                dataBytes = json.dumps(sensorNode).encode("utf-8")
                                # print(dataBytes)
                                encrypted= cipher.encrypt(dataBytes)
                                # print(encrypted)
                                newItem = Transaction(item["sender"],item["sensor"], item["receiver"],encrypted.decode())
                                # print(newItem)
                                corruptedTransactions.append(newItem)
                            
                        
                            corruptedBlock = Block(corruptedTransactions,block['typeBlock'], int(block['index']),int(block['proof']),block['previousHash'], block['timestamp'],None)
                            corruptedChain.append(corruptedBlock)
                        print(Blockchain.toJson(corruptedChain))
                        CorruptedBlockchain.register(corruptedChain, node)
                        
        except Exception as e:
            print('Something wrong happen in replaceChain...')
            print(e)
    
          
    