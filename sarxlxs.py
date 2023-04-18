import streamlit as st
import pandas as pd
import sqlite3
from pmdarima.arima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
from openpyxl.workbook import workbook


# Connexion à la base de données SQLite3
conn = sqlite3.connect('ma_base.db')

# Lecture des données de consommation de la table 'consommation'
df = pd.read_sql_query("SELECT * FROM ma_table", conn)

# Fermeture de la connexion à la base de données
conn.close()

# Groupement des données de consommation par date
df_cons = df.groupby('date')['valeur'].sum().reset_index()
df_cons = df_cons.set_index('date')

# Sélection des données historiques
train = df_cons[:'2019-12-01']

# Sélection des meilleurs paramètres SARIMA en utilisant la méthode AIC
model = auto_arima(train, seasonal=True, m=12, suppress_warnings=True)
order = model.order
seasonal_order = model.seasonal_order

# Ajustement du modèle SARIMA sur les données de consommation avec les meilleurs paramètres trouvés
model = SARIMAX(train, order=order, seasonal_order=seasonal_order)
result = model.fit()

# Prédiction de la consommation future pour les 5 prochaines années
future_dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='MS')
future = result.predict(start=len(train), end=len(train)+59, typ='levels')
future.index = future_dates

# Concaténation des données historiques et de prévisions dans un tableau
table_data = pd.concat([train, future], axis=1)
table_data.columns = ['Historique', 'Prévisions']

# Affichage des données dans un tableau
st.write('Données historiques et de prévisions :')
st.table(table_data)

# Affichage des données dans un tableau éditable
st.write('Données historiques et de prévisions :')
editable_table = st.table(table_data)


# Exportation du tableau éditable au format Excel
wb = openpyxl.Workbook()
ws = wb.active
for r in dataframe_to_rows(table_data, index=False, header=True):
    ws.append(r)

# Enregistrer le fichier Excel dans un buffer mémoire
data = BytesIO()
wb.save(data)

# Afficher le bouton de téléchargement
st.write('Télécharger le tableau éditable sous forme de fichier Excel')
st.download_button(label="Télécharger le fichier Excel", data=data, file_name="tableau_editable.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")