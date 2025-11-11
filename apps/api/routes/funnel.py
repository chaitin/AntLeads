"""Funnel analytics API endpoints."""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.database import get_db
from apps.api.models import LeadORM
from packages.core.models.lead import LeadStage
from packages.core.schemas.funnel import FunnelResponse, FunnelStageData

router = APIRouter()


@router.get("/", response_model=FunnelResponse)
async def get_funnel(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Get sales funnel data with conversion metrics."""
    # Build base query
    query = select(
        LeadORM.stage,
        func.count(LeadORM.id).label("count"),
        func.coalesce(func.sum(LeadORM.estimated_value), 0).label("total_value"),
    ).group_by(LeadORM.stage)

    # Apply date filters
    if start_date:
        query = query.where(LeadORM.created_at >= start_date)
    if end_date:
        query = query.where(LeadORM.created_at <= end_date)

    result = await db.execute(query)
    stage_data = {stage: (count, total_value) for stage, count, total_value in result.all()}

    # Calculate metrics for each stage
    stages = []
    stage_order = [
        LeadStage.NEW,
        LeadStage.CONTACTED,
        LeadStage.QUALIFIED,
        LeadStage.PROPOSAL,
        LeadStage.NEGOTIATION,
        LeadStage.WON,
        LeadStage.LOST,
    ]

    total_leads = sum(count for count, _ in stage_data.values())
    total_value = sum(value for _, value in stage_data.values())

    for idx, stage in enumerate(stage_order):
        count, value = stage_data.get(stage, (0, 0))

        # Calculate conversion rate to next stage
        conversion_rate = None
        if idx < len(stage_order) - 1 and count > 0:
            next_stage = stage_order[idx + 1]
            next_count, _ = stage_data.get(next_stage, (0, 0))
            conversion_rate = (next_count / count) * 100 if count > 0 else 0

        stages.append(
            FunnelStageData(
                stage=stage,
                count=count,
                total_value=float(value),
                conversion_rate=conversion_rate,
                average_days=None,  # Would need additional tracking to calculate
            )
        )

    # Overall conversion rate (NEW -> WON)
    new_count, _ = stage_data.get(LeadStage.NEW, (0, 0))
    won_count, _ = stage_data.get(LeadStage.WON, (0, 0))
    overall_conversion = (won_count / new_count * 100) if new_count > 0 else 0

    return FunnelResponse(
        stages=stages,
        total_leads=total_leads,
        total_value=float(total_value),
        overall_conversion_rate=overall_conversion,
        period_start=start_date,
        period_end=end_date,
    )
