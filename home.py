import streamlit as st

# Définir une fonction pour afficher chaque page
def page_accueil():
    st.write("Contenu de la page d'accueil")

def page_2():
    st.write("Contenu de la page 2")

def page_3():
    st.write("Contenu de la page 3")

# Créer un dictionnaire contenant les fonctions de chaque page
pages = {
    "dashb": page_accueil,
    "VisualisationGraph": page_2,
    "visualisationTableau": page_3
}

# Créer un conteneur pour chaque page
container_accueil = st.empty()
container_2 = st.empty()
container_3 = st.empty()

# Créer une barre de navigation avec un menu déroulant
selection = st.selectbox("Aller à", list(pages.keys()))

# Afficher le contenu de la page sélectionnée et cacher le contenu des autres pages
if selection == "dashb":
    container_accueil.write(pages["dashb"]())
    container_2.empty()
    container_3.empty()
elif selection == "VisualisationGraph":
    container_accueil.empty()
    container_2.write(pages["VisualisationGraph"]())
    container_3.empty()
elif selection == "visualisationTableau":
    container_accueil.empty()
    container_2.empty()
    container_3.write(pages["visualisationTableau"]())
