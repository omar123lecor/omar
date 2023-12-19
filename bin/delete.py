#!/usr/bin/python3
import argparse
import os
import shutil
import json
from status import check_login_status
from datetime import datetime

BASE_PATH = "/home/abderrahmane/ID1FS/home"
METADATA_PATH = "/home/abderrahmane/ID1FS/metadata/metadata.json"
BACKUP_PATH = "/home/abderrahmane/ID1FS/backup"

LOG_PATH = "/home/abderrahmane/ID1FS/log"
LOG_FILE_NAME = "execution_log.txt"


def get_full_path(filename):
    # Construire le chemin complet en ajoutant le chemin de base
    return os.path.join(BASE_PATH, filename)


def create_backup(filename):
    # Créer le dossier de sauvegarde s'il n'existe pas déjà
    if not os.path.exists(BACKUP_PATH):
        os.makedirs(BACKUP_PATH)

    source_path = get_full_path(filename)
    backup_path = os.path.join(BACKUP_PATH, f"{filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    # Copier le fichier vers le dossier de sauvegarde
    shutil.copy2(source_path, backup_path)
    log_execution("Backup", f"File '{filename}' backed up to '{backup_path}'.")


def log_execution(action, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")  # Add a separator for better readability between log entries


def delete_file(filename):
    full_path = get_full_path(filename)

    try:
        # Sauvegarder le fichier avant de le supprimer
        create_backup(filename)

        # Supprimer le fichier
        os.remove(full_path)
        log_execution("File Deletion", f"File '{full_path}' deleted successfully.")
        print(f"File '{full_path}' deleted successfully.")
    except Exception as e:
        log_execution("File Deletion Error", f"Error deleting file '{full_path}': {str(e)}")
        print(f"Error deleting file '{full_path}': {str(e)}")


def delete_directory(dirname):
    full_path = get_full_path(dirname)

    try:
        # Sauvegarder le répertoire avant de le supprimer
        create_backup(dirname)

        # Supprimer le répertoire
        shutil.rmtree(full_path)
        log_execution("Directory Deletion", f"Directory '{full_path}' deleted successfully.")
        print(f"Directory '{full_path}' deleted successfully.")
    except Exception as e:
        log_execution("Directory Deletion Error", f"Error deleting directory '{full_path}': {str(e)}")
        print(f"Error deleting directory '{full_path}': {str(e)}")


def remove_metadata(filename):
    # Charger les métadonnées existantes depuis le fichier JSON
    metadata = {}
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r') as metadata_file:
            metadata = json.load(metadata_file)

    # Supprimer les métadonnées associées au fichier
    if filename in metadata:
        del metadata[filename]

        # Enregistrer les métadonnées mises à jour dans le fichier JSON
        with open(METADATA_PATH, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=2)


def main():
    # Vérifier le statut avant d'exécuter le script principal
    if not check_login_status():
        log_execution("Error", "Script execution failed: Login status is inactive.")
        return

    parser = argparse.ArgumentParser(description="Commande pour supprimer des fichiers et des dossiers")

    try:
        # Ajouter des options pour supprimer un fichier (-f) et un dossier (-d)
        parser.add_argument('-f', '--delete-file', metavar='FILENAME', help='Supprimer un fichier')
        parser.add_argument('-d', '--delete-dir', metavar='DIRNAME', help='Supprimer un dossier')

        args = parser.parse_args()

        if args.delete_file:
            delete_file(args.delete_file)
        elif args.delete_dir:
            delete_directory(args.delete_dir)
        else:
            log_execution("Error", "Script execution failed: Missing options or filename.")
            parser.print_help()

    except argparse.ArgumentError as e:
        log_execution("Error", f"Script execution failed: {str(e)}")
        parser.print_help()


if __name__ == "__main__":
    main()



