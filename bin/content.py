#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime

LOG_PATH = "/home/abderrahmane/ID1FS/log"
LOG_FILE_NAME = "execution_log.txt"


def check_login_status():
    file_path = "/home/abderrahmane/ID1FS/bin/login_status.json"
    try:
        with open(file_path, "r") as status_file:
            status_data = json.load(status_file)
            return status_data["status"]
    except FileNotFoundError:
        return False


def display_file_content(filename, options):
    if check_login_status():
        target_directory = "/home/abderrahmane/ID1FS/home"

        # Vérifie si le fichier se trouve dans le répertoire cible
        if os.path.abspath(filename).startswith(os.path.abspath(target_directory)):
            try:
                with open(filename, "r") as file:
                    content = file.read()

                    if options.a:
                        # Afficher les lignes numérotées
                        content = [f"{i+1}: {line}" for i, line in enumerate(content.splitlines())]
                        content = "\n".join(content)
                        print(f"File content:\n{content}")
                    elif options.b:
                        # Afficher le nombre de lignes
                        line_count = len(content.splitlines())
                        print(f"Number of lines in '{filename}': {line_count}")
                    elif options.r:
                        # Afficher le nombre de caractères
                        char_count = len(content)
                        print(f"Number of characters in '{filename}': {char_count}")
                    else:
                        print(f"File content:\n{content}")

                    # Ajouter une entrée de journal pour l'affichage du contenu du fichier
                    log_execution("Display Content", f"Content of file '{filename}' displayed.")
            except FileNotFoundError:
                # Ajouter une entrée de journal pour l'erreur de fichier non trouvé
                log_execution("Error", f"File '{filename}' not found.")
                print(f"Error: File '{filename}' not found.")
        else:
            # Ajouter une entrée de journal pour l'erreur de fichier non autorisé
            log_execution("Error", f"File '{filename}' is not allowed. It must be in the directory '{target_directory}'.")
            print(f"Error: File '{filename}' is not allowed. It must be in the directory '{target_directory}'.")
    else:
        # Ajouter une entrée de journal pour l'erreur d'état de connexion désactivé
        log_execution("Error", "Connection status is off. Please login first.")
        print("Error: Connection status is off. Please login first.")


def log_execution(action, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")  # Ajouter un séparateur pour une meilleure lisibilité entre les entrées de journal


def main():
    parser = argparse.ArgumentParser(description="Display file content with specific options if connection status is on")
    parser.add_argument("filename", help="Name of the file to display")
    parser.add_argument("-a", action="store_true", help="Display lines with line numbers")
    parser.add_argument("-b", action="store_true", help="Display the number of lines in the file")
    parser.add_argument("-r", action="store_true", help="Display the number of characters in the file")

    args = parser.parse_args()
    display_file_content(args.filename, args)


if __name__ == "__main__":
    main()

