 # Projet 4 python openclassrooms

Ce script permet de générer un tournoi d'échec selon le système de tournoi Suisse.
Il suit le design pattern MVC (Modèle Vue Controller), la librairie TinyDB est utilisée afin de sauvegarder 
les informations des joueurs / résultats de matchs / tournois

La version de **Python** à utiliser : _**3.10.5**_

# **ENVIRONNEMENT VIRTUEL**

Création de l'environnement virtuel :


Pour créer l'environnement virtuel il faut exécuter la commande suivante à la racine du projet :

    python -m venv env


Puis la commande suivante pour démarrer l'environnement :

-   sous Linux

    
    source env/bin/activate

-   sous Windows


    env/Scripts/activate.bat


Pour installer les packages spécifiés dans le fichier requirements.txt il faut exécuter la commande suivante :

    pip install -r requirements.txt

# **FLAKE8**

Le code suit les normes de codage de la PEP8, un rapport peut être généré via flake8 avec la commande :

    flake8

Le fichier de configuration est ".flake8" à la racine du projet

Le rapport sera généré dans le répertoire "flake8_rapport".

# **SCRIPT**

Lors de l'exécution du script via la commande

    python main.py

Il y aura un menu dans la console, qui permettra de choisir 
ce que l'on souhaite effectuer

Il y a plusieurs possibilités :

    Veuillez choisir un action :  
     1 : Créer un nouveau joueur
     2 : Mettre à jour le classement d'un joueur
     3 : Créer un tournoi
     4 : Reprendre un tournoi en cour
     5 : Consulter l'historique des tournois
     0 : Quitter

Il suffit d'écrire 1, 2, 3, 4, 5 ou 0

Le choix 1 permet de créer un joueur, en saisissant les différentes informations demandées : nom, 
prénom, date de naissance, civilité, classement.

Le choix 2 permet de rechercher un joueur soit par son nom, soit par son classement afin de mettre à jour celui ci

Le choix 3 permet de créer un nouveau tournoi et de générer les matchs selon le modèle de tournoi suisse, 
apres avoir sélectionné / créé les différents joueurs participants au tournoi

Le choix 4 permet de reprendre le cours d'un tournoi qui n'est pas terminé

Le choix 5 permet de consulter les scores des tournois qui sont terminés

Le choix 0 permet de quitter le programme