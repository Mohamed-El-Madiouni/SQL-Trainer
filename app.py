"""
Module principal de l'application SQL Trainer.

Ce fichier initialise la base de données,
charge les exercices et les solutions SQL, et fournit une interface
interactive avec Streamlit pour que les utilisateurs puissent pratiquer SQL.
"""

import duckdb


def connect_db(name: str) -> duckdb.DuckDBPyConnection:
    """Connecte à la base de données DuckDB.

    :param name: Nom du fichier de base de données.
    :returns: Objet de connexion à la base de données.
    """
    return duckdb.connect(database=f"./data/{name}", read_only=False)
