# ui_components/intel_lab.py
import json
import os
import re
import streamlit as st
import pandas as pd
from time import sleep
from src.dashboard.cenary4.blockchain import Blockchain
from src.proposed_model.smart_contract_3 import SC3
from src.suport_layer.cipher import Cipher
class Cenary3:
    @staticmethod
    def show_data_collected():
        st.header("# Data Blockchain")
        st.text("This is the data collected and registred in BCD (Data Blockchain)")
        blockchain = SC3.getBCD()
        
        st.write("# There are ",str(len(blockchain.chain))+" blocks")
        st.write(blockchain.toJsonDecrypted())
    @staticmethod
    def dataset_training():
        df = pd.read_csv('dataset.csv', delimiter=",")
        st.dataframe(df)
    @staticmethod
    def training_results():
        st.header("Current IoT time proccess")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('prediction.csv', delimiter=",")
        edit_df = st.data_editor(df,key="df_editor", on_change=def_on_change, args=[df])
        
        st.line_chart(df,color=['blue','red'])
                
        while True:
            sleep(5)
            df = pd.read_csv('../prediction.csv', delimiter=",")
    # Define a function to update the dataframe based on user edits
    def def_on_change(df):
        state = st.session_state["df_editor"]
        for index, change_dict in state["edited_rows"].items():
            df.loc[df.index == index, "edited"] = True

        if st.sidebar.button("Consumer Dataset"):
            st.header("Temperature from Intel Lab Dataset")
            df = pd.read_csv('dataset.csv', delimiter=",")
            st.dataframe(df)
    @staticmethod
    def show_blockchains():
        
        st.header("# Lista de Blockchains com os modelos resultantes do treinamento")
        # st.header("# Blockchain Corrompida")
        nodes = Cenary3.getBlockchainFileNames()
        col1,col2 = st.columns(2)
    
        if(nodes):
            print(nodes)
            cont=0
            for node in nodes:
                if cont%2==0:
                    with col1:
                        st.write(f'# Name: {node}')
                        # st.write(f'# Nome: {node}')
                        chain = Cenary3.getLocalBLockchainFile(node)
                        print(chain)
                        # st.write("### Contém ",str(len(chain['chain']))+" blocos")
                        st.write("### Contains ",str(len(chain['chain']))+" blocks")
                        st.write(chain['chain'])
                else:
                    with col2:
                        st.write(f'# Name: {node}')
                        # st.write(f'# Nome: {node}')
                        chain = Cenary3.getLocalBLockchainFile(node)
                        # st.write("### Contém ",str(len(chain['chain']))+" blocos")
                        st.write("### Contains ",str(len(chain['chain']))+" blocks")
                        st.write(chain['chain'])
                cont+=1
    @staticmethod  
    def getBlockchainFileNames():
        prefix = os.path.dirname(os.path.abspath(__file__))
        fileNames = []
        for file in os.listdir(prefix):
            if file.endswith(".json"):
                x = re.search("^data_blockchain.*json$", file) or re.search("^consumer_blockchain.*json$", file)
                if(x):
                    fileNames.append(file)
        return fileNames
    
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
                        print('data = {data}')
                        decripted = cipher.decrypt(data)
                        dataJson = json.loads(decripted)
                        dataJson = Blockchain.toJsonDecrypted(dataJson['chain'])
                        return dataJson
            except Exception as e:
                print('229 - not found local blockchain file: ', node)
                print(e)
                return []