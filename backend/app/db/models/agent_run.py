"""Agent run model for tracking AI agent executions."""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import BaseModel


class AgentType(str, enum.Enum):
    """AI agent types in the system."""
    PROSPECTOR = "prospector"
    BANT_QUALIFIER = "bant_qualifier"
    SCHEDULER = "scheduler"
    INTENT_CLASSIFIER = "intent_classifier"


class AgentRunStatus(str, enum.Enum):
    """Agent run status values."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class AgentRun(BaseModel):
    """
    Agent run model - Track AI agent executions.

    Records input, output, timing, and resource usage for each agent run.
    """

    __tablename__ = "agent_runs"

    # Campaign association
    campaign_id = Column(
        UUID(as_uuid=True),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Agent type
    agent_type = Column(
        SQLEnum(AgentType, name="agent_type", create_type=False),
        nullable=False
    )

    # Status
    status = Column(
        SQLEnum(AgentRunStatus, name="agent_run_status", create_type=False),
        default=AgentRunStatus.PENDING,
        nullable=False,
        index=True
    )

    # Input/Output data
    input_data = Column(JSONB)
    output_data = Column(JSONB)

    # Error handling
    error_message = Column(Text)

    # Timing
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    duration_ms = Column(Integer)

    # Resource usage
    tokens_used = Column(Integer)

    # Relationships
    campaign = relationship("Campaign", back_populates="agent_runs")

    @property
    def is_success(self) -> bool:
        """Check if agent run completed successfully."""
        return self.status == AgentRunStatus.COMPLETED

    def __repr__(self) -> str:
        return f"<AgentRun {self.agent_type.value} ({self.status.value})>"
