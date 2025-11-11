"""Funnel and analytics schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from packages.core.models.lead import LeadStage


class FunnelStageData(BaseModel):
    """Data for a single funnel stage."""

    stage: LeadStage
    count: int
    total_value: float
    conversion_rate: Optional[float] = None  # Percentage to next stage
    average_days: Optional[float] = None  # Average days in this stage


class FunnelResponse(BaseModel):
    """Response schema for sales funnel visualization."""

    stages: list[FunnelStageData]
    total_leads: int
    total_value: float
    overall_conversion_rate: float  # NEW -> WON
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None


class ConversionMetrics(BaseModel):
    """Lead conversion metrics."""

    stage: LeadStage
    leads_entered: int
    leads_advanced: int
    leads_stalled: int
    average_time_in_stage_days: float
    conversion_rate: float
