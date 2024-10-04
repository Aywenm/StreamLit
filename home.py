import streamlit as st
from css import add_custom_css
st.markdown("""
        <style>
        
        .title {
            font-size: 1.5em;
            color: #4CAF50;
        }
        .p{
            font-size: 1.2em;
            color: #4CAF50;
        }
        """, unsafe_allow_html=True)



    
def main():
    add_custom_css()  
    st.markdown('<h2 class="title">notre apli pour selectionner le meilleur trajet</h2>', unsafe_allow_html=True)
    st.markdown('<p class="p">trajet en avion ou en voiture, velo ou a pied, vous est flash ? cette apli est faite pour vous</p>', unsafe_allow_html=True)
if __name__ == '__main__':
    main()