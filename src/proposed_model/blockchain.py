# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:22:31 2021

@author: silva
"""
from sys import getsizeof
from src.suport_layer.hostTrainer import HostTrainer
from src.suport_layer.cipher import Cipher
import re
from src.suport_layer.block import Block
import os
import json
from pathlib import Path
import hashlib


class Blockchain:
    def __init__(self, node="h1"):
        self.node = node
        self.prefix = os.path.dirname(os.path.abspath(__file__))
        self.blockchainType = "data_blockchain"
        self.fileName = str(self.blockchainType+"_"+str(self.node)+'.json')
        self.fileNameNotCript = str(
            'blockchain_notCript_'+"_"+str(self.node)+'.json')
        self.chain = self.initializeChain()
        self.nodes = set()
        self.cipher = Cipher()

    def initializeChain(self)->list:
        return self.solveBizzantineProblem()

    def __str__(self):

        return str({
            "chain": self.chain,
        })

    def __repr__(self):
        return str({
            "chain": self.chain,
        })

    def toJson(self):
        chain = []
        for block in self.chain:
            chain.append(Block.toJson(block))

        return {
            "chain": chain,
        }

    def toJsonDecrypted(self) -> dict:
        chain = []
        for block in self.chain:
            chain.append(Block.fromJsonDecrypt(Block.toJson(block)).toJson())


        return {
            "chain": chain,
        }

    @staticmethod
    def fromJson(data):
        try:
            if isinstance(data, list):
                chain = []
                for jsonBlock in data:
                    chain.append(Block.fromJson(jsonBlock))
                return chain
        except Exception as e:            
            print('That is not a dict object. Try it again!')
            print(e)
            return data

    def registerEncripted(self):
        self.fileName = str(self.prefix +"/"+self.blockchainType +
                            str(self.node)+'.json')
        try:
            dataBytes = json.dumps(self.toJson()).encode("utf-8")
            encrypted = self.cipher.encrypt(dataBytes)
            try:
                with open(self.fileName, 'wb') as f:
                    f.write(encrypted)
                    
                print('registring new chain in {} with {} blocks '.format(
                    self.fileName, len(self.chain)))
            except Exception as e:
                print("Erro ao registrar blockchain: ")
                print(e)
        except Exception as e:
            print("Erro ao converter chain para bytes ", self.fileName)
            print(e)

    def register(self):
        fileNameNotCript = str(self.prefix +"/"+self.fileNameNotCript)
        with open(fileNameNotCript, 'w') as blockchainFile:
            jsonData = self.toJsonDecrypted()
            print('registring new no encrypted chain in {} with {} blocks '.format(
                self.fileName, len(self.chain)))
            if jsonData is not None:
                json.dump(jsonData, blockchainFile)

    def createBlock(self, data, typeBlock="data", dataBlock=None):

        if typeBlock == "data":
            self.blockchainType = "data_blockchain"
            return self.createDataBlock(data)
        else:
            self.blockchainType = "consumer_blockchain"
            return self.createConsumerBlock(data, dataBlock)

    def createDataBlock(self, pool):
        try:
            previousBlock = self.getPreviousBlock()
            if previousBlock is None:
                print("initial block")
                block = Block(pool, self.blockchainType)
            else:
                proof = self.proofOfWork(previousBlock.proof)
                
                previousHash = self.hash(previousBlock)
                
                block = Block(pool, self.blockchainType,
                            (previousBlock.index+1), proof, previousHash)
            print(f'tamanho de um bloco minerado : {getsizeof(block)} bytes')
            self.chain.append(block)
            if (self.isChainValid(self.chain)):
                self.register()
                self.registerEncripted()
            else:
                self.chain = []

            return block
        except Exception as e:
            print('exception create block:')
            print(e)

    def createConsumerBlock(self, pool, dataBlock):
        if dataBlock is None:
            print('Some bad happens...data block is None')
            return None
        previousBlock = self.getPreviousBlock()
        index = dataBlock.index
        dataHash = self.hash(dataBlock)
        hostTrainer = HostTrainer(self.node, index, dataHash)
        if previousBlock is None:
            block = Block(pool, self.blockchainType, None,
                          None, None, None, hostTrainer)
        else:
            proof = self.proofOfWork(previousBlock.proof)
            previousHash = self.hash(previousBlock)
            block = Block(pool, self.blockchainType, (previousBlock.index+1),
                          proof, previousHash, None, hostTrainer)
        self.chain.append(block)
        if (self.isChainValid(self.chain)):
            self.register()
            self.registerEncripted()
        else:
            self.chain = []

        return block

    def getPreviousBlock(self):
        chain = self.solveBizzantineProblem()
        if(chain is not None):
            if len(chain)>0:
                return chain[-1]
        return None

    def proofOfWork(self, previous_proof, new_proof=1):
        if isinstance(previous_proof, str):
            previous_proof = int(previous_proof)
        if isinstance(new_proof, str):
            new_proof = int(new_proof)

        while True:
            hashOperation = self.getHashOperation(previous_proof, new_proof)
            if self.checkPuzzle(hashOperation) is True:
                break
            else:
                new_proof += 1
        return new_proof

    def checkPuzzle(self, hash_test):
        if hash_test[0:4] == '0000':
            return True
        return False

    def getHashOperation(self, previous_proof, new_proof):
        return hashlib.sha256(str(new_proof**2-previous_proof**2).encode("utf-8")).hexdigest()

    def hash(self, value):
        try:
            if isinstance(value, Block):
                value = str(value)
                encoded = json.dumps(value).encode("utf-8")
                return hashlib.sha256(encoded).hexdigest()
        except:
            print('It can not get the hash of not Block: ', type(value))
            return None

    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            previousBlockHash = self.hash(previousBlock)
            if block.previousHash != previousBlockHash:
                print('hashs diferents')
                return False
            previousProof = previousBlock.proof
            proof = block.proof
            hashOperation = self.getHashOperation(previousProof, proof)
            if self.checkPuzzle(hashOperation) is False:
                return False
            previousBlock = block
            blockIndex += 1
        return True

    def getLocalBLockchainFile(self, node=None):
        if node is not None:
            fileName = str(self.prefix +"/"  + node)

            try:
                with open(fileName, 'rb') as blockchainFile:
                    if os.path.getsize(fileName) > 0:
                        cipher = Cipher()
                        data = blockchainFile.read()
                        decripted = cipher.decrypt(data)
                        dataJson = json.loads(decripted)
                        dataJson = Blockchain.fromJson(dataJson['chain'])
                        return dataJson
            except Exception as e:
                print('229 - not found local blockchain file: ', node)
                print(e)
                return []

    def getBlockchainFileNames(self):
        fileNames = []
        for file in os.listdir(self.prefix ):
            if file.endswith(".json"):
                x = re.search("^"+self.blockchainType+".*json$", file)
                if (x):
                    fileNames.append(file)
        return fileNames

    def solveBizzantineProblem(self)->list:
        try:
            nodes = self.getBlockchainFileNames()
            longest_chain = None
            max_length = 0
            nameNode = None
            if (nodes):
                for node in nodes:
                    chain = self.getLocalBLockchainFile(node)
                    length = len(chain)
                    print(f'bizzantine chain len = {length}')
                    isValide = self.isChainValid(chain)
                    if length > max_length and isValide:
                        max_length = length
                        longest_chain = chain
                        nameNode = node
                        print(f'longest chain of node {nameNode}')
            else:
                longest_chain = []
           
            
            if longest_chain is None:
                return []
            else:
                print('The current biggest chain is {} with {} blocks'.format(
                nameNode, len(longest_chain)))
                return longest_chain

        except Exception as e:
            print('Something wrong happen in replaceChain...')
            print(e)
            return []
