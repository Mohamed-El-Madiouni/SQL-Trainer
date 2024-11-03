"""
Module principal de l'application SQL Trainer.

Ce fichier initialise la base de données,
charge les exercices et les solutions SQL, et fournit une interface
interactive avec Streamlit pour que les utilisateurs puissent pratiquer SQL.
"""

import logging
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


def show_welcome_screen(available_themes: list[str]) -> None:
    """Affiche un écran de bienvenue et une sélection de thème."""

    st.title("Bienvenue sur **SQL Trainer** 🐘")
    st.subheader(
        "Une plateforme interactive pour maîtriser SQL à travers des exercices pratiques."
    )
    st.selectbox(
        "Choisissez un thème pour commencer :",
        available_themes,
        index=None,  # Aucun thème sélectionné par défaut
        key="initial_theme_selection",
        placeholder="Choisissez un thème...",
        on_change=lambda: st.session_state.update(
            {"option": st.session_state.initial_theme_selection}
        ),
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


def load_exercise_data(
    con: duckdb.DuckDBPyConnection, theme: str, exercise_name: str
) -> dict | None:
    """Charge les données associées à un exercice spécifique.

    :param con: Connexion active à la base de données.
    :param theme: Nom du thème de l'exercice.
    :param exercise_name: Nom de l'exercice.
    :returns: Dictionnaire contenant les données de l'exercice, ou None si vide.
    """
    exercise_data = con.execute(
        "SELECT * FROM exercises WHERE theme = ? AND exercise_name = ?",
        (theme, exercise_name),
    ).fetchone()
    if exercise_data:
        # Conversion en dictionnaire pour faciliter l'accès aux données
        column_names = [desc[0] for desc in con.description]
        return dict(zip(column_names, exercise_data))
    return None


def load_question_and_solution(answer_name: str, question_name: str) -> tuple[str, str]:
    """Charge les fichiers de question et de solution pour un exercice donné.

    :param answer_name: Nom du fichier de la solution.
    :param question_name: Nom du fichier de la question.
    :returns: Contient le texte de la solution et le texte de la question.
    """
    try:
        with open(f"./answer/{answer_name}.sql", "r", encoding="UTF-8") as file:
            answer = file.read()
        with open(f"./questions/{question_name}.txt", "r", encoding="UTF-8") as file:
            question = file.read()
    except FileNotFoundError as exception:
        st.error(f"Erreur lors du chargement des fichiers : \n\n{exception}")
        logging.error("Erreur lors du chargement des fichiers : \n\n%s", exception)
        return "", ""
    return answer, question


def handle_sidebar(con: duckdb.DuckDBPyConnection, available_themes: list[str]) -> str:
    """Gère la sélection du thème et de l'exercice dans la barre latérale.

    :param con: Connexion active à la base de données.
    :param available_themes: Liste des thèmes disponibles.
    :returns: L'exercice sélectionné.
    """
    with st.sidebar:
        st.selectbox(
            "Changer de thème :",
            available_themes,
            index=(
                available_themes.index(st.session_state.option)
                if st.session_state.option in available_themes
                else 0
            ),
            key="sidebar_selected_theme",
            on_change=lambda: st.session_state.update(
                {"option": st.session_state.sidebar_selected_theme}
            ),
        )

        exercises = get_exercises_for_theme(con, st.session_state.option)
        current_exercise = st.selectbox(
            "Choisissez un exercice :",
            exercises,
            key="sidebar_selected_exercise",
            placeholder="Choisissez un exercice...",
        )

        st.session_state.exercise = current_exercise
    return current_exercise


def display_exercise_details(con: duckdb.DuckDBPyConnection) -> None:
    """Affiche les détails de l'exercice sélectionné dans l'interface.

    :param con: Connexion active à la base de données.
    """
    if st.session_state.exercise:
        exercise_data = load_exercise_data(
            con, st.session_state.option, st.session_state.exercise
        )

        if exercise_data:
            answer_name = exercise_data["exercise_name"]
            question_name = exercise_data["question"]
            #            sort_order = exercise_data["order"]

            exercise_answer, exercise_question = load_question_and_solution(
                answer_name, question_name
            )
            st.write("### Consigne de l'exercice sélectionné :")
            st.write(exercise_question)
            st.write("**Réponse attendue** :")
            st.code(exercise_answer, language="sql")
        else:
            st.error("Les données de l'exercice n'ont pas pu être chargées.")
            logging.error("Les données de l'exercice n'ont pas pu être chargées.")


def main() -> None:
    """Fonction principale de l'application Streamlit pour initier
    la base de données et afficher les exercices SQL."""
    init_database("db.duckdb")  # Initialiser la base de données
    con = connect_db("db.duckdb")  # Connexion à la base de données
    init_session_state()
    available_themes = get_available_themes(con)  # Récupérer les thèmes disponibles

    # Affichage conditionnel
    if not st.session_state.option:
        show_welcome_screen(
            available_themes
        )  # Afficher la page d'accueil si aucun thème n'est sélectionné
    else:
        handle_sidebar(
            con, available_themes
        )  # Afficher la barre latérale après sélection d'un thème
        display_exercise_details(con)  # Afficher les détails de l'exercice sélectionné


if __name__ == "__main__":
    main()
