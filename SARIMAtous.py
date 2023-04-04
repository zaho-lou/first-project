import streamlit as st
import pandas as pd
import sqlite3
from pmdarima.arima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Connexion à la base de données SQLite3
conn = sqlite3.connect('ma_base.db')

# Lecture des données de consommation de la table 'consommation'
df = pd.read_sql_query("SELECT * FROM ma_table", conn, index_col='date', parse_dates=True)

# Fermeture de la connexion à la base de données
conn.close()

# Groupement des données de consommation par date
df_cons = df.groupby('date')['valeur'].sum().reset_index()
df_cons = df_cons.set_index('date')

# Sélection des meilleurs paramètres SARIMA en utilisant la méthode AIC
model = auto_arima(df_cons, seasonal=True, m=12, suppress_warnings=True)
order = model.order
seasonal_order = model.seasonal_order

# Ajustement du modèle SARIMA sur les données de consommation avec les meilleurs paramètres trouvés
model = SARIMAX(df_cons, order=order, seasonal_order=seasonal_order)
result = model.fit()

# Prédiction de la consommation future pour les 5 prochaines années
future_dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='MS')
future = result.predict(start=len(df_cons), end=len(df_cons)+59, typ='levels')
future.index = future_dates

# Affichage de la prédiction pour toutes les données
st.write('Prévision de la consommation pour les 5 prochaines années:')
st.line_chart(pd.concat([df_cons, future], axis=1).rename(columns={'consommation': 'Historique', 0: 'Prévision'}))

# Affichage des données de prédiction dans un tableau
st.write('Données de prédiction :')
st.write(future.to_frame(name='Prévision'))
