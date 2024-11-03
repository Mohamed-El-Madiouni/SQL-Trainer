"""
Ce module initialise et gère la base de données DuckDB pour l'application.

Il comprend des fonctions pour charger les fichiers CSV, valider les données,
créer des tables nécessaires et surveiller la qualité des données via un système de logs.
"""

import logging
import os

import duckdb
import pandas as pd

# Création du dossier log si nécessaire
if not os.path.exists("log"):
    os.makedirs("log")

# Configuration du logger pour surveiller la qualité des données
logging.basicConfig(
    filename="./log/data_quality.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def check_data_directory_exists() -> None:
    """Vérifie l'existence du dossier de données et le crée s'il n'existe pas."""
    if not os.path.exists("data"):
        os.makedirs("data")


def generate_exercise_dataframe() -> pd.DataFrame:
    """Génère un DataFrame contenant les données pour la table des exercices.

    :returns: DataFrame contenant les thèmes, noms d'exercices, ordres et questions.
    """
    distinct_themes = [
        "1. Sélection Simple",
        "2. Joins",
        "3. Fonctions d’Agrégation",
        "4. Window Functions",
        "5. Sous-requêtes",
    ]
    theme_list = []
    exercise_names = []
    questions = []
    theme_number = 0
    for theme in distinct_themes:
        theme_number += 1
        for j in range(7):
            theme_list.append(theme)
            exercise_names.append(f"Exercice_{theme_number}.{j + 1}")
            questions.append(f"Exercice_{theme_number}.{j + 1}")

    orders = []
    # Lire chaque ligne du fichier et l'ajouter à la liste `orders`
    with open("./data/order.txt", "r", encoding="utf-8") as file:
        for line in file:
            orders.append(
                line.strip()
            )  # .strip() pour enlever les éventuels espaces et sauts de ligne

    return pd.DataFrame(
        {
            "theme": theme_list,
            "exercise_name": exercise_names,
            "order": orders,
            "question": questions,
        }
    )


def create_exercise_table_in_db(con: duckdb.DuckDBPyConnection) -> None:
    """Crée la table 'exercises' pour les exercices dans la base de données.

    :param con: Connexion active à la base de données DuckDB.
    """
    tab_df = generate_exercise_dataframe()  # pylint:disable=(unused-variable)
    try:
        con.execute("CREATE TABLE IF NOT EXISTS exercises AS SELECT * FROM tab_df")

    except duckdb.Error as e:
        print(f"Erreur lors de la création de la table 'tab': {e}")


def load_csv_to_db(
    con: duckdb.DuckDBPyConnection, file_path: str, table_name: str
) -> None:
    """Charge un fichier CSV dans une table DuckDB avec validation des données."""

    try:
        # Lecture du CSV avec Pandas
        df = pd.read_csv(file_path, sep=",")

        # Validation des données selon le fichier
        if file_path == "./data/department.csv":
            validate_department_columns(df, file_path)
        if file_path in ("./data/employees.csv", "./data/employees_test.csv"):
            validate_employee_columns(df, file_path)
            validate_salary_column(df, file_path)
            validate_age_column(df, file_path)

        # Insertion des données après validation
        con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")
        logging.info(
            "Table '%s' créée avec succès à partir du fichier %s", table_name, file_path
        )

    except FileNotFoundError as e:
        logging.error("Fichier non trouvé : %s", e)
    except pd.errors.EmptyDataError as e:
        logging.error("Fichier vide ou données incorrectes : %s", e)
    except pd.errors.ParserError as e:
        logging.error("Erreur de parsing dans %s : %s", file_path, e)
    except ValueError as e:
        logging.error("Erreur de validation des données pour %s : %s", file_path, e)
    except duckdb.Error as e:  # Gestion des erreurs DuckDB
        logging.error(
            "Erreur SQL dans la table %s pour %s : %s", table_name, file_path, e
        )


def validate_department_columns(df: pd.DataFrame, file_path: str) -> None:
    """Valide les colonnes et données du fichier department.csv.

    :param df: DataFrame contenant les données du fichier department.
    :param file_path: Chemin vers le fichier CSV pour les logs.
    :raises ValueError: Si des colonnes sont manquantes ou si des valeurs nulles sont détectées.
    """
    expected_columns = {"id", "department_name", "location"}
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        logging.warning("Colonnes manquantes dans %s: %s", file_path, missing_columns)
        raise ValueError(f"Colonnes manquantes dans {file_path}: {missing_columns}")

    if df.isnull().values.any():
        null_count = df.isnull().sum().sum()
        logging.warning(
            "Données manquantes détectées dans %s: %s valeurs nulles",
            file_path,
            null_count,
        )
        raise ValueError(
            f"Données manquantes dans {file_path}: {null_count} valeurs nulles"
        )


def validate_employee_columns(df: pd.DataFrame, file_path: str) -> None:
    """Valide les colonnes et données du fichier employees.csv.

    :param df: DataFrame contenant les données du fichier employees.
    :param file_path: Chemin vers le fichier CSV pour les logs.
    :raises ValueError: Si des colonnes sont manquantes ou si des valeurs nulles sont détectées.
    """
    expected_columns = {"id", "name", "age", "department", "salary"}
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        logging.warning("Colonnes manquantes dans %s: %s", file_path, missing_columns)
        raise ValueError(f"Colonnes manquantes dans {file_path}: {missing_columns}")

    if df.isnull().values.any():
        null_count = df.isnull().sum().sum()
        logging.warning(
            "Données manquantes détectées dans %s: %s valeurs nulles",
            file_path,
            null_count,
        )
        raise ValueError(
            f"Données manquantes dans {file_path}: {null_count} valeurs nulles"
        )


def validate_salary_column(df: pd.DataFrame, file_path: str) -> None:
    """Vérifie les valeurs extrêmes dans la colonne 'salary'.

    :param df: DataFrame contenant les données du fichier employees.
    :param file_path: Chemin vers le fichier CSV pour les logs.
    """
    if "salary" in df.columns:
        extreme_salaries = df[(df["salary"] < 10000) | (df["salary"] > 200000)]
        if not extreme_salaries.empty:
            logging.info("Valeurs extrêmes détectées dans 'salary' pour %s", file_path)
            logging.info(extreme_salaries)
            raise ValueError(
                f"Valeurs extrêmes détectées dans 'salary' pour {file_path}"
            )


def validate_age_column(df: pd.DataFrame, file_path: str) -> None:
    """Vérifie les valeurs extrêmes dans la colonne 'age'.

    :param df: DataFrame contenant les données du fichier employees.
    :param file_path: Chemin vers le fichier CSV pour les logs.
    """
    if "age" in df.columns:
        extreme_ages = df[(df["age"] < 18) | (df["age"] > 65)]
        if not extreme_ages.empty:
            logging.info("Valeurs extrêmes détectées dans 'age' pour %s", file_path)
            logging.info(extreme_ages)


def process_csv_files(con: duckdb.DuckDBPyConnection, csv_folder: str) -> None:
    """Parcourt tous les fichiers CSV d'un dossier et les charge dans la base de données.

    :param con: Connexion active à la base de données DuckDB.
    :param csv_folder: Chemin vers le dossier contenant les fichiers CSV.
    """
    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith(".csv"):
            table_name = os.path.splitext(csv_file)[0]
            file_path = os.path.join(csv_folder, csv_file)
            load_csv_to_db(con, file_path, table_name)


def initialize_database_tables(con: duckdb.DuckDBPyConnection) -> None:
    """Crée toutes les tables nécessaires dans la base de données,
    y compris les exercices et les données.

    :param con: Connexion active à la base de données DuckDB.
    """
    csv_directory = "./data"
    check_data_directory_exists()  # Vérifier l'existence du dossier de données
    process_csv_files(con, csv_directory)
    create_exercise_table_in_db(con)
