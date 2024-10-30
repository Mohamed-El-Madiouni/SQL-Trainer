"""
Module principal de l'application SQL Trainer.

Ce fichier initialise la base de données,
charge les exercices et les solutions SQL, et fournit une interface
interactive avec Streamlit pour que les utilisateurs puissent pratiquer SQL.
"""

import os

import duckdb
import streamlit as st

from init_db import initialize_database_tables


def connect_db(name: str) -> duckdb.DuckDBPyConnection:
    """Connecte à la base de données DuckDB.

    :param name: Nom du fichier de base de données.
    :returns: Objet de connexion à la base de données.
    """
    return duckdb.connect(database=f"./data/{name}", read_only=False)


def init_database(name: str) -> None:
    """Initialise la base de données en créant le dossier de données et les tables nécessaires.

    :param name: Nom du fichier de base de données.
    """
    # Crée le dossier s'il n'existe pas
    if "data" not in os.listdir():
        os.mkdir("data")

    # Initialise la base de données si le fichier n'existe pas
    if name not in os.listdir("data"):
        con = connect_db(name)
        initialize_database_tables(con)  # Initialisation des tables
        con.close()


def init_session_state() -> None:
    """Initialise les variables de l'état de session Streamlit pour l'option,
    l'exercice et la requête de l'utilisateur."""

    if "option" not in st.session_state:
        st.session_state.option = ""
    if "exercise" not in st.session_state:
        st.session_state.exercise = ""
    if "user_query" not in st.session_state:
        st.session_state.user_query = ""


def show_welcome_screen() -> None:
    """Affiche un écran de bienvenue dans l'application Streamlit pour les utilisateurs."""

    st.title("Bienvenue sur **SQL Trainer** 🐘")
    st.subheader(
        "Une plateforme interactive pour maîtriser SQL à travers des exercices pratiques."
    )


def get_available_themes(con: duckdb.DuckDBPyConnection) -> list[str]:
    """Récupère la liste des thèmes disponibles dans la base de données.

    :param con: Connexion active à la base de données.
    :returns: Liste des thèmes disponibles, ordonnée alphabétiquement.
    """
    available_themes = con.execute(
        "SELECT DISTINCT theme FROM exercises ORDER BY theme"
    ).fetchall()
    return [theme[0] for theme in available_themes]


def get_exercises_for_theme(con: duckdb.DuckDBPyConnection, theme: str) -> list[str]:
    """Récupère les exercices disponibles pour un thème spécifique.

    :param con: Connexion active à la base de données.
    :param theme: Nom du thème pour lequel récupérer les exercices.
    :returns: Liste des noms d'exercices pour le thème donné.
    """
    exercise_list = con.execute(
        "SELECT exercise_name FROM exercises WHERE theme = ? ORDER BY exercise_name",
        (theme,),
    ).fetchall()
    return [exercise[0] for exercise in exercise_list]


def main() -> None:
    """Fonction principale de l'application Streamlit pour initier
    la base de données et afficher les exercices SQL."""
    init_database("db.duckdb")  # Initialiser la base de données
    con = connect_db("db.duckdb")  # Connexion à la base de données # pylint: disable=unused-variable
    init_session_state()
    show_welcome_screen()


if __name__ == "__main__":
    main()
