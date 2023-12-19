#!/usr/bin/env python3

import argparse
import os  # Ajout de cette ligne
from status import check_login_status
from datetime import datetime

LOG_PATH = "/home/abderrahmane/ID1FS/log"
LOG_FILE_NAME = "execution_log.txt"

def log_command(command, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Command: {command}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")  # Ajout d'un séparateur pour une meilleure lisibilité entre les entrées de journal

def count_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return len(lines)

def main():
    # Vérifiez le statut avant d'exécuter le script
    if not check_login_status():
        print("Le statut de connexion est désactivé. Veuillez activer le système.")
        return

    # Configuration de l'analyseur d'arguments
    parser = argparse.ArgumentParser(description="Compte le nombre de lignes dans un fichier.")
    parser.add_argument('fichier', metavar='FICHIER', type=str, help='Le chemin vers le fichier à analyser')
    parser.add_argument('-c', '--caracteres', action='store_true', help='Compter le nombre de caractères au lieu de lignes')
    parser.add_argument('-w', '--mots', action='store_true', help='Compter le nombre de mots au lieu de lignes')
    parser.add_argument('-l', '--lignes', action='store_true', help='Compter le nombre de lignes (par défaut)')

    # Analyse des arguments de la ligne de commande
    args = parser.parse_args()

    # Enregistrez la commande dans le log
    log_command("count_lines", f"File: {args.fichier}, Characters: {args.caracteres}, Words: {args.mots}, Lines: {args.lignes}")

    if args.caracteres:
        with open(args.fichier, 'r') as file:
            content = file.read()
            count = len(content)
            print(f"Nombre de caractères dans {args.fichier}: {count}")
    elif args.mots:
        with open(args.fichier, 'r') as file:
            content = file.read()
            words = content.split()
            count = len(words)
            print(f"Nombre de mots dans {args.fichier}: {count}")
    else:
        # Par défaut, ou si -l est spécifié, compter le nombre de lignes
        count = count_lines(args.fichier)
        print(f"Nombre de lignes dans {args.fichier}: {count}")

if __name__ == "__main__":
    main()


