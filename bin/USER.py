#!/usr/bin/env python3
import getpass
import crypt
import json
import argparse
import os
import subprocess

USERS_FILE = "/home/abderrahmane/ID1FS/bin/users.json"


def crypter_mot_de_passe(mot_de_passe):
    # Utilisation de la méthode SHA-512 pour le cryptage du mot de passe
    return crypt.crypt(mot_de_passe, crypt.mksalt(crypt.METHOD_SHA512))


def ajouter_utilisateur_systeme(nom_utilisateur, mot_de_passe):
    # Vérifier si l'utilisateur existe déjà
    try:
        subprocess.run(["id", nom_utilisateur], check=True)
        print(f"L'utilisateur {nom_utilisateur} existe déjà.")
        return
    except subprocess.CalledProcessError:
        pass

    # Ajouter l'utilisateur en utilisant la commande useradd
    subprocess.run(["sudo", "useradd", "-m", nom_utilisateur])

    # Définir le mot de passe pour l'utilisateur avec chpasswd
    input_data = f"{nom_utilisateur}:{mot_de_passe}"
    subprocess.run(["echo", input_data, "|", "sudo", "chpasswd"], shell=True)

    # Enregistrez le nom d'utilisateur et le mot de passe dans le fichier users.json
    enregistrer_utilisateur(nom_utilisateur, mot_de_passe)

    print(f"L'utilisateur {nom_utilisateur} a été ajouté avec succès.")


def enregistrer_utilisateur(nom_utilisateur, mot_de_passe):
    # Charger les utilisateurs existants depuis le fichier users.json s'il existe
    utilisateurs = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            utilisateurs = json.load(file)

    # Enregistrer le nouvel utilisateur
    utilisateurs[nom_utilisateur] = crypter_mot_de_passe(mot_de_passe)

    # Écrire la liste mise à jour dans le fichier users.json
    with open(USERS_FILE, "w") as file:
        json.dump(utilisateurs, file)


def supprimer_utilisateur(nom_utilisateur):
    try:
        subprocess.run(["sudo", "userdel", nom_utilisateur], check=True)
        print(f"L'utilisateur {nom_utilisateur} a été supprimé avec succès.")

        # Supprimer l'utilisateur du fichier users.json s'il existe
        supprimer_utilisateur_fichier(nom_utilisateur)
    except subprocess.CalledProcessError:
        print(f"L'utilisateur {nom_utilisateur} n'existe pas.")


def supprimer_utilisateur_fichier(nom_utilisateur):
    # Charger les utilisateurs existants depuis le fichier users.json s'il existe
    utilisateurs = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            utilisateurs = json.load(file)

        # Supprimer l'utilisateur du fichier users.json
        if nom_utilisateur in utilisateurs:
            del utilisateurs[nom_utilisateur]

            # Écrire la liste mise à jour dans le fichier users.json
            with open(USERS_FILE, "w") as file:
                json.dump(utilisateurs, file)


def changer_utilisateur(nom_utilisateur):
    try:
        subprocess.run(["sudo", "su", "-", nom_utilisateur], check=True)
    except subprocess.CalledProcessError:
        print(f"L'utilisateur {nom_utilisateur} n'existe pas.")


def main():
    parser = argparse.ArgumentParser(description="Gérer les utilisateurs.")
    parser.add_argument("action", choices=["add", "delete", "switch"], help="Action à effectuer (add, delete, switch).")
    parser.add_argument("nom_utilisateur", help="Nom de l'utilisateur.")

    args = parser.parse_args()

    if args.action == "add":
        mot_de_passe = getpass.getpass(prompt=f"Entrez le mot de passe pour {args.nom_utilisateur}: ")
        confirmation_mot_de_passe = getpass.getpass(prompt=f"Confirmez le mot de passe: ")

        if mot_de_passe == confirmation_mot_de_passe:
            ajouter_utilisateur_systeme(args.nom_utilisateur, mot_de_passe)
        else:
            print("Les mots de passe ne correspondent pas. Aucun utilisateur ajouté.")

    elif args.action == "delete":
        supprimer_utilisateur(args.nom_utilisateur)

    elif args.action == "switch":
        changer_utilisateur(args.nom_utilisateur)


if __name__ == "__main__":
    main()

