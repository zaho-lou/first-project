import sqlite3
import pandas as pd
import streamlit as st
import base64

import io

# Fonction pour télécharger les données sous format Excel
def download_link(df, filename, link_text):
    excel_file = io.BytesIO()
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    excel_file.seek(0)
    b64 = base64.b64encode(excel_file.read()).decode()
    href = f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}"
    st.markdown(f'<a href="{href}" download="{filename}">{link_text}</a>', unsafe_allow_html=True)

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

# Calcul de la somme des consommations pour chaque mois
monthly_data = df_client.resample('M')['valeur'].sum()

# Calcul de la variation de consommation par rapport au mois précédent
variation = monthly_data.pct_change()

# Affichage des données mensuelles et de la variation
st.write(f"Consommation mensuelle pour le client {client} :")
editable_monthly_data = st.dataframe(monthly_data)
st.write(f"Taux de variation de consommation mensuelle pour le client {client} :")
editable_variation = st.dataframe(variation)

# Ajout d'un bouton de téléchargement des données sous format Excel
if st.button("Télécharger les données sous format Excel"):
    download_link(df_client, f"donnees_client_{client}.xlsx", "Télécharger")