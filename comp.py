import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Connexion à la base de données
conn = sqlite3.connect('ma_base.db')

# Chargement des données dans un dataframe Pandas
df = pd.read_sql_query("SELECT * FROM ma_table", conn)

# Sélection d'un client spécifique
client = st.sidebar.selectbox("Sélectionnez un client :", df['client_id'].unique())

# Filtre les données pour n'afficher que celles du client sélectionné
df_client = df[df['client_id'] == client]

# Conversion de la colonne de dates en un objet DatetimeIndex
df_client['date'] = pd.to_datetime(df_client['date'])
df_client = df_client.set_index('date')

# Extraction des données pour le mois de mars 2018 et le mois de mars 2019
data_2018 = df_client.loc['2018-03']
data_2019 = df_client.loc['2019-03']

# Graphique de la consommation pour le mois de mars 2018 et 2019
fig, ax = plt.subplots()
ax.plot(data_2018['valeur'], label='2018')
ax.plot(data_2019['valeur'], label='2019')
ax.set_title(f"Comparaison de la consommation en Mars pour le client {client}")
ax.set_xlabel("Jour")
ax.set_ylabel("Consommation (kWh)")
ax.legend()
st.pyplot(fig)

# Calcul de la différence de consommation entre les deux années
diff = data_2019['valeur'].sum() - data_2018['valeur'].sum()

# Affichage de la différence de consommation
st.write(f"Le client {client} a consommé {diff} kWh de plus en mars 2019 par rapport à mars 2018.")
