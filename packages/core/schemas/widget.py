"""Widget API schemas."""
from typing import Optional

from pydantic import BaseModel, Field


class WidgetCreateRequest(BaseModel):
    """Request schema for creating a widget."""

    name: str = Field(..., min_length=1, max_length=100)
    title: str = Field(default="Get in Touch")
    description: Optional[str] = Field(default="Fill out the form below and we'll get back to you soon.")
    submit_button_text: str = Field(default="Submit")
    success_message: str = Field(default="Thank you! We'll be in touch soon.")
    fields: list[str] = Field(default=["name", "email", "phone", "company", "message"])
    primary_color: str = Field(default="#3b82f6")
    button_position: str = Field(default="bottom-right")
    auto_open: bool = Field(default=False)
    auto_open_delay: int = Field(default=5)


class WidgetUpdateRequest(BaseModel):
    """Request schema for updating a widget."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = None
    description: Optional[str] = None
    submit_button_text: Optional[str] = None
    success_message: Optional[str] = None
    fields: Optional[list[str]] = None
    primary_color: Optional[str] = None
    button_position: Optional[str] = None
    auto_open: Optional[bool] = None
    auto_open_delay: Optional[int] = None
    is_active: Optional[bool] = None


class WidgetFormSubmission(BaseModel):
    """Form data submitted from widget."""

    widget_id: str = Field(..., description="Public widget ID")
    name: str = Field(..., min_length=1)
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    message: Optional[str] = None
    url: Optional[str] = Field(None, description="URL where form was submitted")
    referrer: Optional[str] = None


class WidgetConfigResponse(BaseModel):
    """Public widget configuration (without sensitive data)."""

    widget_id: str
    title: str
    description: Optional[str]
    submit_button_text: str
    success_message: str
    fields: list[str]
    primary_color: str
    button_position: str
    auto_open: bool
    auto_open_delay: int
