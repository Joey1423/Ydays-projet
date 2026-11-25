Projet individuel de développement — 2e année.

FileSense est un logiciel qui range, nettoie et retrouve automatiquement des fichiers, **sans jamais en perdre un seul** : tri par règles configurables, détection de doublons, annulation de toute opération, surveillance en temps réel et interface.

> ⚠️ Tous les tests se font sur des dossiers de test générés par script, jamais sur de vrais documents.

## Objectifs par niveau

### Niveau 1 — Socle (évaluation intermédiaire)
- [x] Scan récursif d'un dossier (nom, taille, dates, type)
- [ ] Tri par catégories selon des règles
- [ ] Mode simulation (dry-run)
- [ ] Gestion des conflits de noms (jamais d'écrasement), des fichiers verrouillés et des permissions
- [ ] Journal de toutes les opérations
- [ ] Ligne de commande avec options claires
- [x] Script de génération du jeu de test (1 000 puis 10 000 fichiers)
- [ ] Au moins 10 tests automatisés (3 pour l'instant)
- [ ] Schéma d'architecture et fichier de configuration

### Niveau 2 — Avancé (évaluation finale)
- [ ] Moteur de règles configurable (YAML/JSON)
- [ ] Détection de doublons (taille puis SHA-256)
- [ ] Annulation (undo) via un journal transactionnel SQLite
- [ ] Renommage par métadonnées (EXIF, titre PDF, tags audio)
- [ ] Surveillance d'un dossier en temps réel
- [ ] Interface graphique ou web locale
- [ ] Au moins 25 tests, dont les cas limites

### Niveau 3 — Expert (au moins une fonctionnalité)
- [ ] À choisir

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
# Générer le jeu de test (1000 fichiers par défaut) dans test_data/
python scripts/generate_testset.py
python scripts/generate_testset.py 10000

# Lancer les tests
pytest
```

_Le reste sera complété au fur et à mesure._

## Journal de bord

| Date | Séance | Travail réalisé |
|------|--------|-----------------|
| ~11/11/2026 | Séance 1 | Prise de connaissance du sujet : lecture et analyse du sujet FileSense, identification des trois niveaux attendus (socle, avancé, expert), des livrables des deux évaluations, des barèmes et des contraintes principales (aucune perte de fichier, tests uniquement sur des dossiers de test, commits réguliers, usage de l'IA à noter). |
| 25/11/2026 | Séance 2 | Mise en place de la structure du projet (modules `scanner`, `rules`, `actions`, `journal`, `cli`, dossiers `tests/` et `scripts/`, `config.yaml`, `.gitignore`). Création du générateur de jeu de test (`scripts/generate_testset.py`) : nombre de fichiers en argument, types variés, sous-dossiers, doublons, noms avec accents, noms très longs et fichiers sans extension, sans jamais écraser un fichier existant. Création du scanner récursif (`filesense/scanner.py`) qui récupère nom, taille, dates et extension et gère les erreurs de permission, avec 3 premiers tests automatisés. Préparation de l'oral de la séance suivante. |