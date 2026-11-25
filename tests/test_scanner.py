"""Tests du scanner. Lancement : py -m unittest discover tests"""

import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from filesense.scanner import scanner


class TestScanner(unittest.TestCase):

    def setUp(self):
        """Crée un dossier temporaire avant chaque test, supprimé après."""
        temporaire = tempfile.TemporaryDirectory()
        self.addCleanup(temporaire.cleanup)
        self.dossier = Path(temporaire.name)

    def test_parcours_recursif(self):
        sous_dossier = self.dossier / "a" / "b"
        sous_dossier.mkdir(parents=True)
        (self.dossier / "racine.txt").touch()
        (sous_dossier / "profond.txt").touch()

        fichiers, erreurs = scanner(self.dossier)

        self.assertEqual({f.nom for f in fichiers}, {"racine.txt", "profond.txt"})
        self.assertEqual(erreurs, [])

    def test_informations_du_fichier(self):
        chemin = self.dossier / "Été.PNG"
        chemin.write_bytes(b"12345")
        date = datetime(2025, 1, 15, 12, 0)
        os.utime(chemin, (date.timestamp(), date.timestamp()))
        (self.dossier / "sans_extension").touch()

        fichiers, _ = scanner(self.dossier)
        par_nom = {f.nom: f for f in fichiers}

        image = par_nom["Été.PNG"]
        self.assertEqual(image.chemin, chemin)
        self.assertEqual(image.extension, ".png")
        self.assertEqual(image.taille, 5)
        self.assertEqual(image.date_modification, date)
        self.assertIsInstance(image.date_creation, datetime)
        self.assertEqual(par_nom["sans_extension"].extension, "")

    def test_dossier_interdit(self):
        interdit = self.dossier / "interdit"
        interdit.mkdir()
        (self.dossier / "lisible.txt").touch()
        vrai_scandir = os.scandir

        def faux_scandir(chemin):
            """Simule un refus d'accès, seulement sur le dossier interdit."""
            if Path(chemin) == interdit:
                raise PermissionError("Accès refusé")
            return vrai_scandir(chemin)

        with patch("filesense.scanner.os.scandir", faux_scandir):
            fichiers, erreurs = scanner(self.dossier)

        self.assertEqual([f.nom for f in fichiers], ["lisible.txt"])
        self.assertEqual(erreurs, [(interdit, "Accès refusé")])


if __name__ == "__main__":
    unittest.main()
