"""Parcours récursif d'un dossier, en lecture seule."""

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class FichierInfo:
    """Informations relevées sur un fichier."""
    chemin: Path
    nom: str
    extension: str  # en minuscules avec le point, "" si absente
    taille: int  # en octets
    date_creation: datetime
    date_modification: datetime


def lire_infos(entree):
    """Construit un FichierInfo à partir d'une entrée de os.scandir."""
    infos = entree.stat(follow_symlinks=False)
    # st_birthtime (date de création) n'existe pas sur tous les systèmes
    creation = getattr(infos, "st_birthtime", infos.st_ctime)
    chemin = Path(entree.path)
    return FichierInfo(
        chemin=chemin,
        nom=entree.name,
        extension=chemin.suffix.lower(),
        taille=infos.st_size,
        date_creation=datetime.fromtimestamp(creation),
        date_modification=datetime.fromtimestamp(infos.st_mtime),
    )


def scanner(dossier):
    """Parcourt un dossier et renvoie (fichiers, erreurs).

    fichiers : liste de FichierInfo
    erreurs : liste de tuples (chemin, message) pour ce qui n'a pas pu être lu
    """
    dossier = Path(dossier)
    if not dossier.is_dir():
        raise NotADirectoryError(f"Ce n'est pas un dossier : {dossier}")

    fichiers = []
    erreurs = []
    _parcourir(dossier, fichiers, erreurs)
    return fichiers, erreurs


def _parcourir(dossier, fichiers, erreurs):
    """Remplit les deux listes, en s'appelant elle-même sur les sous-dossiers."""
    try:
        with os.scandir(dossier) as contenu:
            entrees = list(contenu)
    except OSError as erreur:  # PermissionError est un cas particulier d'OSError
        erreurs.append((Path(dossier), str(erreur)))
        return

    for entree in entrees:
        try:
            # Liens ignorés : ils peuvent sortir du dossier ou créer une boucle
            if entree.is_symlink() or entree.is_junction():
                continue
            if entree.is_dir():
                _parcourir(entree.path, fichiers, erreurs)
            elif entree.is_file():
                fichiers.append(lire_infos(entree))
        except OSError as erreur:
            erreurs.append((Path(entree.path), str(erreur)))
