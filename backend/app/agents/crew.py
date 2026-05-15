"""CrewAI configuration and setup for Vectra agents."""

from typing import Optional, Any
from crewai import Agent, Crew, Process, Task, LLM
from crewai.memory import ShortTermMemory

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def get_llm() -> Optional[Any]:
    """
    Get configured LLM for CrewAI agents.

    Claude (Anthropic) is the primary provider — the brain for all agent reasoning.
    Ollama is kept as optional fallback.
    Returns an explicit LLM object so CrewAI never falls back to OpenAI.
    """
    api_key = settings.ANTHROPIC_API_KEY or settings.CLAUDE_API_KEY

    # Claude — primary provider
    if settings.LLM_PROVIDER == "claude" and api_key:
        try:
            llm = LLM(
                model=f"anthropic/{settings.CLAUDE_MODEL}",
                api_key=api_key,
            )
            logger.info(f"LLM configured: Claude ({settings.CLAUDE_MODEL})")
            return llm
        except Exception as e:
            logger.warning(f"Claude LLM init failed: {e}, trying Ollama fallback")

    # Ollama fallback (local)
    if settings.OLLAMA_BASE_URL and settings.OLLAMA_API_KEY:
        try:
            llm = LLM(
                model=f"ollama/{settings.OLLAMA_MODEL}",
                base_url=settings.OLLAMA_BASE_URL,
                api_key=settings.OLLAMA_API_KEY,
            )
            logger.info(f"LLM configured: Ollama {settings.OLLAMA_MODEL}")
            return llm
        except Exception as e:
            logger.warning(f"Ollama LLM init failed: {e}")

    logger.warning("No LLM configured — agents use direct API calls (email gen uses template fallback)")
    return None


def get_memory() -> Optional[ShortTermMemory]:
    """
    Get Redis-based memory for CrewAI agents.
    
    Uses Redis for context storage between agent runs.
    
    Returns:
        ShortTermMemory instance or None if Redis not available
    """
    if not settings.REDIS_URL:
        logger.warning("REDIS_URL not configured - agents will not use persistent memory")
        return None
    
    try:
        # CrewAI ShortTermMemory uses Redis internally
        # This will be configured per-agent or per-crew
        memory = ShortTermMemory()
        logger.info("Memory configured: Redis via CrewAI ShortTermMemory")
        return memory
    except Exception as e:
        logger.warning(f"Failed to initialize Redis memory: {e}")
        return None


def create_crew(
    agents: list[Agent],
    tasks: list,
    process: Process = Process.sequential,
    memory: Optional[ShortTermMemory] = None,
    verbose: bool = True,
) -> Crew:
    """
    Create a CrewAI crew with configured LLM and memory.
    
    Args:
        agents: List of CrewAI agents
        tasks: List of tasks for the crew
        process: Process type (sequential, hierarchical, consensual)
        memory: Optional memory instance
        verbose: Enable verbose logging
    
    Returns:
        Configured Crew instance
    """
    llm = get_llm()
    
    crew_config = {
        "agents": agents,
        "tasks": tasks,
        "process": process,
        "verbose": verbose,
    }
    
    if llm:
        crew_config["llm"] = llm
    
    if memory:
        crew_config["memory"] = memory
    
    crew = Crew(**crew_config)
    
    logger.info(f"Crew created with {len(agents)} agents, {len(tasks)} tasks, process={process}")
    
    return crew


def get_default_agent_config() -> dict:
    """
    Get default configuration for agents.
    
    Returns:
        Dictionary with default agent configuration
    """
    return {
        "llm": get_llm(),
        "memory": get_memory(),
        "verbose": True,
        "allow_delegation": False,
        "max_iter": 3,
        "max_execution_time": 300,  # 5 minutes max per agent execution
    }
