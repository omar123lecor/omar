#!/usr/bin/env python3
import argparse
import os
import json
from status import check_login_status
from datetime import datetime

LOG_PATH = "/home/abderrahmane/ID1FS/log"
LOG_FILE_NAME = "execution_log.txt"

base_path = '/home/abderrahmane/ID1FS/home'  # Chemin de base
metadata_path = '/home/abderrahmane/ID1FS/metadata/metadata.json'  # Chemin du fichier JSON de métadonnées

def format_timestamp(timestamp):
    # Formater le timestamp en une chaîne de date lisible
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def add_metadata(filename):
    # Charger les métadonnées existantes depuis le fichier JSON
    metadata = {}
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as metadata_file:
            try:
                metadata = json.load(metadata_file)
            except json.decoder.JSONDecodeError:
                print("Le fichier de métadonnées est vide or mal formaté. Il sera créé à nouveau.")

    # Chemin complet du fichier
    full_path = os.path.join(base_path, filename)

    # Récupérer les informations sur le fichier
    stat_info = os.stat(full_path)

    # Ajouter les métadonnées pour le fichier
    metadata[filename] = {
        'path': full_path,
        'created_at': format_timestamp(stat_info.st_ctime),
        'last_modified_at': format_timestamp(stat_info.st_mtime),
        'size': stat_info.st_size,
        'permissions': oct(stat_info.st_mode & 0o777),  # Convertir en octal
        'owner': stat_info.st_uid,
        'group': stat_info.st_gid
    }

    # Enregistrer les métadonnées mises à jour dans le fichier JSON
    with open(metadata_path, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=2)

    print(f"Métadonnées ajoutées pour '{full_path}'.")
    log_execution("Metadata", f"Metadata added for '{full_path}'.")

def create_file(filename):
    # Chemin complet du fichier à créer
    full_path = os.path.join(base_path, filename)

    # Vérifier si le fichier existe déjà
    if not os.path.exists(full_path):
        # Créer un nouveau fichier
        with open(full_path, 'w') as file:
            file.write("Contenu du fichier créé\n")
        print(f"Fichier '{full_path}' créé avec succès.")

        # Ajouter les métadonnées pour le fichier
        add_metadata(filename)
        log_execution("File Creation", f"File created: '{full_path}'")
    else:
        print(f"Erreur : Le fichier '{full_path}' existe déjà.")
        log_execution("File Creation Error", f"File creation failed: '{full_path}' already exists.")

def create_directory(dirname):
    # Chemin complet du répertoire à créer
    full_path = os.path.join(base_path, dirname)

    # Vérifier si le répertoire existe déjà
    if not os.path.exists(full_path):
        # Créer un nouveau répertoire
        os.makedirs(full_path)
        print(f"Répertoire '{full_path}' créé avec succès.")

        # Ajouter les métadonnées pour le répertoire
        add_metadata(dirname)
        log_execution("Directory Creation", f"Directory created: '{full_path}'")
    else:
        print(f"Erreur : Le répertoire '{full_path}' existe déjà.")
        log_execution("Directory Creation Error", f"Directory creation failed: '{full_path}' already exists.")

def log_execution(action, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")  # Add a separator for better readability between log entries

def main():
    # Vérifiez le statut avant d'exécuter le script
    if not check_login_status():
        print("Le statut de connexion est désactivé. Veuillez activer le système.")
        log_execution("Error", "Script execution failed: Login status is inactive.")
        return

    parser = argparse.ArgumentParser(description="Commande pour créer des fichiers et des dossiers")

    # Ajouter des options pour créer un fichier (-f) et un dossier (-d)
    parser.add_argument('-f', '--create-file', metavar='FILENAME', help='Créer un fichier')
    parser.add_argument('-d', '--create-dir', metavar='DIRNAME', help='Créer un dossier')

    args = parser.parse_args()

    if args.create_file:
        create_file(args.create_file)
    elif args.create_dir:
        create_directory(args.create_dir)
    else:
        parser.print_help()
        log_execution("Error", "No operation specified.")

if __name__ == "__main__":
    main()



