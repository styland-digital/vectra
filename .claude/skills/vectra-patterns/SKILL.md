---
name: vectra-patterns
description: Vectra-specific coding patterns, conventions, and best practices. Auto-activates when working on Vectra codebase for campaigns, leads, emails, meetings, or agents.
---

# Vectra Development Patterns

## Multi-Tenant Architecture

### 🚨 CRITICAL: Every Query Must Filter by Organization

```python
# ✅ CORRECT - Always filter by organization
async def get_campaigns(self) -> list[Campaign]:
    stmt = select(Campaign).where(
        Campaign.organization_id == self.org_id
    )
    return list(await self.db.scalars(stmt))

# ❌ WRONG - Missing organization filter (SECURITY RISK)
async def get_campaigns(self) -> list[Campaign]:
    return list(await self.db.scalars(select(Campaign)))
```

### Service Layer Pattern

All business logic goes in services, not routes.

```python
# app/services/campaign_service.py
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate

class CampaignService:
    """Campaign business logic with multi-tenant isolation."""
    
    def __init__(self, db: AsyncSession, org_id: UUID):
        self.db = db
        self.org_id = org_id
    
    async def list(self, status: str | None = None) -> list[Campaign]:
        """List campaigns for organization."""
        stmt = select(Campaign).where(
            Campaign.organization_id == self.org_id
        )
        if status:
            stmt = stmt.where(Campaign.status == status)
        return list(await self.db.scalars(stmt))
    
    async def get(self, campaign_id: UUID) -> Campaign | None:
        """Get campaign by ID with org check."""
        campaign = await self.db.get(Campaign, campaign_id)
        if campaign and campaign.organization_id == self.org_id:
            return campaign
        return None
    
    async def create(self, data: CampaignCreate) -> Campaign:
        """Create new campaign."""
        campaign = Campaign(
            organization_id=self.org_id,
            **data.model_dump()
        )
        self.db.add(campaign)
        await self.db.commit()
        await self.db.refresh(campaign)
        return campaign
    
    async def update(self, campaign_id: UUID, data: CampaignUpdate) -> Campaign:
        """Update campaign."""
        campaign = await self.get(campaign_id)
        if not campaign:
            raise CampaignNotFoundError(campaign_id)
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(campaign, field, value)
        
        await self.db.commit()
        await self.db.refresh(campaign)
        return campaign
```

## API Endpoint Pattern

```python
# app/api/v1/campaigns.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.services.campaign_service import CampaignService
from app.schemas.campaign import CampaignCreate, CampaignResponse
from app.models import User

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.get("/", response_model=list[CampaignResponse])
async def list_campaigns(
    status: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all campaigns for current organization."""
    service = CampaignService(db, current_user.organization_id)
    return await service.list(status=status)

@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    data: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new campaign."""
    service = CampaignService(db, current_user.organization_id)
    return await service.create(data)

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get campaign by ID."""
    service = CampaignService(db, current_user.organization_id)
    campaign = await service.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign
```

## Pydantic Schema Pattern

```python
# app/schemas/campaign.py
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID
from typing import Any

class CampaignBase(BaseModel):
    """Shared campaign fields."""
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    target_criteria: dict[str, Any] = Field(default_factory=dict)
    bant_threshold: int = Field(default=60, ge=0, le=100)

class CampaignCreate(CampaignBase):
    """Fields for creating a campaign."""
    pass

class CampaignUpdate(BaseModel):
    """Fields for updating a campaign (all optional)."""
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    target_criteria: dict[str, Any] | None = None
    bant_threshold: int | None = Field(None, ge=0, le=100)
    status: str | None = None

class CampaignResponse(CampaignBase):
    """Campaign response with all fields."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    organization_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
```

## Exception Handling Pattern

```python
# app/core/exceptions.py
from fastapi import HTTPException

class VectraException(HTTPException):
    """Base exception for Vectra."""
    status_code: int = 500
    code: str = "INTERNAL_ERROR"
    
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=self.status_code,
            detail={"code": self.code, "message": detail or self.code}
        )

class NotFoundError(VectraException):
    status_code = 404
    code = "NOT_FOUND"

class CampaignNotFoundError(NotFoundError):
    code = "CAMPAIGN_NOT_FOUND"
    
    def __init__(self, campaign_id: UUID):
        super().__init__(f"Campaign {campaign_id} not found")

class UnauthorizedError(VectraException):
    status_code = 401
    code = "UNAUTHORIZED"

class ForbiddenError(VectraException):
    status_code = 403
    code = "FORBIDDEN"
```

## React Component Pattern

```typescript
// components/features/campaigns/CampaignCard.tsx
import { Campaign } from '@/lib/types'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { formatDate } from '@/lib/utils'

interface CampaignCardProps {
  campaign: Campaign
  onSelect?: (id: string) => void
}

export function CampaignCard({ campaign, onSelect }: CampaignCardProps) {
  const statusVariant = {
    draft: 'secondary',
    active: 'default',
    paused: 'warning',
    completed: 'success',
  }[campaign.status] as 'secondary' | 'default' | 'warning' | 'success'

  return (
    <Card 
      className="cursor-pointer hover:shadow-md transition-shadow"
      onClick={() => onSelect?.(campaign.id)}
    >
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-lg font-semibold truncate">
          {campaign.name}
        </CardTitle>
        <Badge variant={statusVariant}>{campaign.status}</Badge>
      </CardHeader>
      <CardContent>
        <div className="flex justify-between text-sm text-muted-foreground">
          <span>{campaign.leadsCount} leads</span>
          <span>{formatDate(campaign.createdAt)}</span>
        </div>
      </CardContent>
    </Card>
  )
}
```

## Data Fetching Pattern (React Query)

```typescript
// lib/hooks/useCampaigns.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { Campaign, CampaignCreate } from '@/lib/types'

export function useCampaigns(status?: string) {
  return useQuery({
    queryKey: ['campaigns', { status }],
    queryFn: () => api.get<Campaign[]>('/campaigns', { params: { status } }),
  })
}

export function useCampaign(id: string) {
  return useQuery({
    queryKey: ['campaigns', id],
    queryFn: () => api.get<Campaign>(`/campaigns/${id}`),
    enabled: !!id,
  })
}

export function useCreateCampaign() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: CampaignCreate) => api.post<Campaign>('/campaigns', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] })
    },
  })
}
```

## References

For more detailed examples, see:
- `references/api-patterns.md` - More API endpoint patterns
- `references/agent-patterns.md` - CrewAI agent patterns
- `references/testing-patterns.md` - Test examples
