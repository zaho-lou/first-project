import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')



# Connexion à la base de données

conn = sqlite3.connect('ma_base.db')
c = conn.cursor()

    # Fonction pour récupérer les données du client pour l'année spécifiée
def get_customer_data(client_id, year):
    query = f"SELECT date, valeur FROM ma_table WHERE client_id = {client_id} AND strftime('%Y', date) = '{year}'"
    result = c.execute(query).fetchall()
    return result

# Fonction pour transformer les données en un DataFrame Pandas
def transform_data(data):
    df = pd.DataFrame(data, columns=['date', 'valeur'])
    df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m'))
    df = df.groupby(['date'])['valeur'].sum().reset_index()
    return df

# Fonction pour afficher le graphique
def show_plot(data):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(28,11))
    fig.suptitle('Consommations mensuelles pour l\'année sélectionnée')
    ax1.bar(data['date'], data['valeur'], color='purple')
    ax1.set_title('Barres')
    ax1.set_xlabel('Mois')
    ax1.set_ylabel('valeur')
    ax2.plot(data['date'], data['valeur'], color='orange')
    ax2.set_title('Linéaire')
    ax2.set_xlabel('Mois')
    ax2.set_ylabel('valeur')
    st.pyplot(fig)

df = pd.read_sql_query("SELECT * FROM ma_table", conn)

# Interface utilisateur Streamlit
st.title('Visualisation des consommations des clients')
client_id = st.sidebar.selectbox("Sélectionnez un client :", df['client_id'].unique())

now = datetime.now()
year = st.sidebar.selectbox('Sélectionnez une année', range(now.year - 17, now.year + 1))

data = get_customer_data(client_id, year)
df = transform_data(data)
show_plot(df)

# Fermer la connexion à la base de données
c.close()
conn.close()
