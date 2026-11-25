"""Génère un jeu de faux fichiers dans test_data/.

Utilisation : python scripts/generate_testset.py [nombre]
"""

import argparse
import random
from pathlib import Path

# Racine du projet = dossier parent de scripts/
DOSSIER = Path(__file__).resolve().parent.parent / "test_data"

SOUS_DOSSIERS = ["", "telechargements", "bureau", "bureau/vieux", "photos/été 2025"]
EXTENSIONS = [".txt", ".pdf", ".docx", ".xlsx", ".jpg", ".PNG", ".mp3",
              ".mp4", ".zip", ".py", ".csv", ".inconnu"]
MOTS = ["rapport", "facture", "photo", "cours", "projet", "musique"]
MOTS_ACCENTS = ["été", "Noël", "reçu", "élève", "forêt", "garçon", "cœur"]


def choisir_nom(numero, cas):
    """Construit un nom unique (grâce au numéro) selon le cas voulu."""
    extension = random.choice(EXTENSIONS)
    if cas == "accents":
        return f"{random.choice(MOTS_ACCENTS)}_{numero}{extension}"
    if cas == "long":
        # 150 caractères : long, mais sous la limite Windows de 260 par chemin
        fin = f"_{numero}{extension}"
        return "nom_tres_long_".ljust(150 - len(fin), "x") + fin
    if cas == "sans_extension":
        return f"{random.choice(MOTS)}_{numero}"
    return f"{random.choice(MOTS)}_{numero}{extension}"


def choisir_cas(numero):
    """Sur 10 fichiers : 1 doublon, 1 accents, 1 long, 1 sans extension, 6 normaux."""
    cas_speciaux = {0: "doublon", 1: "accents", 2: "long", 3: "sans_extension"}
    return cas_speciaux.get(numero % 10, "normal")


def generer(nombre):
    """Crée les fichiers et renvoie le nombre de fichiers par cas."""
    random.seed(42)  # même graine = même jeu de test à chaque lancement
    compteur = {}
    originaux = []  # fichiers déjà créés, que l'on peut dupliquer

    for numero in range(1, nombre + 1):
        cas = choisir_cas(numero)
        if cas == "doublon":
            original = random.choice(originaux)
            nom = f"copie_{numero}{original.suffix}"
            contenu = original.read_bytes()
        else:
            nom = choisir_nom(numero, cas)
            # Le numéro rend chaque contenu unique ; la taille est variable
            contenu = f"Fichier de test {numero}\n".encode() + random.randbytes(
                random.randint(0, 4096))

        chemin = DOSSIER / random.choice(SOUS_DOSSIERS) / nom
        chemin.parent.mkdir(parents=True, exist_ok=True)
        with open(chemin, "xb") as fichier:  # "x" : erreur si le fichier existe
            fichier.write(contenu)

        if cas != "doublon":
            originaux.append(chemin)
        compteur[cas] = compteur.get(cas, 0) + 1
    return compteur


def main():
    parser = argparse.ArgumentParser(description="Génère un jeu de fichiers de test.")
    parser.add_argument("nombre", nargs="?", type=int, default=1000,
                        help="nombre de fichiers à créer (1000 par défaut)")
    args = parser.parse_args()

    if args.nombre < 1:
        parser.error("le nombre doit être au moins 1")
    if DOSSIER.exists() and any(DOSSIER.iterdir()):
        parser.error(f"{DOSSIER} n'est pas vide : supprime-le avant de relancer")

    compteur = generer(args.nombre)
    print(f"{args.nombre} fichiers créés dans {DOSSIER}")
    for cas, total in compteur.items():
        print(f"  {cas} : {total}")


if __name__ == "__main__":
    main()
