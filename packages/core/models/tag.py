"""Lead tag business models."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class LeadTag(BaseModel):
    """Lead tag business model."""

    id: Optional[UUID] = None
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#6B7280", pattern="^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = None
    created_at: Optional[datetime] = None
