# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:22:31 2021

@author: silva
"""
import sys
sys.path.insert(0,'/home/mininet/mininet_blockchain_ml/proposed_model/data_collector')

import time
import datetime
import hashlib
import json
import os
import ast
from block import Block
from transaction import Transaction
from node import Node
import re
from pool import Pool


class Blockchain:
    def __init__(self, node):
        self.node = node
        self.fileName = str('blockchain_'+str(self.node)+'.json')
        self.chain = []
        self.nodes = set()


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
        
    @classmethod
    def fromJson(self, data):
        try:
            if isinstance(data, list):
                chain = []
                for jsonBlock in data:
                    chain.append(Block.fromJson(jsonBlock))  
                return chain
        except:
            if isinstance(data, Blockchain(node)):
                return data
            print('That is not a dict object. Try it again!')

    def register(self, prefix="../data_collector/"):
        fileName = str(prefix + self.fileName) 
        with open(fileName,"w") as blockchainFile:
            print('registring new chain in {} with {} blocks '.format(self.fileName, len(self.chain)))
            json.dump(self.toJson(), blockchainFile)


    def createBlock(self, pool):
        previousBlock = self.getPreviousBlock()
        if previousBlock is None:
            block = Block(pool, self.node)
        else:
            proof = self.proofOfWork(previousBlock.proof)
            previousHash = self.hash(previousBlock)
            block = Block(pool,self.node,(previousBlock.index+1),proof,previousHash)
        
        self.chain.append(block)
        if(self.isChainValid(self.chain)):
            self.register()
        else:
            self.chain = []
        return block
            
        


    def getPreviousBlock(self)->Block: 
        chain = Blockchain.solveBizzantineProblem()
        if chain is None:
            return None
        elif len(chain)>0:            
            self.chain = chain          
            return self.chain[-1]
        return None
                                    

    def proofOfWork(self, previous_proof, new_proof = 1):
        if isinstance(previous_proof,str):
            previous_proof = int(previous_proof)
        if isinstance(new_proof,str):
            new_proof = int(new_proof)
        
        while True:
            hashOperation = self.getHashOperation(previous_proof, new_proof)
            if self.checkPuzzle(hashOperation) is True:
                break
            else:
                new_proof +=1
        return new_proof                            

    @staticmethod
    def checkPuzzle(hash_test):
        if hash_test[0:4]=='0000':
            return True
            return False
    @staticmethod
    def getHashOperation(previous_proof, new_proof):
        return hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
        
        
    @staticmethod
    def hash(value):
        try:
            if isinstance(value, Block):
                value = str(value)
                encoded = json.dumps(value).encode()
                return hashlib.sha256(encoded).hexdigest()
        except:
            print('It can not get the hash of not Block: ',type(value))
            return None
        
    @staticmethod
    def isChainValid(chain):
        previousBlock = chain[0]
        blockIndex=1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            previousBlockHash = Blockchain.hash(previousBlock)
            if block.previousHash != previousBlockHash:
                return False
            previousProof = previousBlock.proof
            proof = block.proof
            hashOperation = Blockchain.getHashOperation(previousProof, proof)
            if Blockchain.checkPuzzle(hashOperation) is False:
                return False
            previousBlock = block
            blockIndex += 1
        return True


    @staticmethod      
    def getLocalBLockchainFile(node = None, prefix='../data_collector/'):
        if node is not None:
            x = re.search("^blockchain.*json$", node)
            if(x is False):
                fileName = str(prefix + 'blockchain_'+node+'.json')   
            else:
                fileName = str(prefix + node) 
            if os.path.exists(fileName) is False:
                return []
            try:
                with open(fileName) as blockchainFile:
                    if os.path.getsize(fileName) > 0:
                        data = json.load(blockchainFile)['chain']
                        return Blockchain.fromJson(data)
            except:
                print('not found local blockchain file: ',node)
                return []
    
    @staticmethod  
    def getBlockchainFileNames(prefix='../data_collector/'):
        fileNames = []
        for file in os.listdir(prefix):
            if file.endswith(".json"):
                x = re.search("^blockchain.*json$", file)
                if(x):
                    fileNames.append(file)
        return fileNames
                    
    @staticmethod          
    def solveBizzantineProblem():
        try:            
            nodes = Blockchain.getBlockchainFileNames()
            longest_chain = None
            max_length = 0
            nameNode=None
            if(nodes):
                for node in nodes:
                    chain = Blockchain.getLocalBLockchainFile(node)
                    length = len(chain)
                    isValide = Blockchain.isChainValid(chain)
                    if length>max_length and isValide:
                        max_length = length
                        longest_chain = chain
                        nameNode = node
            else:
                longest_chain = []
            print('The current biggest chain is {} with {} blocks'.format(nameNode, len(longest_chain)))
            return longest_chain
        except:
            print('Something wrong happen in replaceChain...')
            
    @staticmethod
    def getNotAssinedBlock(node):
        transaction = Pool.getNotAssinedTransactions()      
        
        blockchain = Blockchain(node)
        return  blockchain.createBlock(transaction)
