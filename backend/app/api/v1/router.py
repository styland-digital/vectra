"""Main API router for v1."""

from fastapi import APIRouter

from app.api.v1 import auth, admin, user, campaigns, leads, emails

# Create main router
api_router = APIRouter(prefix="/api/v1", tags=["v1"])

# Routes partagées (auth)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Routes Platform Admin
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

# Routes User/Organisation
api_router.include_router(user.router, prefix="/user", tags=["user"])

# Routes Campaigns (under /user/campaigns)
api_router.include_router(campaigns.router, prefix="/user/campaigns", tags=["campaigns"])

# Routes Leads (under /user/leads)
api_router.include_router(leads.router, prefix="/user/leads", tags=["leads"])

# Routes Emails (under /user/emails)
api_router.include_router(emails.router, prefix="/user/emails", tags=["emails"])

# TODO: Include other sub-routers when implemented
# from app.api.v1 import meetings, analytics
# api_router.include_router(meetings.router, prefix="/user/meetings", tags=["meetings"])
# api_router.include_router(analytics.router, prefix="/user/analytics", tags=["analytics"])
