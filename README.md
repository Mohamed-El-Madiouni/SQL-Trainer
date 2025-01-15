# SQL Trainer

Découvrez le projet ici : [Lien vers l'application](https://sql-training-25664b6fb456.herokuapp.com)

## Table des Matières


1. [Introduction](#introduction)
2. [Fonctionnalités](#fonctionnalités)
3. [Installation](#installation)
   - [Prérequis](#prérequis)
   - [Étapes d'installation](#étapes-dinstallation)
4. [Structure du Projet](#structure-du-projet)
5. [Architecture et Choix Techniques](#architecture-et-choix-techniques)
6. [Utilisation](#utilisation)
   - [Lancer l'application](#lancer-lapplication)
   - [Sélection d'un exercice](#sélection-dun-exercice)
   - [Résoudre un exercice](#résoudre-un-exercice)
   - [Visualisation des tables](#visualisation-des-tables)
   - [Accéder à la solution](#accéder-à-la-solution)
7. [Tests](#tests)
   - [Exécution des tests](#exécution-des-tests)
   - [Fonctionnalités testées](#fonctionnalités-testées)
8. [Conclusion](#conclusion)

---

## Introduction

SQL Trainer est une plateforme interactive conçue pour aider les utilisateurs à pratiquer et maîtriser les requêtes SQL. Ce projet a été réalisé pour démontrer des compétences clés en ingénierie de données, notamment :

- Gestion de bases de données avec **DuckDB**.
- Développement d'une interface utilisateur interactive avec **Streamlit**.
- Validation et transformation des données en Python.
- Déploiement CI/CD avec **GitHub Actions** et **Heroku**.

Il combine des aspects pédagogiques et techniques pour offrir une solution complète d'apprentissage SQL, tout en illustrant des pratiques essentielles de data engineering.

---

## Fonctionnalités

- Interface interactive avec **Streamlit** pour pratiquer SQL en temps réel.
- Exercices progressifs couvrant :
  - La sélection simple.
  - Les jointures.
  - Les fonctions d’agrégation.
  - Les fonctions de fenêtres (window functions).
  - Les sous-requêtes.
- Vérification automatique des réponses avec des messages d'erreur détaillés.
- Visualisation des tables utilisées pour chaque exercice.
- Déploiement facile sur **Heroku** avec CI/CD intégré via **GitHub Actions**.

---

## Installation

Suivez les étapes ci-dessous pour configurer et exécuter le projet localement.

### Prérequis

- **Python 3.10 ou version ultérieure** : Assurez-vous d'avoir Python installé sur votre machine.
- **pip** : Pour gérer les dépendances Python.
- **Heroku CLI** (facultatif) : Si vous souhaitez déployer l'application sur Heroku.

### Étapes d'installation

1. Clonez le dépôt :
   ```bash
   git clone git@github.com:Mohamed-El-Madiouni/SQL-Trainer.git
   cd SQL-Trainer
   ```

2. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Initialisez la base de données :
   ```bash
   python init_db.py
   ```

5. Lancez l'application Streamlit :
   ```bash
   streamlit run app.py
   ```

L'application sera disponible dans votre navigateur à l'adresse suivante : [http://localhost:8501](http://localhost:8501).

---

## Structure du Projet

Voici une présentation de l'arborescence du projet et des fichiers principaux :

```plaintext
|----SQL-Trainer/
|--------.github/
|------------workflows/
|----------------build_and_deploy.yaml   # Configuration du workflow CI/CD
|--------answer/
|------------Exercice_X.X.sql           # Solutions SQL pour les exercices
|--------data/
|------------db.duckdb                  # Base de données DuckDB
|------------department.csv             # Données des départements
|------------employees.csv              # Données des employés
|------------order.txt                  # Ordre des colonnes pour les exercices
|--------log/
|------------data_quality.log           # Logs de qualité des données
|--------questions/
|------------Exercice_X.X.txt           # Énoncés des exercices
|--------.gitignore                     # Fichiers et dossiers à ignorer par Git
|--------app.py                         # Fichier principal de l'application
|--------init_db.py                     # Initialisation de la base de données
|--------Procfile                       # Configuration de déploiement Heroku
|--------requirements.txt               # Dépendances Python
|--------test_app.py                    # Tests unitaires pour l'application
```

Chaque dossier et fichier a une fonction précise pour assurer le bon fonctionnement de l'application, depuis les exercices jusqu'à la gestion des données.

---

## Architecture et Choix Techniques

Ce projet utilise une architecture modulaire et légère qui met en avant des technologies modernes de gestion de données et de développement :

- **DuckDB** : Une base de données légère et performante, parfaite pour des cas d'usage comme l'exécution locale de requêtes SQL.
- **Streamlit** : Une plateforme rapide pour créer des applications web interactives et explorer les résultats en temps réel.
- **Python** : Utilisé pour gérer la validation des données, l'initialisation de la base et la logique métier.
- **CI/CD avec GitHub Actions** : Automatisation des tests unitaires et du déploiement continu.
- **Heroku** : Déploiement facile pour permettre un accès en ligne à l'application.

Ces choix techniques reflètent une approche professionnelle orientée vers la simplicité, la scalabilité et la maintenabilité.

---

## Utilisation

### Lancer l'application

1. Après avoir démarré l'application Streamlit comme décrit dans la section "Installation", ouvrez votre navigateur et accédez à l'adresse [http://localhost:8501](http://localhost:8501).
2. Une page d'accueil s'affiche, vous invitant à sélectionner un thème parmi ceux disponibles.

### Sélection d'un exercice

1. Choisissez un thème dans le menu déroulant (par exemple, "1. Sélection Simple").
2. Une fois le thème sélectionné, choisissez un exercice dans la barre latérale.

### Résoudre un exercice

1. Lisez l'énoncé de l'exercice affiché dans l'onglet **Exercice**.
2. Saisissez votre requête SQL dans le champ prévu à cet effet.
3. Cliquez sur le bouton **Exécuter** pour voir les résultats de votre requête.
4. Comparez vos résultats à ceux attendus :
   - Si votre requête est correcte, un message de félicitations s'affiche.
   - Sinon, des messages d'erreur ou des indices vous sont fournis pour corriger votre requête.

### Visualisation des tables

Les tables nécessaires pour résoudre chaque exercice sont affichées dans l'interface. Vous pouvez explorer les premières lignes des données pour mieux comprendre leur structure.

### Accéder à la solution

Si vous êtes bloqué, un onglet **Solution** est disponible pour consulter la réponse correcte.

---

## Tests

SQL Trainer est livré avec une suite de tests unitaires pour vérifier la fiabilité de ses fonctionnalités.

### Exécution des tests

1. Assurez-vous d'avoir installé toutes les dépendances, y compris celles nécessaires aux tests.
   ```bash
   pip install -r requirements.txt
   ```

2. Lancez les tests avec la commande suivante :
   ```bash
   python -m unittest discover
   ```

### Fonctionnalités testées

- Initialisation et connexion à la base de données.
- Chargement et validation des fichiers CSV.
- Gestion des thèmes et exercices.
- Comparaison des résultats entre la solution correcte et la requête utilisateur.
- Exécution des requêtes SQL définies par l'utilisateur.

Ces tests permettent de s'assurer que l'application fonctionne correctement et que les données des exercices sont valides.

---

## Conclusion

SQL Trainer est un outil pour apprendre et pratiquer SQL de manière interactive. Ce projet reflète mes compétences en ingénierie de données, notamment en gestion de pipelines SQL, validation des données, et création d'environnements d'apprentissage interactifs.

N'hésitez pas à explorer le projet, à résoudre les exercices et à perfectionner vos compétences SQL. Bonne pratique et amusez-vous bien ! 
