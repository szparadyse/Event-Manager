# Event-Manager

Application Django de gestion d'événements avec catégories, tags, images, avis et réponses.

## Description rapide

- **Événements**: titre, catégorie, date, lieu, places, créateur
- **Avis (reviews)**: texte, note, auteur, date de création
- **Réponses (answers)**: réponses aux avis
- **Images**: associées aux événements et éventuellement aux avis, avec **tags**

## Prérequis

- Python 3.10+
- pip
- Optionnel: virtualenv

## Installation et lancement

1. Cloner le projet et se placer dans le dossier du projet Django

```bash
git clone <votre_repo>
cd Event-Manager/eventManager
```

2. Créer et activer un environnement virtuel (si besoin)

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# Sous Windows: venv\Scripts\activate
```

3. Installer les dépendances

```bash
pip install django
# Si un requirements.txt est présent, utilisez:
# pip install -r requirements.txt
```

4. Appliquer les migrations

```bash
python manage.py migrate
```

5. (Optionnel) Créer un superutilisateur pour accéder à l'admin

```bash
python manage.py createsuperuser
```

6. Insérer des données de test

```bash
python populate_test_data.py
```

Ce script crée des utilisateurs, catégories, tags, événements, avis, réponses et images. Il est idempotent: vous pouvez le relancer sans dupliquer les principales entrées.

7. Lancer le serveur de développement

```bash
python manage.py runserver
```

Accéder à l'application: `http://127.0.0.1:8000/`

## Structure utile

- `eventManager/accounts/models.py`: modèles (`Categories`, `Tags`, `Events`, `Image`, `EventReviews`, `Answers`)
- `eventManager/populate_test_data.py`: insertion de données de test
- `eventManager/templates/` et `accounts/templates/`: templates
- `eventManager/eventManager/settings.py`: configuration Django

## Notes

- Les chemins d'images utilisés par le script (`images/...`) sont symboliques. Ajoutez des fichiers si vous affichez réellement ces images.
- Pensez à définir le fuseau horaire dans `settings.py` si nécessaire (`TIME_ZONE`).
