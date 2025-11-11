"""AI scoring and tagging service."""
from typing import List

from packages.core.models.lead import ContactInfo, Lead, LeadPriority, LeadSource


class LeadScorer:
    """AI-powered lead scoring engine."""

    def __init__(self):
        """Initialize the scorer with weights."""
        self.source_weights = {
            LeadSource.GOOGLE_ADS: 15,
            LeadSource.META_ADS: 12,
            LeadSource.TIKTOK_ADS: 10,
            LeadSource.LANDING_PAGE: 18,
            LeadSource.WEB_FORM: 20,
            LeadSource.EVENT: 25,
            LeadSource.IMPORT: 5,
            LeadSource.REFERRAL: 30,
            LeadSource.DIRECT: 15,
            LeadSource.OTHER: 5,
        }

    def calculate_score(self, lead: Lead) -> int:
        """Calculate lead score based on various factors."""
        score = 0

        # Source quality (0-30 points)
        score += self.source_weights.get(lead.source, 5)

        # Contact completeness (0-25 points)
        score += self._score_contact_info(lead.contact_info)

        # Estimated value (0-20 points)
        if lead.estimated_value:
            if lead.estimated_value >= 100000:
                score += 20
            elif lead.estimated_value >= 50000:
                score += 15
            elif lead.estimated_value >= 10000:
                score += 10
            else:
                score += 5

        # Product interest (0-10 points)
        if lead.product_interest:
            score += 10

        # UTM tracking (0-10 points)
        if lead.utm_campaign:
            score += 5
        if lead.utm_source:
            score += 3
        if lead.utm_medium:
            score += 2

        # Company info (0-5 points)
        if lead.contact_info.company:
            score += 5

        return min(score, 100)  # Cap at 100

    def _score_contact_info(self, contact: ContactInfo) -> int:
        """Score contact information completeness."""
        score = 0

        if contact.email:
            score += 10
        if contact.phone:
            score += 8
        if contact.company:
            score += 5
        if contact.title:
            score += 2

        return min(score, 25)

    def suggest_tags(self, lead: Lead) -> List[str]:
        """AI-powered tag suggestions based on lead attributes."""
        tags = []

        # Value-based tags
        if lead.estimated_value:
            if lead.estimated_value >= 100000:
                tags.append("enterprise")
            elif lead.estimated_value >= 50000:
                tags.append("mid-market")
            else:
                tags.append("smb")

        # Score-based tags
        if lead.score >= 75:
            tags.append("hot-lead")
        elif lead.score >= 50:
            tags.append("warm-lead")
        else:
            tags.append("cold-lead")

        # Source-based tags
        if lead.source in [LeadSource.REFERRAL, LeadSource.EVENT]:
            tags.append("high-quality")

        if lead.source in [LeadSource.GOOGLE_ADS, LeadSource.META_ADS, LeadSource.TIKTOK_ADS]:
            tags.append("paid-traffic")

        # Contact completeness
        if (lead.contact_info.email and lead.contact_info.phone and
            lead.contact_info.company and lead.contact_info.title):
            tags.append("complete-profile")

        # Product interest
        if lead.product_interest:
            if "enterprise" in lead.product_interest.lower():
                tags.append("enterprise-interest")
            if "demo" in lead.product_interest.lower():
                tags.append("demo-request")

        return tags

    def suggest_priority(self, lead: Lead) -> LeadPriority:
        """Suggest priority based on lead score."""
        if lead.score >= 80:
            return LeadPriority.URGENT
        elif lead.score >= 60:
            return LeadPriority.HIGH
        elif lead.score >= 40:
            return LeadPriority.MEDIUM
        else:
            return LeadPriority.LOW


# Global scorer instance
scorer = LeadScorer()


def score_lead(lead: Lead) -> int:
    """Score a lead."""
    return scorer.calculate_score(lead)


def auto_tag_lead(lead: Lead) -> List[str]:
    """Generate automatic tags for a lead."""
    return scorer.suggest_tags(lead)


def suggest_lead_priority(lead: Lead) -> LeadPriority:
    """Suggest priority for a lead."""
    return scorer.suggest_priority(lead)
