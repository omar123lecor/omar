#!/usr/bin/env python3
import os
import argparse
from datetime import datetime
from status import check_login_status
LOG_PATH = "/home/abderrahmane/ID1FS/log"
LOG_FILE_NAME = "execution_log.txt"


def log_execution(action, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")  # Ajouter un séparateur pour une meilleure lisibilité entre les entrées de journal


# Vérifiez le statut avant d'exécuter le script principal
if check_login_status():
    # Configuration de l'analyseur d'arguments
    parser = argparse.ArgumentParser(description="Liste le contenu du répertoire courant avec différentes options.")
    parser.add_argument('-f', '--fichiers', action='store_true', help='Afficher uniquement les fichiers')
    parser.add_argument('-d', '--repertoires', action='store_true', help='Afficher uniquement les répertoires')
    parser.add_argument('-a', '--caches', action='store_true', help='Afficher les fichiers cachés')
    parser.add_argument('-l', '--long', action='store_true', help='Afficher les détails des fichiers')
    parser.add_argument('-n', '--nombre', action='store_true', help='Calculer le nombre de fichiers dans le répertoire')

    # Analyse des arguments de la ligne de commande
    args = parser.parse_args()

    # Liste les fichiers dans le répertoire courant
    liste_fichiers = os.listdir()

    # Filtrer les fichiers et répertoires selon les options
    if args.fichiers:
        liste_fichiers = [fichier for fichier in liste_fichiers if os.path.isfile(fichier)]
        print("Contenu du répertoire courant (fichiers seulement):")
        log_execution("List Files", "Listing files in the current directory.")
        for fichier in liste_fichiers:
            print(fichier)
    elif args.repertoires:
        liste_fichiers = [fichier for fichier in liste_fichiers if os.path.isdir(fichier)]
        print("les répertoires existants :")
        log_execution("List Directories", "Listing directories in the current directory.")
        for fichier in liste_fichiers:
            print(fichier)
    elif args.caches:
        liste_fichiers = [fichier for fichier in liste_fichiers if fichier.startswith('.')]
        print("Contenu du répertoire courant (fichiers cachés):")
        log_execution("List Hidden Files", "Listing hidden files in the current directory.")
        for fichier in liste_fichiers:
            print(fichier)
    elif args.long:
        print("Contenu du répertoire courant (détails des fichiers):")
        log_execution("List File Details", "Listing file details in the current directory.")
        for fichier in liste_fichiers:
            stat_info = os.stat(fichier)
            date_modification = datetime.utcfromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            type_fichier = 'd' if os.path.isdir(fichier) else '-'
            print(f"{type_fichier}{os.stat(fichier).st_mode:04o} {stat_info.st_nlink} {stat_info.st_uid} {stat_info.st_gid} {stat_info.st_size} {date_modification} {fichier}")
    elif args.nombre:
        print(f"Nombre total de fichiers dans le répertoire courant: {len(liste_fichiers)}")
        log_execution("Count Files", "Counting total files in the current directory.")
    else:
        print("Contenu du répertoire courant:")
        log_execution("List All", "Listing all files in the current directory.")
        for fichier in liste_fichiers:
            print(fichier)
else:
    print("Le statut de connexion est désactivé. Veuillez activer le système.")
    log_execution("Error", "Connection status is off. Please login first.")

