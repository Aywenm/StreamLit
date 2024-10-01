import streamlit as st
my_var = 'voici le premier texte'
txt = st.text_area(
    "Text to analyze",
    "It was the best of times, it was the worst of times, it was the age of "
    "wisdom, it was the age of foolishness, it was the epoch of belief, it "
    "was the epoch of incredulity, it was the season of Light, it was the "
    "season of Darkness, it was the spring of hope, it was the winter of "
    "despair, (...)",
)
def main():
    st.header("Home page")
    st.title("notre apli pour selectionner le meilleur trajet")
    st.write(my_var)
    st.write(f"You wrote {len(txt)} characters.")
if __name__ == '__main__':
    main()