"""Widget business models."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Widget(BaseModel):
    """Widget business model."""

    id: Optional[UUID] = None
    name: str = Field(..., min_length=1, max_length=100)
    widget_id: str
    api_key: str

    # Form configuration
    title: str = Field(default="Get in Touch", max_length=200)
    description: Optional[str] = None
    submit_button_text: str = Field(default="Submit", max_length=50)
    success_message: str = Field(default="Thank you! We'll be in touch soon.")

    # Fields configuration (list of field definitions)
    fields: list[dict] = Field(default_factory=list)

    # Styling
    primary_color: str = Field(default="#3b82f6", pattern="^#[0-9A-Fa-f]{6}$")
    button_position: str = Field(default="bottom-right", max_length=20)

    # Behavior
    auto_open: bool = False
    auto_open_delay: int = Field(default=5, ge=0)

    # Metadata
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True
