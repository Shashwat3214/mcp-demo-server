# server.py — MCP server with Pydantic output schemas

from typing import List, Dict
from pydantic import BaseModel, Field
from fastmcp import FastMCP
from mock_data import EVENTS, COURSES, ENGAGEMENT, ACCOUNT_NEWS

mcp = FastMCP("HyTechPro Demo MCP Server")


# ---------- Output schemas ----------
class EventItem(BaseModel):
    name: str = Field(description="Event name")
    date: str = Field(description="Event date YYYY-MM-DD")
    type: str = Field(description="Event type")


class CourseItem(BaseModel):
    name: str = Field(description="Course name")
    completed_date: str = Field(description="Completion date YYYY-MM-DD")
    credits: int = Field(description="Credits earned")


class EngagementData(BaseModel):
    email_opens_last_30_days: int = Field(description="Email opens in last 30 days")
    site_visits_last_30_days: int = Field(description="Site visits in last 30 days")
    last_interaction: str = Field(description="Last interaction date or 'unknown'")
    engagement_score: str = Field(description="high, medium, low, or no_data")


class NewsItem(BaseModel):
    headline: str = Field(description="News headline")
    source: str = Field(description="News source")
    date: str = Field(description="Publication date YYYY-MM-DD")


class EventsResponse(BaseModel):
    email: str = Field(description="Member email")
    events: List[EventItem] = Field(description="Events attended")
    count: int = Field(description="Number of events")


class CoursesResponse(BaseModel):
    email: str = Field(description="Member email")
    courses: List[CourseItem] = Field(description="Completed courses")
    total_credits: int = Field(description="Total credits")
    count: int = Field(description="Number of courses")


class EngagementMetricsResponse(BaseModel):
    members: Dict[str, EngagementData] = Field(description="Engagement keyed by email")
    count: int = Field(description="Number of members")


class MemberSummaryResponse(BaseModel):
    email: str = Field(description="Member email")
    events_attended: List[EventItem] = Field(description="Events attended")
    events_count: int = Field(description="Total events")
    courses_completed: List[CourseItem] = Field(description="Courses completed")
    courses_count: int = Field(description="Total courses")
    total_credits: int = Field(description="Total credits earned")
    engagement: EngagementData = Field(description="Engagement metrics")


class AccountNewsResponse(BaseModel):
    news: Dict[str, List[NewsItem]] = Field(description="News keyed by account")
    accounts_checked: int = Field(description="Accounts checked")


# ---------- Tools ----------
@mcp.tool()
def get_events_attended(email: str, year: int | None = None) -> EventsResponse:
    """Retrieves the list of events a member has attended.
    Use when a user asks about event history or what events they attended.
    Args:
        email: The member's email address (required).
        year: Optional. Filters events to that year (e.g., 2026).
    """
    member_events = EVENTS.get(email, [])
    if year is not None:
        member_events = [e for e in member_events if e["date"].startswith(str(year))]
    return EventsResponse(email=email, events=[EventItem(**e) for e in member_events], count=len(member_events))


@mcp.tool()
def get_courses_completed(email: str) -> CoursesResponse:
    """Retrieves courses a member completed and credits earned.
    Use when a user asks about learning history, courses, or credits.
    Args:
        email: The member's email address (required).
    """
    mc = COURSES.get(email, [])
    return CoursesResponse(email=email, courses=[CourseItem(**c) for c in mc],
                           total_credits=sum(c["credits"] for c in mc), count=len(mc))


@mcp.tool()
def get_engagement_metrics(emails: List[str]) -> EngagementMetricsResponse:
    """Retrieves engagement metrics for a list of members.
    Args:
        emails: A list of member email addresses.
    """
    default = EngagementData(email_opens_last_30_days=0, site_visits_last_30_days=0,
                             last_interaction="unknown", engagement_score="no_data")
    result = {e: (EngagementData(**ENGAGEMENT[e]) if e in ENGAGEMENT else default) for e in emails}
    return EngagementMetricsResponse(members=result, count=len(result))


@mcp.tool()
def get_member_engagement_summary(email: str) -> MemberSummaryResponse:
    """Comprehensive engagement summary for a member in one call:
    events, courses, credits, and engagement. Preferred for renewals/reviews.
    Args:
        email: The member's email address (required).
    """
    events = EVENTS.get(email, [])
    courses = COURSES.get(email, [])
    eng = ENGAGEMENT.get(email, {"email_opens_last_30_days": 0, "site_visits_last_30_days": 0,
                                 "last_interaction": "unknown", "engagement_score": "no_data"})
    return MemberSummaryResponse(
        email=email,
        events_attended=[EventItem(**e) for e in events], events_count=len(events),
        courses_completed=[CourseItem(**c) for c in courses], courses_count=len(courses),
        total_credits=sum(c["credits"] for c in courses),
        engagement=EngagementData(**eng),
    )


@mcp.tool()
def get_account_news(account_names: List[str]) -> AccountNewsResponse:
    """Retrieves recent news mentions for a list of company accounts.
    Args:
        account_names: A list of company / account names.
    """
    result = {a: [NewsItem(**n) for n in ACCOUNT_NEWS.get(a, [])] for a in account_names}
    return AccountNewsResponse(news=result, accounts_checked=len(account_names))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)