import streamlit as st

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)

st.title("Main Page")
st.sidebar.success("Select a page above.")

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Input a text here", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    st.session_state["my_input"] = my_input
    st.write("You have entered: ", my_input)


# page1.py
import streamlit as st

def app():
    st.title("Page 1")
    st.write("Contenu de la page 1")

# page2.py
import streamlit as st

def app():
    st.title("Page 2")
    st.write("Contenu de la page 2")

# app.py
import streamlit as st
from dashb import app as dashb
from page2 import app as page2

# Créer un dictionnaire qui associe les noms de page à leurs fonctions
pages = {
    "Page 1": page1,
    "Page 2": page2
}

# Utiliser la barre latérale pour permettre à l'utilisateur de sélectionner une page
selection = st.sidebar.selectbox("Choisir une page", list(pages.keys()))

# Afficher la page sélectionnée
page = pages[selection]
page()
