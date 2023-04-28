import streamlit as st
import sqlite3
import pandas as pd

def main():

    conn = sqlite3.connect('ma_base.db')
    cur = conn.cursor()

    # Interface utilisateur Streamlit
    st.title("Visualisation des consommations des clients")

    # Récupération de tous les IDs clients existants dans la table
    cur.execute("SELECT DISTINCT client_id FROM ma_table")
    clients = cur.fetchall()

    # Saisie de l'ID du client
    client_id = st.selectbox("Saisir l'ID du client", [client[0] for client in clients])

    # Récupération des consommations annuelles du client
    cur.execute("SELECT strftime('%Y', date) AS annee, round(SUM(valeur)) FROM ma_table WHERE client_id = ? GROUP BY strftime('%Y', date)", (client_id,))
    rows_an = cur.fetchall()

    # Récupération des consommations mensuelles du client
    cur.execute("SELECT strftime('%Y', date) || ' ' || strftime('%m', date) AS mois, round(SUM(valeur)) FROM ma_table WHERE client_id = ? GROUP BY strftime('%Y-%m', date)", (client_id,))
    rows_mois = cur.fetchall()

    # Fermeture de la connexion à la base de données
    cur.close()
    conn.close()

    # Création du dataframe pour les consommations annuelles
    df_an = pd.DataFrame(rows_an, columns=['annee', 'consommation_annuelle'])

    # Création du dataframe pour les consommations mensuelles
    df_mois = pd.DataFrame(rows_mois, columns=['mois', 'consommation_mensuelle'])

    # Formatage des données pour le dataframe final

    df_mois['annee'] = df_mois['mois'].str[:4]
    df_mois['mois'] = df_mois['mois'].str[-2:]
    df_mois['mois'] = pd.to_datetime(df_mois['mois'], format='%m').dt.month_name(locale='fr_FR')
    df = df_mois.pivot(index='annee', columns='mois', values='consommation_mensuelle')


    # Réorganisation des colonnes
    cols = list(df.columns)
    df = df[cols]

    # Renommage des index et colonnes
    df.index.name = 'Année'
    df.columns = [col.capitalize() for col in df.columns]


    # Affichage du dataframe final
st.write(f"Consommations du client {int(client_id)}")
st_table = st.experimental_data_editor(df, num_rows="dynamic")
