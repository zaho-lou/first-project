import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Connexion à la base de données
conn = sqlite3.connect('ma_base.db')


# Fonction pour récupérer les données du client pour une année donnée
def get_customer_data_for_year(client_id, year):
    query = f"SELECT * FROM ma_table WHERE client_id={client_id} AND strftime('%Y', date)='{year}'"
    df = pd.read_sql(query, conn)
    return df

df = pd.read_sql_query("SELECT * FROM ma_table", conn)

# Fonction pour calculer les consommations mensuelles pour une année donnée
def get_monthly_consumptions_for_year(df):
    monthly_consumptions = df.groupby(['annee', 'mois'])['valeur'].sum()
    return monthly_consumptions

# Interface Streamlit
st.title('Visualisation des consommations des clients par année')

# Sélection de l'id du client
client_id = st.sidebar.selectbox("Sélectionnez un client :",df['client_id'].unique())

# Sélection de l'année
now = datetime.now()
selected_year = st.sidebar.selectbox('Sélectionnez une année', range(now.year - 17, now.year + 1))

if client_id:
    # Récupération des données du client pour l'année sélectionnée
    df = get_customer_data_for_year(client_id, str(selected_year))

    # Ajout des colonnes 'annee' et 'mois' à partir de la colonne 'date'
    df['annee'] = pd.DatetimeIndex(df['date']).year
    df['mois'] = pd.DatetimeIndex(df['date']).month

    # Calcul des consommations mensuelles pour l'année sélectionnée
    monthly_consumptions = get_monthly_consumptions_for_year(df)

    # Affichage des consommations annuelles et mensuelles
    st.write(f'Consommations pour l\'année {selected_year} :')
    st.write(monthly_consumptions)
