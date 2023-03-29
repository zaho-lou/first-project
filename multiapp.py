from dashb import app as app1
from visualisationTab import app as app2
from VisualisationGraph import app as app3
import streamlit as st

app_dict = {
    "Dashboard": app1,
    "visualisationTab": app2,
    "VisualisationGraph": app3
}

def run_app():
    app = st.sidebar.selectbox(
        "Sélectionnez une application",
        list(app_dict.keys())
    )
    app_func = app_dict[app]
    app_func()

if __name__ == '__main__':
    run_app()
