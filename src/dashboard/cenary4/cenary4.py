# ui_components/intel_lab.py
import streamlit as st
import pandas as pd
from time import sleep
from src.dashboard.cenary4.smart_contract_3 import SC3
from src.dashboard.cenary4.corruptedBlockchain import CorruptedBlockchain
from src.dashboard.cenary4.blockchain import Blockchain
class Cenary4:
    @staticmethod
    def show_data_collected():
        # st.header("# Blockchain Válida")
        # st.write(f'## Nome: data_blockchainh3.json')
        # st.text("Esses são os dados coletados e registrado na BCD (Blockchain de Dados)")
        st.header("# Valid Blockchain")
        st.write(f'## Name: data_blockchainh3.json')
        st.text("This is the data collected and registred in BCD (Data Blockchain)")
        blockchain = SC3.getBCD()
        
        st.write("# Existem ",str(len(blockchain.chain))+" blocos")
        # st.write("# There are ",str(len(blockchain.chain))+" blocks")
        st.write(Blockchain.toJsonDecrypted(blockchain.chain))

    @staticmethod
    def show_corrupted_data_collected():
        
        st.header("# Corrupted Blockchain")
        # st.header("# Blockchain Corrompida")
        nodes = CorruptedBlockchain.getBlockchainFileNames()
        col1,col2 = st.columns(2)
    
        if(nodes):
            cont=0
            for node in nodes:
                if node=='data_blockchainh3.json':
                    continue
                if cont%2==0:
                    with col1:
                        st.write(f'# Name: {node}')
                        # st.write(f'# Nome: {node}')
                        chain = CorruptedBlockchain.getLocalBLockchainFile(node)
                        # st.write("### Contém ",str(len(chain['chain']))+" blocos")
                        st.write("### Contains ",str(len(chain['chain']))+" blocks")
                        st.write(chain['chain'])
                else:
                    with col2:
                        st.write(f'# Name: {node}')
                        # st.write(f'# Nome: {node}')
                        chain = CorruptedBlockchain.getLocalBLockchainFile(node)
                        # st.write("### Contém ",str(len(chain['chain']))+" blocos")
                        st.write("### Contains ",str(len(chain['chain']))+" blocks")
                        st.write(chain['chain'])
                cont+=1
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