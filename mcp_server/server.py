# server.py
# MCP server using FastMCP with Pydantic output schemas
# so Salesforce Agentforce can introspect each tool's outputs.

from typing import List, Dict
from pydantic import BaseModel, Field
from fastmcp import FastMCP
from mock_data import EVENTS, COURSES, ENGAGEMENT, ACCOUNT_NEWS

mcp = FastMCP("HyTechPro Demo MCP Server")


# ============================================================
# OUTPUT SCHEMAS (Pydantic models)
# These let Agentforce see each tool's output structure.
# ============================================================

class EventItem(BaseModel):
    name: str = Field(description="Event name")
    date: str = Field(description="Event date in YYYY-MM-DD")
    type: str = Field(description="Event type (Conference, Workshop, etc.)")


class CourseItem(BaseModel):
    name: str = Field(description="Course name")
    completed_date: str = Field(description="Completion date in YYYY-MM-DD")
    credits: int = Field(description="Credits earned for this course")


class EngagementData(BaseModel):
    email_opens_last_30_days: int = Field(description="Email opens in last 30 days")
    site_visits_last_30_days: int = Field(description="Site visits in last 30 days")
    last_interaction: str = Field(description="Date of last interaction or 'unknown'")
    engagement_score: str = Field(description="high, medium, low, or no_data")


class NewsItem(BaseModel):
    headline: str = Field(description="News headline")
    source: str = Field(description="News source publication")
    date: str = Field(description="Publication date YYYY-MM-DD")


class EventsResponse(BaseModel):
    email: str = Field(description="Member email looked up")
    events: List[EventItem] = Field(description="List of events attended")
    count: int = Field(description="Number of events")


class CoursesResponse(BaseModel):
    email: str = Field(description="Member email looked up")
    courses: List[CourseItem] = Field(description="List of completed courses")
    total_credits: int = Field(description="Sum of credits across all courses")
    count: int = Field(description="Number of courses")


class EngagementMetricsResponse(BaseModel):
    members: Dict[str, EngagementData] = Field(description="Engagement keyed by email")
    count: int = Field(description="Number of members looked up")


class MemberSummaryResponse(BaseModel):
    email: str = Field(description="Member email")
    events_attended: List[EventItem] = Field(description="All events attended")
    events_count: int = Field(description="Total events attended")
    courses_completed: List[CourseItem] = Field(description="All courses completed")
    courses_count: int = Field(description="Total courses completed")
    total_credits: int = Field(description="Sum of all credits earned")
    engagement: EngagementData = Field(description="Engagement metrics")


class AccountNewsResponse(BaseModel):
    news: Dict[str, List[NewsItem]] = Field(description="News items keyed by account name")
    accounts_checked: int = Field(description="Number of accounts checked")


# ============================================================
# TOOL 1 — Events attended
# ============================================================
@mcp.tool()
def get_events_attended(email: str, year: int | None = None) -> EventsResponse:
    """
    Retrieves the list of events a member has attended.

    Use this tool when a user asks about their event history, what events
    they attended, or for event-related summaries.

    Args:
        email: The member's email address (required).
        year: Optional. If provided, filters events to only that year (e.g., 2026).
    """
    member_events = EVENTS.get(email, [])
    if year is not None:
        member_events = [e for e in member_events if e["date"].startswith(str(year))]
    return EventsResponse(
        email=email,
        events=[EventItem(**e) for e in member_events],
        count=len(member_events),
    )


# ============================================================
# TOOL 2 — Courses completed
# ============================================================
@mcp.tool()
def get_courses_completed(email: str) -> CoursesResponse:
    """
    Retrieves the list of courses a member has completed and credits earned.

    Use this tool when a user asks about their learning history, courses,
    certifications, or continuing education credits.

    Args:
        email: The member's email address (required).
    """
    member_courses = COURSES.get(email, [])
    total = sum(c["credits"] for c in member_courses)
    return CoursesResponse(
        email=email,
        courses=[CourseItem(**c) for c in member_courses],
        total_credits=total,
        count=len(member_courses),
    )


# ============================================================
# TOOL 3 — Engagement metrics for multiple members
# ============================================================
@mcp.tool()
def get_engagement_metrics(emails: List[str]) -> EngagementMetricsResponse:
    """
    Retrieves engagement metrics (email opens, site visits, last interaction)
    for a list of members. Useful for prioritizing outreach to lapsed members.

    Args:
        emails: A list of member email addresses.
    """
    result = {}
    default = EngagementData(
        email_opens_last_30_days=0,
        site_visits_last_30_days=0,
        last_interaction="unknown",
        engagement_score="no_data",
    )
    for email in emails:
        if email in ENGAGEMENT:
            result[email] = EngagementData(**ENGAGEMENT[email])
        else:
            result[email] = default
    return EngagementMetricsResponse(members=result, count=len(result))


# ============================================================
# TOOL 4 — Composite: member engagement summary
# ============================================================
@mcp.tool()
def get_member_engagement_summary(email: str) -> MemberSummaryResponse:
    """
    Provides a comprehensive engagement summary for a member in one call:
    events attended, courses completed, credits, and engagement metrics.

    This is the preferred tool for renewal conversations and account reviews —
    it combines multiple data sources into a single response.

    Args:
        email: The member's email address (required).
    """
    events = EVENTS.get(email, [])
    courses = COURSES.get(email, [])
    eng = ENGAGEMENT.get(email, {
        "email_opens_last_30_days": 0,
        "site_visits_last_30_days": 0,
        "last_interaction": "unknown",
        "engagement_score": "no_data",
    })
    return MemberSummaryResponse(
        email=email,
        events_attended=[EventItem(**e) for e in events],
        events_count=len(events),
        courses_completed=[CourseItem(**c) for c in courses],
        courses_count=len(courses),
        total_credits=sum(c["credits"] for c in courses),
        engagement=EngagementData(**eng),
    )


# ============================================================
# TOOL 5 — Account news
# ============================================================
@mcp.tool()
def get_account_news(account_names: List[str]) -> AccountNewsResponse:
    """
    Retrieves recent news mentions for a list of company accounts.
    Useful for sales reps preparing for outreach or account reviews.

    Args:
        account_names: A list of company / account names.
    """
    result = {}
    for account in account_names:
        items = ACCOUNT_NEWS.get(account, [])
        result[account] = [NewsItem(**n) for n in items]
    return AccountNewsResponse(news=result, accounts_checked=len(account_names))


# ============================================================
# START THE SERVER
# ============================================================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)