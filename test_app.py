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

from init_db import check_data_directory_exists, load_csv_to_db


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
