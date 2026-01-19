# Correction du Problème Celery

## Problème Identifié

Celery ne pouvait pas démarrer car les modules de tasks référencés n'existaient pas :

- `app.tasks.prospector`
- `app.tasks.bant`
- `app.tasks.scheduler`

## Solution Appliquée

### 1. Création des fichiers de tasks manquants

Création de trois fichiers de tasks avec des placeholders :

- `backend/app/tasks/prospector.py` - Task pour trouver des leads
- `backend/app/tasks/bant.py` - Task pour qualifier les leads
- `backend/app/tasks/scheduler.py` - Task pour envoyer des emails

### 2. Modification de celery_app.py

Retrait de la liste `include` explicite dans la configuration Celery, car Celery peut auto-découvrir les tasks depuis le module `app.tasks`.

**Avant :**

```python
celery_app = Celery(
    "vectra",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.prospector", "app.tasks.bant", "app.tasks.scheduler"],
)
```

**Après :**

```python
celery_app = Celery(
    "vectra",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    # Tasks will be auto-discovered from app.tasks module
)
```

### 3. Mise à jour de **init**.py

Ajout des imports dans `app/tasks/__init__.py` pour que les tasks soient enregistrées :

```python
from app.tasks import prospector, bant, scheduler  # noqa: F401
```

## Vérification

Pour vérifier que Celery fonctionne :

```bash
cd backend
venv\Scripts\activate  # Windows
# ou source venv/bin/activate  # Mac/Linux

# Tester l'import
python -c "import app.tasks.celery_app; print('OK')"

# Démarrer Celery worker
celery -A app.tasks.celery_app worker --loglevel=INFO
```

## Prochaines Étapes

Les tasks sont actuellement des placeholders. Il faudra implémenter la logique complète :

1. **prospector.find_leads** - Intégrer l'agent Prospector avec RocketReach
2. **bant.qualify_lead** - Intégrer l'agent BANT avec scoring
3. **scheduler.send_email** - Intégrer l'agent Scheduler avec SendGrid

---

*Dernière mise à jour : 15 Janvier 2026*
