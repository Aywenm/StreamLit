# Ajouter du CSS personnalisé
import streamlit as st

def add_custom_css():
    st.markdown("""
        <style>
        .main-title {
            font-size: 2em;
            color: #4CAF50;
            text-align: center;
        }
        .duration {
            font-size: 1.2em;
            color: #4CAF50;
        }
        [data-testid=stSidebar] {
            background-color: #ff000050;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">Bienvenue à mon application Streamlit</h1>', unsafe_allow_html=True)

# Call the function to add the custom CSS
add_custom_css()