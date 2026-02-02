"""Base agent class for Vectra agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from crewai import Agent, Task, Crew
from crewai.memory import ShortTermMemory

from app.agents.crew import get_llm, get_memory, get_default_agent_config
from app.agents.tools import get_shared_tools
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class BaseVectraAgent(ABC):
    """Base class for all Vectra agents using CrewAI."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the agent with CrewAI configuration."""
        self.config = config or {}
        self.logger = get_logger(self.__class__.__name__)
        
        # Get default config and merge with provided config
        default_config = get_default_agent_config()
        agent_config = {**default_config, **self.config}
        
        # Initialize CrewAI Agent
        self.crewai_agent = self._create_crewai_agent(agent_config)
        
        # Tools available to this agent
        self.tools = self._get_tools()

    def _create_crewai_agent(self, config: Dict[str, Any]) -> Agent:
        """
        Create a CrewAI Agent instance.
        
        Args:
            config: Agent configuration
            
        Returns:
            CrewAI Agent instance
        """
        agent_kwargs = {
            "role": self._get_role(),
            "goal": self._get_goal(),
            "backstory": self._get_backstory(),
            "verbose": config.get("verbose", True),
            "allow_delegation": config.get("allow_delegation", False),
            "max_iter": config.get("max_iter", 3),
            "max_execution_time": config.get("max_execution_time", 300),
        }
        
        # Add tools if available
        tools = self._get_tools()
        if tools:
            agent_kwargs["tools"] = tools
        
        # Add LLM if configured
        llm = config.get("llm") or get_llm()
        if llm:
            agent_kwargs["llm"] = llm
        
        # Add memory if configured
        memory = config.get("memory") or get_memory()
        if memory:
            agent_kwargs["memory"] = memory
        
        agent = Agent(**agent_kwargs)
        self.logger.info(f"Created CrewAI agent: {self.__class__.__name__}")
        
        return agent

    @abstractmethod
    def _get_role(self) -> str:
        """Return the agent's role."""
        pass

    @abstractmethod
    def _get_goal(self) -> str:
        """Return the agent's goal."""
        pass

    @abstractmethod
    def _get_backstory(self) -> str:
        """Return the agent's backstory."""
        pass

    def _get_tools(self) -> List[Any]:
        """
        Get tools available to this agent.
        
        Override in subclasses to add agent-specific tools.
        
        Returns:
            List of tools
        """
        # Start with shared tools
        tools = get_shared_tools()
        return tools

    def _build_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        Build the prompt from input data.
        
        Override in subclasses to customize prompt building.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Formatted prompt string
        """
        # Default implementation - override in subclasses
        return ""

    def _parse_result(self, result: Any) -> Dict[str, Any]:
        """
        Parse the agent result.
        
        Override in subclasses to customize result parsing.
        
        Args:
            result: Raw result from CrewAI
            
        Returns:
            Parsed result dictionary
        """
        # Default implementation
        if isinstance(result, dict):
            return {"success": True, "data": result}
        return {"success": True, "data": str(result)}

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent task.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Result dictionary with 'success' and 'data' keys
        """
        pass

    def _create_task(self, description: str, expected_output: str = "") -> Task:
        """
        Create a CrewAI Task for this agent.
        
        Args:
            description: Task description
            expected_output: Expected output format
            
        Returns:
            CrewAI Task instance
        """
        if not expected_output:
            expected_output = "JSON format with the results"
        
        task = Task(
            description=description,
            agent=self.crewai_agent,
            expected_output=expected_output,
        )
        
        return task

    def _execute_crew(self, tasks: List[Task]) -> Any:
        """
        Execute a Crew with tasks.
        
        Args:
            tasks: List of tasks to execute
            
        Returns:
            Crew execution result
        """
        from crewai import Process
        
        crew = Crew(
            agents=[self.crewai_agent],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )
        
        self.logger.info(f"Executing crew with {len(tasks)} task(s)")
        result = crew.kickoff()
        
        return result
