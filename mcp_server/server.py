# server.py — DIAGNOSTIC: dict returns (no output schema), int|None kept

from typing import List
from fastmcp import FastMCP
from mock_data import EVENTS, COURSES, ENGAGEMENT, ACCOUNT_NEWS

mcp = FastMCP("HyTechPro Demo MCP Server")


@mcp.tool()
def get_events_attended(email: str, year: int | None = None) -> dict:
    """Retrieves the list of events a member has attended.
    Use when a user asks about event history or what events they attended.
    Args:
        email: The member's email address (required).
        year: Optional. Filters events to that year (e.g., 2026).
    """
    member_events = EVENTS.get(email, [])
    if year is not None:
        member_events = [e for e in member_events if e["date"].startswith(str(year))]
    return {"email": email, "events": member_events, "count": len(member_events)}


@mcp.tool()
def get_courses_completed(email: str) -> dict:
    """Retrieves courses a member completed and credits earned.
    Use when a user asks about learning history, courses, or credits.
    Args:
        email: The member's email address (required).
    """
    member_courses = COURSES.get(email, [])
    total = sum(c["credits"] for c in member_courses)
    return {"email": email, "courses": member_courses, "total_credits": total, "count": len(member_courses)}


@mcp.tool()
def get_engagement_metrics(emails: List[str]) -> dict:
    """Retrieves engagement metrics for a list of members.
    Args:
        emails: A list of member email addresses.
    """
    result = {}
    for email in emails:
        result[email] = ENGAGEMENT.get(email, {
            "email_opens_last_30_days": 0,
            "site_visits_last_30_days": 0,
            "last_interaction": "unknown",
            "engagement_score": "no_data",
        })
    return {"members": result, "count": len(result)}


@mcp.tool()
def get_member_engagement_summary(email: str) -> dict:
    """Comprehensive engagement summary for a member in one call:
    events, courses, credits, and engagement. Preferred for renewals/reviews.
    Args:
        email: The member's email address (required).
    """
    events = EVENTS.get(email, [])
    courses = COURSES.get(email, [])
    eng = ENGAGEMENT.get(email, {
        "email_opens_last_30_days": 0, "site_visits_last_30_days": 0,
        "last_interaction": "unknown", "engagement_score": "no_data",
    })
    return {
        "email": email,
        "events_attended": events, "events_count": len(events),
        "courses_completed": courses, "courses_count": len(courses),
        "total_credits": sum(c["credits"] for c in courses),
        "engagement": eng,
    }


@mcp.tool()
def get_account_news(account_names: List[str]) -> dict:
    """Retrieves recent news mentions for a list of company accounts.
    Args:
        account_names: A list of company / account names.
    """
    result = {}
    for account in account_names:
        result[account] = ACCOUNT_NEWS.get(account, [])
    return {"news": result, "accounts_checked": len(account_names)}


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)