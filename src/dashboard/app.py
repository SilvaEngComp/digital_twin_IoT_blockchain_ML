import streamlit as st
from intel_lab.intel_lab import show_intel_lab_dataset
import pandas as pd
from src.proposed_model.smart_contract_3 import SC3
import base64
from cenary1.cenary1 import Cenary1
from cenary2.cenary2 import Cenary2
from cenary3.cenary3 import Cenary3
from cenary4.cenary4 import Cenary4
from general_components.compare_time_operations import show_compare_time_operations
from utils.utils import get_image_base64

# Import other UI components as needed
import os

def main():
    config_page()
    config_sidebar()

def config_sidebar():

    # Example of integrating the "Intel Lab Dataset" button
    if st.sidebar.button("Intel Lab Dataset"):
        show_intel_lab_dataset()
    # Set Streamlit page configuration
    # Sidebar navigation
    if st.sidebar.button("Cenário 1"):
        Cenary1.show_data_collected()


    if st.sidebar.button("Cenário 2"):
        Cenary2.show_data_collected()

        
    if st.sidebar.button("Cenário 3"):
        # Cenary3.show_data_collected()
        Cenary3.show_blockchains()

        
    if st.sidebar.button("Cenário 4"):
        Cenary4.show_data_collected()
        Cenary4.show_corrupted_data_collected()

    if st.sidebar.button("Aálise do Tempo de Colleta"):
        show_compare_time_operations()

def config_page():
    image_url = get_image_base64("images/wiser.png")
    logo = get_image_base64("images/logo_url.png")

    st.set_page_config(page_title="RFoT Dashboard", page_icon=logo, layout="wide")

    st.sidebar.title("Dashboard Menu")
    # Apply custom CSS for styling
    local_css("style.css")

    st.header("Dashboard Experimentos RFoT")

    # Embed the image with custom CSS in Streamlit
    st.markdown(f'<img src="{image_url}" class="top-right-image">', unsafe_allow_html=True)


# Custom CSS to inject for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()