import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from statsmodels.tsa.statespace.sarimax import SARIMAX
import streamlit as st

# Connexion à la base de données SQLite3
conn = sqlite3.connect('ma_base.db')

# Fonction pour obtenir les données de consommation du client
def get_client_data(client_id):
    query = f"SELECT * FROM ma_table WHERE client_id = '{client_id}'"
    df = pd.read_sql_query(query, conn)
    return df.set_index('date')


# Fonction pour prédire la consommation future du client en utilisant SARIMA
def predict_future_consumption(client_id):
    # Obtenir les données de consommation du client
    data = get_client_data(client_id)

    # Préparer les données pour la modélisation SARIMA
    ts = data['valeur']
    ts.index = pd.to_datetime(ts.index)
    ts = ts.resample('D').sum().fillna(0)

    # Entraîner le modèle SARIMA sur les données historiques
    model = SARIMAX(ts, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results = model.fit()

    # Prédire la consommation future du client pour les 5 prochaines années
    future_dates = pd.date_range(start=ts.index[-1], periods=365 * 5, freq='D')[1:]
    future_ts = pd.Series(results.predict(start=len(ts), end=len(ts) + len(future_dates) - 1), index=future_dates)

    # Plot the predicted future consumption
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ts, label='Historique')
    ax.plot(future_ts, label='Prédiction')
    ax.legend()
    ax.set_title(f'Consommation prévue pour le client {client_id}')
    ax.set_xlabel('date')
    ax.set_ylabel('valeur')
    st.pyplot(fig)
    plt.show()

    # Retourner les prédictions pour les 5 prochaines années
    return future_ts


# Interface Streamlit pour entrer l'id du client et obtenir la prédiction de la consommation future
st.title('Prédiction de la consommation future des clients')

# Obtenir l'id du client à partir de l'utilisateur
client_id = st.text_input('client_id')

if client_id:
    try:
        future_consumption = predict_future_consumption(client_id)
        st.write(future_consumption)
    except:
        st.write("Une erreur s'est produite. Veuillez vérifier l'ID du client et réessayer.")
