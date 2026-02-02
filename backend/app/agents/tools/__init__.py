"""Shared tools for Vectra agents."""

from typing import List, Any

from app.core.logging import get_logger

logger = get_logger(__name__)


def get_shared_tools() -> List[Any]:
    """
    Get shared tools available to all agents.
    
    Returns:
        List of CrewAI tools
    """
    # Tools will be added here as needed
    # Examples:
    # - Database query tools
    # - API integration tools
    # - Data validation tools
    
    tools: List[Any] = []
    
    logger.debug(f"Returning {len(tools)} shared tools")
    
    return tools


def get_tool_by_name(name: str) -> Any:
    """
    Get a specific tool by name.
    
    Args:
        name: Name of the tool
    
    Returns:
        Tool instance
    
    Raises:
        ValueError: If tool not found
    """
    tools = get_shared_tools()
    
    for tool in tools:
        if tool.name == name:
            return tool
    
    raise ValueError(f"Tool '{name}' not found")


__all__ = ["get_shared_tools", "get_tool_by_name"]
