import streamlit as st
import pandas as pd
import sqlite3
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima.arima import auto_arima

# Connexion à la base de données SQLite3
conn = sqlite3.connect('ma_base.db')

# Lecture des données de consommation de la table 'consommation'
df = pd.read_sql_query("SELECT * FROM ma_table", conn, index_col='date', parse_dates=True)

# Fermeture de la connexion à la base de données
conn.close()

# Groupement des données par client
df_grouped = df.groupby('client_id')

# Boucle sur chaque client pour faire la prédiction de la consommation future
for client, data in df_grouped:
    # Sélection des colonnes de la consommation et suppression des valeurs manquantes
    df_cons = data[['valeur']].dropna()

    # Sélection des meilleurs paramètres SARIMA en utilisant la méthode AIC
    model = auto_arima(df_cons, seasonal=True, m=12, suppress_warnings=True)
    order = model.order
    seasonal_order = model.seasonal_order

    # Ajustement du modèle SARIMA sur les données de consommation avec les meilleurs paramètres trouvés
    model = SARIMAX(df_cons, order=order, seasonal_order=seasonal_order)
    result = model.fit()

    # Prédiction de la consommation future pour les années 2020 à 2024
    future_dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='MS')
    future = result.predict(start=len(df_cons), end=len(df_cons)+59, typ='levels')
    future.index = future_dates

    # Affichage de la prédiction pour chaque client
    st.write(f'Prévision de la consommation pour le client {client}:')
    st.line_chart(pd.concat([df_cons, future], axis=1).rename(columns={'consommation': 'Historique', 0: 'Prévision'}))
