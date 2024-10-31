"""
Ce module initialise et gère la base de données DuckDB pour l'application.

Il comprend des fonctions pour charger les fichiers CSV, valider les données,
créer des tables nécessaires et surveiller la qualité des données via un système de logs.
"""

import os

import duckdb
import pandas as pd


def create_exercise_table_in_db(con: duckdb.DuckDBPyConnection) -> None:
    """Crée la table 'exercises' pour les exercices dans la base de données.

    :param con: Connexion active à la base de données DuckDB.
    """
    # Exemples de données pour les thèmes, exercices, questions et réponses
    data = {
        "theme": ["SQL Basics", "Joins", "Aggregation"],
        "exercise_name": ["Exercice 1", "Exercice 2", "Exercice 3"],
        "question": [
            "Sélectionnez tous les employés.",
            "Affichez les employés avec leur département.",
            "Calculez le salaire moyen par département.",
        ],
        "answer": [
            "SELECT * FROM employees;",
            "SELECT employees.name, department.department_name FROM employees JOIN "
            "department ON employees.department = department.id;",
            "SELECT department, AVG(salary) FROM employees GROUP BY department;",
        ],
    }
    exercises_df = pd.DataFrame(data)  # pylint: disable=unused-variable

    # Créer la table 'exercises' avec les données d'exemple
    con.execute("CREATE TABLE IF NOT EXISTS exercises AS SELECT * FROM exercises_df")


def load_csv_to_db(
    con: duckdb.DuckDBPyConnection, file_path: str, table_name: str
) -> None:
    """Charge un fichier CSV dans une table DuckDB.

    :param con: Connexion active à la base de données.
    :param file_path: Chemin vers le fichier CSV.
    :param table_name: Nom de la table dans la base de données.
    """
    df = pd.read_csv(file_path)  # pylint: disable=unused-variable
    con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")


def create_data_tables_in_db(con: duckdb.DuckDBPyConnection) -> None:
    """Crée les tables de données nécessaires en chargeant les fichiers CSV.

    :param con: Connexion active à la base de données DuckDB.
    """
    if os.path.exists("data/employees.csv"):
        load_csv_to_db(con, "data/employees.csv", "employees")
    if os.path.exists("data/department.csv"):
        load_csv_to_db(con, "data/department.csv", "department")


def initialize_database_tables(con: duckdb.DuckDBPyConnection) -> None:
    """Crée toutes les tables nécessaires dans la base de données,
    y compris les exercices et les données.

    :param con: Connexion active à la base de données DuckDB.
    """
    create_exercise_table_in_db(con)
    create_data_tables_in_db(
        con
    )  # Charger les tables de données depuis les fichiers CSV
