---

## 3. create-migration.md

```markdown
# Créer une Migration de Base de Données

## Usage
```
/create-migration "<description>"
```

Exemple:
- `/create-migration "add email tracking fields"`

## Ce que cette commande fait

1. Génère une migration Alembic avec autogenerate
2. Review et ajuste le fichier généré
3. Propose les index nécessaires
4. Vérifie la cohérence avec le schema existant

## Commandes exécutées

```bash
cd backend
alembic revision --autogenerate -m "<description>"
```

## Vérifications automatiques

1. **Colonnes NOT NULL** - S'assurer qu'il y a un DEFAULT ou que la table est vide
2. **Foreign Keys** - Vérifier que les tables référencées existent
3. **Index** - Proposer les index pour les FK et colonnes fréquemment filtrées
4. **ENUMs** - Créer le type ENUM avant la colonne

## Template de migration

```python
"""<description>

Revision ID: xxx
Revises: yyy
Create Date: 2026-01-14

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'xxx'
down_revision = 'yyy'
branch_labels = None
depends_on = None

def upgrade():
    # Créer ENUM si nécessaire
    # op.execute("CREATE TYPE status_enum AS ENUM ('a', 'b', 'c')")
    
    # Ajouter colonne
    op.add_column('table_name', sa.Column(
        'new_column',
        sa.String(255),
        nullable=True
    ))
    
    # Créer index
    op.create_index('idx_table_new_column', 'table_name', ['new_column'])

def downgrade():
    op.drop_index('idx_table_new_column', 'table_name')
    op.drop_column('table_name', 'new_column')
    # op.execute("DROP TYPE status_enum")
```

## Checklist avant apply

- [ ] Le fichier de migration est correct
- [ ] Les données existantes ne seront pas perdues
- [ ] Les index sont créés pour les colonnes filtrées
- [ ] downgrade() fonctionne
- [ ] Testé sur une copie de la DB
```

---