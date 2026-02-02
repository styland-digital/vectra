---
description: Create a new API endpoint with schema, service, router, and tests following Vectra patterns.
allowed-tools: Read, Write, Edit, Bash
skills: fastapi-backend, vectra-patterns
---

# Create API Endpoint: $ARGUMENTS

## Files to Create

### 1. Schema (`backend/app/schemas/$ARGUMENTS.py`)
```python
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID

class ${ARGUMENTS}Base(BaseModel):
    # Add fields here
    pass

class ${ARGUMENTS}Create(${ARGUMENTS}Base):
    pass

class ${ARGUMENTS}Update(BaseModel):
    # All fields optional for partial update
    pass

class ${ARGUMENTS}Response(${ARGUMENTS}Base):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime
```

### 2. Service (`backend/app/services/${ARGUMENTS}_service.py`)
```python
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import ${ARGUMENTS}
from app.schemas.${ARGUMENTS} import ${ARGUMENTS}Create, ${ARGUMENTS}Update

class ${ARGUMENTS}Service:
    def __init__(self, db: AsyncSession, org_id: UUID):
        self.db = db
        self.org_id = org_id
    
    # Implement CRUD methods with org_id filter
```

### 3. Router (`backend/app/api/v1/$ARGUMENTS.py`)
```python
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_db, get_current_user
from app.services.${ARGUMENTS}_service import ${ARGUMENTS}Service

router = APIRouter(prefix="/$ARGUMENTS", tags=["$ARGUMENTS"])

# Implement endpoints
```

### 4. Tests (`backend/tests/test_api/test_$ARGUMENTS.py`)
```python
import pytest
from httpx import AsyncClient

class Test${ARGUMENTS}API:
    # Write tests FIRST
    pass
```

### 5. Register in `backend/app/api/v1/__init__.py`
```python
from app.api.v1.$ARGUMENTS import router as ${ARGUMENTS}_router
api_router.include_router(${ARGUMENTS}_router)
```

## Follow TDD
1. Write tests first
2. Run tests (should fail)
3. Implement code
4. Run tests (should pass)
