import streamlit as st
import sqlite3
import hashlib
import secrets

# Fonctions pour la base de données

def create_usertable():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, salt TEXT)')
    conn.commit()
    conn.close()

def add_userdata(username, password, salt):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password, salt) VALUES (?,?,?)', (username, password, salt))
    conn.commit()
    conn.close()

def get_userdata(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    data = c.fetchone()
    conn.close()
    return data

# Fonction de hachage de mot de passe

def hash_password(password, salt):
    hash_object = hashlib.sha256(salt.encode() + password.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig

# Fonction de création de sel

def create_salt():
    return secrets.token_hex(16)

# Fonction pour la page de connexion

def login():
    st.title("Page de connexion")

    # Création de la table utilisateurs
    create_usertable()

    # Création du formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type='password')

    if st.button("Se connecter"):
        user_data = get_userdata(username)
        if user_data:
            hashed_password = hash_password(password, user_data[3])
            if hashed_password == user_data[2]:
                st.success("Connecté en tant que {}".format(username))
                return True
            else:
                st.warning("Nom d'utilisateur ou mot de passe incorrect")
        else:
            st.warning("Nom d'utilisateur ou mot de passe incorrect")

    return False

# Fonction pour la page d'inscription

def signup():
    st.title("Page d'inscription")

    # Création de la table utilisateurs
    create_usertable()

    # Création du formulaire d'inscription
    new_username = st.text_input("Nom d'utilisateur", key='new_username')
    new_password = st.text_input("Mot de passe", type='password', key='new_password')

    if st.button("S'inscrire"):
        salt = create_salt()
        hashed_password = hash_password(new_password, salt)
        add_userdata(new_username, hashed_password, salt)
        st.success("Compte créé avec succès")
        st.info("Veuillez vous connecter pour accéder à l'application")

# Fonction pour la page dashboard

def dashboard():
    st.title("Page d'accueil")

    # Contenu de la page d'accueil

    st.write("Bienvenue sur notre application")

# Programme principal

def main():
    state = {"loggedin": False}

    if state["loggedin"] == False:
        if login():
            state["loggedin"] = True
        else:
            signup()

    if state["loggedin"] == True:
        dashboard()

if __name__ == '__main__':
    main()
