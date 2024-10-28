# ui_components/intel_lab.py
import streamlit as st
import pandas as pd

def show_compare_time_operations():
    col1,col2 = st.columns(2)
    with col1:
        st.header("Current IoT time proccess")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../current_model/commom_IoT_collector.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
        
        st.header("RFoT time proccess  challenge 5")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../proposed_model/RFoT_collector_challenge_5.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
        
        st.header("RFoT time proccess  challenge 7")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../proposed_model/RFoT_collector_challenge_7.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
    with col2:
        st.header("RFoT time proccess challenge 4")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../proposed_model/RFoT_collector_challenge_4.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
        
        st.header("RFoT time proccess challenge 6")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../proposed_model/RFoT_collector_challenge_6.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))