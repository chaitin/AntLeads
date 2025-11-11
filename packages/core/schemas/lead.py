"""Lead API schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from packages.core.models.lead import ContactInfo, LeadPriority, LeadSource, LeadStage


class LeadCreateRequest(BaseModel):
    """Request schema for creating a new lead."""

    name: str = Field(..., min_length=1, max_length=200)
    source: LeadSource
    contact_info: ContactInfo = Field(default_factory=ContactInfo)
    tags: list[str] = Field(default_factory=list)
    product_interest: Optional[str] = None
    estimated_value: Optional[float] = Field(default=None, ge=0)
    notes: Optional[str] = None

    # Source tracking
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    referrer_url: Optional[str] = None


class LeadUpdateRequest(BaseModel):
    """Request schema for updating a lead."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    stage: Optional[LeadStage] = None
    priority: Optional[LeadPriority] = None
    contact_info: Optional[ContactInfo] = None
    tags: Optional[list[str]] = None
    product_interest: Optional[str] = None
    estimated_value: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None
    assigned_to: Optional[UUID] = None


class LeadResponse(BaseModel):
    """Response schema for lead data."""

    id: UUID
    name: str
    source: LeadSource
    stage: LeadStage
    priority: LeadPriority
    score: int
    contact_info: ContactInfo
    tags: list[str]
    product_interest: Optional[str]
    estimated_value: Optional[float]
    notes: Optional[str]
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    referrer_url: Optional[str]
    assigned_to: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    contacted_at: Optional[datetime]
    closed_at: Optional[datetime]


class LeadListResponse(BaseModel):
    """Response schema for paginated lead list."""

    leads: list[LeadResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class LeadImportRequest(BaseModel):
    """Request schema for bulk lead import."""

    leads: list[LeadCreateRequest] = Field(..., min_length=1, max_length=1000)
    source: LeadSource = LeadSource.IMPORT


class LeadImportResponse(BaseModel):
    """Response schema for bulk import result."""

    total: int
    successful: int
    failed: int
    errors: list[dict] = Field(default_factory=list)


class LeadStatsResponse(BaseModel):
    """Response schema for lead statistics."""

    total_leads: int
    by_stage: dict[str, int]
    by_source: dict[str, int]
    by_priority: dict[str, int]
    average_score: float
    total_estimated_value: float
