# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 12:07:56 2021

@author: silva

This is a Smart contract wich receive data collected by sensor and received by gateway
and call for SC2 to miner a block for a transaction
"""

from sys import getsizeof
from corruptedBlockchain import CorruptedBlockchain
from .smart_contract_2 import SC2
from src.suport_layer.transaction import Transaction
import json
from src.suport_layer.cipher import Cipher
from src.utils.time_register import TimeRegister

class SC1:
    def __init__(self, node, blockWidth=20):
        self._node = node
        self._blockWidth = self.checkBlockWidth(blockWidth)
        self._transactions = []

    def dataTreating(self, msg):
        msgJson = json.loads(msg.payload)
        if 'data' in msgJson:
            transaction = Transaction(
                msgJson['header']['device'], msgJson['header']['sensor'], self._node, msgJson['data'])
            return self.mineBlock(transaction)
        return False

    def validTemp(self, temp):
        decryptedTemp = self.dataDecrypt(temp)
        if float(decryptedTemp) > 16 and float(decryptedTemp) < 40:
            return True
        return False

    def dataDecrypt(self, temp):
        cipher = Cipher()
        temp = temp.replace("b'", "'")
        temp = str.encode(temp)
        decriptedTemp = cipher.decrypt(temp)
        return json.loads(decriptedTemp)
        
    def mineBlock(self, transaction):
        self._transactions.append(transaction)
        print("{}/{} - {}".format(len(self._transactions),
              self._blockWidth, self.dataDecrypt(transaction.data)))

        if len(self._transactions) >= self._blockWidth:
            print(f'tamanho pacote com {self._blockWidth} amostras : {getsizeof(self._transactions)} bytes')
            print("A new Block was minner? = ", SC2.minerNotAssinedTransaction(
                self._node, self._transactions))
            return True
        elif len(self._transactions)==1:
            TimeRegister.addTime("Starting collection")
            
        return False

    def checkBlockWidth(self, blockWidth):
        if (blockWidth is None):
            blockWidth = 20
        elif isinstance(blockWidth, str):
            blockWidth = int(blockWidth)
        return blockWidth

    def restart(self):
        self._transactions = []

    def corruptData(self, transaction):
        self._transactions.append(transaction)
        print("{}/{}".format(len(self._transactions), self._blockWidth))

        if len(self._transactions) >= self._blockWidth:
            CorruptedBlockchain.corruptBlockchain()
            return True
        return False
