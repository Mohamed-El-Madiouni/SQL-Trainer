"""
Module de tests unitaires pour l'application SQL Trainer.

Ce fichier contient des tests pour les fonctions d'interaction avec la base de données,
ainsi que pour la validation des données chargées depuis des fichiers CSV.
Les tests sont réalisés en utilisant unittest.
"""

import os
import unittest

import duckdb
import pandas as pd

# isort: off
from app import (
    compare_results,
    connect_db,
    execute_user_query,
    get_available_themes,
    get_exercises_for_theme,
    init_database,
    load_exercise_data,
    load_question_and_solution,
)

# isort: on
from init_db import check_data_directory_exists, load_csv_to_db


class TestDatabaseFunctions(unittest.TestCase):
    """Tests pour les fonctions qui interagissent avec la base de données."""

    @classmethod
    def setUpClass(cls) -> None:
        """Configure une base de données temporaire pour les tests."""
        cls.db_name: str = "test_db.duckdb"
        init_database(cls.db_name)
        cls.con: duckdb.DuckDBPyConnection = connect_db(cls.db_name)

    @classmethod
    def tearDownClass(cls) -> None:
        """Nettoie en fermant la base de données et en supprimant le fichier de test."""
        cls.con.close()
        # Supprime le fichier de base de données pour garantir un environnement de test propre
        if os.path.exists(cls.db_name):
            os.remove(cls.db_name)

    def test_init_database(self) -> None:
        """Vérifie si la base de données et le dossier sont correctement initialisés."""
        init_database(self.db_name)
        self.assertTrue(os.path.exists("data"), "Le dossier data doit exister.")
        self.assertTrue(
            os.path.exists(f"data/{self.db_name}"),
            "Le fichier de base de données doit être créé.",
        )

    def test_connect_db(self) -> None:
        """Vérifie si la connexion à la base de données est réussie."""
        con: duckdb.DuckDBPyConnection = connect_db(self.db_name)
        self.assertIsInstance(
            con,
            duckdb.DuckDBPyConnection,
            "Doit retourner une instance de connexion DuckDB.",
        )
        con.close()

    def test_get_available_themes(self) -> None:
        """Test de récupération des thèmes uniques dans la base de données."""
        themes: list[str] = get_available_themes(self.con)
        self.assertIsInstance(
            themes, list, "Les thèmes doivent être retournés sous forme de liste."
        )
        self.assertGreater(len(themes), 0, "La liste des thèmes ne doit pas être vide.")

    def test_get_exercises_for_theme(self) -> None:
        """Test de récupération des exercices pour un thème donné."""
        theme: str = "SQL Basics"
        exercises: list[str] = get_exercises_for_theme(self.con, theme)
        self.assertIsInstance(
            exercises, list, "Les exercices doivent être retournés sous forme de liste."
        )

    def test_load_exercise_data(self) -> None:
        """Test de chargement des données pour un exercice spécifique."""
        theme: str = "1. Sélection Simple"
        exercise_name: str = "Exercice_1.1"
        data = load_exercise_data(self.con, theme, exercise_name)
        self.assertEqual(data["order"], "id", "Erreur dans le tri par 'order'")
        self.assertEqual(data["question"], "Exercice_1.1", "Erreur dans la question")
        self.assertIsInstance(
            data,
            dict,
            "Les données de l'exercice doivent être un dictionnaire.",
        )

    def test_load_question_and_solution(self) -> None:
        """Test de chargement des fichiers de question et de solution."""
        answer: str
        question: str
        answer, question = load_question_and_solution("Exercice_1.1", "Exercice_1.1")
        self.assertIsInstance(
            answer, str, "La réponse doit être retournée sous forme de chaîne."
        )
        self.assertIsInstance(
            question, str, "La question doit être retournée sous forme de chaîne."
        )

    def test_execute_user_query(self) -> None:
        """Test d'exécution d'une requête SQL définie par l'utilisateur."""
        query: str = "SELECT 1 AS test_col"
        result_df: pd.DataFrame
        success: bool
        result_df, success = execute_user_query(self.con, query, "test_col")
        self.assertTrue(success, "La requête doit s'exécuter avec succès.")
        self.assertEqual(
            result_df.iloc[0]["test_col"],
            1,
            "La requête doit retourner le résultat correct.",
        )

    def test_compare_results(self) -> None:
        """Test de comparaison entre la requête utilisateur et la solution."""
        solution_df: pd.DataFrame = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        user_df: pd.DataFrame = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        message = compare_results(solution_df, user_df)
        self.assertTrue(
            "Félicitations" in message,
            "Un message de victoire doit s'afficher lorsque les résultats correspondent.",
        )


class TestInitDBFunctions(unittest.TestCase):
    """Tests pour les fonctions relatives à l'initialisation de la base de données."""

    @classmethod
    def setUpClass(cls) -> None:
        """Configure une connexion de base de données temporaire pour les tests."""
        cls.db_path: str = "./data/test_db.duckdb"
        cls.con: duckdb.DuckDBPyConnection = duckdb.connect(cls.db_path)

    @classmethod
    def tearDownClass(cls) -> None:
        """Nettoie en fermant la base de données et en supprimant le fichier de test."""
        cls.con.close()
        # Supprime le fichier de base de données pour garantir un environnement de test propre
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)

    def test_check_data_folder_exists(self) -> None:
        """Vérifie l'existence du dossier data."""
        # Crée le dossier si inexistant pour éviter les erreurs
        check_data_directory_exists()
        self.assertTrue(os.path.exists("data"), "Le dossier data doit exister.")

    def test_load_csv_to_db(self) -> None:
        """Test du chargement d'un fichier CSV dans la base de données."""
        csv_path: str = "data/sample.csv"
        pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]}).to_csv(
            csv_path, index=False, sep=";"
        )
        table_name: str = "test_table"
        load_csv_to_db(self.con, csv_path, table_name)
        result = self.con.execute(f"SELECT * FROM {table_name}").fetchdf()
        self.assertEqual(len(result), 3, "La table doit contenir 3 lignes.")

        # Supprime le fichier CSV de test pour garder un environnement propre
        os.remove(csv_path)

    def test_load_csv_with_validation(self) -> None:
        """Teste le chargement de données CSV avec validation de schéma et valeurs."""
        csv_path = "./data/employees_test.csv"
        df = pd.DataFrame(
            {
                "id": [1, 2],
                "name": ["Fabrice", "Karima"],
                "age": [29, 34],
                "department": [2, 1],
                "salary": [60000, 49000],
            }
        )
        df.to_csv(csv_path, index=False, sep=",")

        # Test de chargement avec validation
        load_csv_to_db(self.con, csv_path, "employees_test")
        loaded_data = self.con.execute("SELECT * FROM employees_test").fetchdf()

        # Validation des colonnes et du contenu
        self.assertEqual(
            list(loaded_data.columns), ["id", "name", "age", "department", "salary"]
        )
        self.assertFalse(loaded_data.isnull().values.any())

        os.remove(csv_path)


if __name__ == "__main__":
    unittest.main()
