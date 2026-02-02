---
name: crewai-agents
description: CrewAI multi-agent patterns for AI prospection, BANT qualification, and meeting scheduling. Use when working on Vectra's AI agents.
---

# CrewAI Agent Patterns for Vectra

## Overview

Vectra uses 3 specialized AI agents orchestrated by CrewAI:

1. **Prospector Agent** - Finds and enriches leads
2. **BANT Agent** - Qualifies leads with scoring
3. **Scheduler Agent** - Generates personalized emails

## Agent Base Class

```python
# app/agents/base.py
from abc import ABC, abstractmethod
from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from langchain_anthropic import ChatAnthropic
from app.core.config import settings

class BaseAgent(ABC):
    """Base class for all Vectra agents."""
    
    def __init__(self):
        self.llm = self._get_llm()
        self.agent = self._create_agent()
    
    def _get_llm(self):
        """Get LLM based on config."""
        if settings.USE_CLAUDE:
            return ChatAnthropic(
                model="claude-sonnet-4-20250514",
                api_key=settings.ANTHROPIC_API_KEY,
            )
        return Ollama(model="llama2:70b")
    
    @abstractmethod
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent."""
        pass
    
    async def run(self, input_data: dict) -> dict:
        """Run the agent with given input."""
        task = self._create_task(input_data)
        crew = Crew(agents=[self.agent], tasks=[task], verbose=True)
        result = await crew.kickoff_async()
        return self._parse_result(result)
```

## BANT Qualifier Agent

```python
# app/agents/bant.py
from crewai import Agent, Task
from app.agents.base import BaseAgent
import json

class BANTAgent(BaseAgent):
    """Agent for qualifying leads using BANT framework."""
    
    def _create_agent(self) -> Agent:
        return Agent(
            role="BANT Lead Qualifier",
            goal="Score leads 0-100 using BANT framework",
            backstory="""You are a senior sales qualification expert. You 
            analyze prospects using the BANT framework to determine if they 
            are sales-ready. You provide objective scores with clear reasoning.""",
            llm=self.llm,
            verbose=True,
        )
    
    def _create_task(self, input_data: dict) -> Task:
        lead = input_data.get("lead", {})
        
        return Task(
            description=f"""
            Analyze this prospect and provide BANT score:
            
            - Name: {lead.get('name')}
            - Title: {lead.get('job_title')}
            - Company: {lead.get('company_name')}
            - Size: {lead.get('company_size')}
            
            ## Scoring (0-25 each)
            - Budget: Company size & funding
            - Authority: Decision-making level
            - Need: Growth signals
            - Timeline: Recent activity
            
            Return JSON with scores and reasoning.
            """,
            agent=self.agent,
            expected_output="JSON with BANT scores"
        )
```

## Campaign Orchestrator

```python
# app/agents/orchestrator.py
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.prospector import ProspectorAgent
from app.agents.bant import BANTAgent
from app.agents.scheduler import SchedulerAgent

class CampaignOrchestrator:
    """Orchestrates the 3 agents for a campaign."""
    
    def __init__(self, db: AsyncSession, org_id: UUID):
        self.db = db
        self.org_id = org_id
        self.prospector = ProspectorAgent()
        self.bant = BANTAgent()
        self.scheduler = SchedulerAgent()
    
    async def run_campaign(self, campaign_id: UUID) -> dict:
        """Run full campaign pipeline."""
        campaign = await self._get_campaign(campaign_id)
        
        # Step 1: Prospect
        prospects = await self._prospect(campaign)
        
        # Step 2: Qualify
        qualified = await self._qualify(prospects, campaign)
        
        # Step 3: Generate emails
        emails = await self._generate_emails(qualified, campaign)
        
        return {
            "prospects_found": len(prospects),
            "qualified": len(qualified),
            "emails_generated": len(emails),
        }
```

## Celery Integration

```python
# app/tasks/campaign_tasks.py
from celery import shared_task
import asyncio

@shared_task(bind=True, max_retries=3)
def run_campaign_task(self, campaign_id: str, org_id: str):
    """Celery task to run campaign asynchronously."""
    try:
        asyncio.run(_run_campaign(campaign_id, org_id))
    except Exception as exc:
        self.retry(exc=exc, countdown=60 * (self.request.retries + 1))
```
