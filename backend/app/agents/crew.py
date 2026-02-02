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
    
    Priority:
    1. Ollama (local) if OLLAMA_BASE_URL configured
    2. Claude API (fallback) if CLAUDE_API_KEY configured
    3. None (will use default)
    
    Note: CrewAI automatically detects LLM providers via environment variables:
    - OLLAMA_BASE_URL and OLLAMA_MODEL for Ollama
    - ANTHROPIC_API_KEY for Claude
    
    Returns:
        LLM instance or None (will use CrewAI default)
    """
    # Ollama Cloud API (priority if API key is set)
    if settings.LLM_PROVIDER == "ollama" and settings.OLLAMA_API_KEY:
        try:
            import os
            os.environ["OLLAMA_API_KEY"] = settings.OLLAMA_API_KEY
            os.environ["OLLAMA_HOST"] = settings.OLLAMA_CLOUD_HOST
            os.environ["OLLAMA_MODEL"] = settings.OLLAMA_MODEL
            logger.info(f"LLM configured: Ollama Cloud {settings.OLLAMA_MODEL} at {settings.OLLAMA_CLOUD_HOST}")
            return None
        except Exception as e:
            logger.warning(f"Failed to initialize Ollama Cloud LLM: {e}, falling back to local/remote Ollama")
    
    # Ollama local/remote
    if settings.LLM_PROVIDER == "ollama" and settings.OLLAMA_BASE_URL:
        try:
            import os
            os.environ["OLLAMA_BASE_URL"] = settings.OLLAMA_BASE_URL
            os.environ["OLLAMA_MODEL"] = settings.OLLAMA_MODEL
            logger.info(f"LLM configured: Ollama {settings.OLLAMA_MODEL} at {settings.OLLAMA_BASE_URL}")
            return None
        except Exception as e:
            logger.warning(f"Failed to initialize Ollama LLM: {e}, falling back to Claude")
    
    # Fallback to Claude API via environment variable
    if settings.CLAUDE_API_KEY:
        try:
            # CrewAI supports Claude via ANTHROPIC_API_KEY env var
            logger.info("LLM configured: Claude API (fallback)")
            logger.info("Note: Set ANTHROPIC_API_KEY environment variable for CrewAI to use Claude")
            # Return None to use CrewAI default (which respects env vars)
            return None
        except Exception as e:
            logger.warning(f"Failed to initialize Claude LLM: {e}")
    
    logger.warning("No LLM configured - using default CrewAI LLM")
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
