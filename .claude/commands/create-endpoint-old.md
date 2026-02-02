---

## 2. create-endpoint.md

```markdown
# Créer un Endpoint API

## Usage
```
/create-endpoint <resource> <method>
```

Exemples:
- `/create-endpoint campaigns GET`
- `/create-endpoint leads POST`

## Ce que cette commande fait

1. Crée ou met à jour le fichier route dans `backend/app/api/v1/`
2. Crée le schema Pydantic si nécessaire
3. Crée/met à jour le service
4. Crée les tests d'intégration
5. Met à jour le router principal

## Pattern à suivre

### Route (api/v1/<resource>.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.schemas.<resource> import <Resource>Create, <Resource>Response
from app.services.<resource> import <Resource>Service
from app.db.models import User

router = APIRouter(prefix="/<resources>", tags=["<resources>"])

@router.get("", response_model=list[<Resource>Response])
async def list_<resources>(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
):
    """List all <resources> for the current organization."""
    service = <Resource>Service(db)
    return await service.list(
        organization_id=current_user.organization_id,
        skip=skip,
        limit=limit
    )

@router.post("", response_model=<Resource>Response, status_code=status.HTTP_201_CREATED)
async def create_<resource>(
    data: <Resource>Create,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new <resource>."""
    service = <Resource>Service(db)
    return await service.create(
        organization_id=current_user.organization_id,
        created_by=current_user.id,
        **data.model_dump()
    )

@router.get("/{id}", response_model=<Resource>Response)
async def get_<resource>(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a <resource> by ID."""
    service = <Resource>Service(db)
    result = await service.get(id, organization_id=current_user.organization_id)
    if not result:
        raise HTTPException(status_code=404, detail="<Resource> not found")
    return result
```

### Schema (schemas/<resource>.py)

```python
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class <Resource>Base(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    # autres champs

class <Resource>Create(<Resource>Base):
    pass

class <Resource>Update(BaseModel):
    name: Optional[str] = None
    # autres champs optionnels

class <Resource>Response(<Resource>Base):
    id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

## Checklist

- [ ] Route créée avec tous les CRUD nécessaires
- [ ] Schema Pydantic avec validation
- [ ] Service avec logique métier
- [ ] Tests d'intégration
- [ ] Mis à jour dans router.py
- [ ] Documentation OpenAPI correcte
```

---