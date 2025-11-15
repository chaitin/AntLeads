"""Lead-related business models."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field


class ContactInfo(BaseModel):
    """Contact information for leads."""

    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class LeadSource(str, Enum):
    """Lead source enumeration."""

    WEB_FORM = "web_form"
    GOOGLE_ADS = "google_ads"
    META_ADS = "meta_ads"
    TIKTOK_ADS = "tiktok_ads"
    LANDING_PAGE = "landing_page"
    EVENT = "event"
    IMPORT = "import"
    REFERRAL = "referral"
    DIRECT = "direct"
    OTHER = "other"


class LeadStage(str, Enum):
    """Lead stage enumeration."""

    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class LeadPriority(str, Enum):
    """Lead priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Lead(BaseModel):
    """Lead business model."""

    id: Optional[UUID] = None
    name: str
    source: LeadSource
    stage: Optional[LeadStage] = LeadStage.NEW
    priority: Optional[LeadPriority] = LeadPriority.MEDIUM
    score: Optional[int] = 0
    contact_info: ContactInfo
    tags: list[str] = []
    product_interest: Optional[str] = None
    estimated_value: Optional[float] = None
    notes: Optional[str] = None

    # Source tracking
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    referrer_url: Optional[str] = None

    # Assignment
    assigned_to: Optional[UUID] = None

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    contacted_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None