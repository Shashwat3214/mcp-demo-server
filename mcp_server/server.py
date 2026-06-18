# server.py
# MCP server using FastMCP. Exposes tools Agentforce can call.

from fastmcp import FastMCP
from mock_data import EVENTS, COURSES, ENGAGEMENT, ACCOUNT_NEWS

# The name Agentforce will see for this server.
mcp = FastMCP("HyTechPro Demo MCP Server")


# ============================================================
# TOOL 1 — Get events attended by a member
# ============================================================
@mcp.tool()
def get_events_attended(email: str, year: int = None) -> dict:
    """
    Retrieves the list of events a member has attended.

    Use this tool when a user asks about their event history, what events
    they attended, or for event-related summaries.

    Args:
        email: The member's email address (required).
        year: Optional. If provided, filters events to only that year (e.g., 2026).

    Returns:
        A dictionary with member email and list of events with name, date, and type.
    """
    member_events = EVENTS.get(email, [])
    if year is not None:
        member_events = [e for e in member_events if e["date"].startswith(str(year))]
    return {
        "email": email,
        "events": member_events,
        "count": len(member_events),
    }


# ============================================================
# TOOL 2 — Get courses completed by a member
# ============================================================
@mcp.tool()
def get_courses_completed(email: str) -> dict:
    """
    Retrieves the list of courses a member has completed, along with credits earned.

    Use this tool when a user asks about their learning history, what courses
    they've taken, certification progress, or continuing education credits.

    Args:
        email: The member's email address (required).

    Returns:
        A dictionary with member email, list of courses, total credits earned,
        and the count of completed courses.
    """
    member_courses = COURSES.get(email, [])
    total_credits = sum(course["credits"] for course in member_courses)
    return {
        "email": email,
        "courses": member_courses,
        "total_credits": total_credits,
        "count": len(member_courses),
    }


# ============================================================
# TOOL 3 — Get engagement metrics for multiple members
# ============================================================
@mcp.tool()
def get_engagement_metrics(emails: list) -> dict:
    """
    Retrieves engagement metrics (email opens, site visits, last interaction)
    for a list of members. Useful for prioritizing outreach to lapsed or
    inactive members.

    Use this tool when staff want to prioritize who to contact, identify
    re-engagement opportunities, or analyze member activity patterns.

    Args:
        emails: A list of member email addresses.

    Returns:
        A dictionary with engagement metrics keyed by email, including
        email opens, site visits, last interaction date, and an overall
        engagement score (high/medium/low).
    """
    result = {}
    for email in emails:
        if email in ENGAGEMENT:
            result[email] = ENGAGEMENT[email]
        else:
            result[email] = {
                "email_opens_last_30_days": 0,
                "site_visits_last_30_days": 0,
                "last_interaction": "unknown",
                "engagement_score": "no_data",
            }
    return {"members": result, "count": len(result)}


# ============================================================
# TOOL 4 — Composite tool: full member engagement summary
# ============================================================
# This is the IMPORTANT tool for the demo. It combines data from
# multiple sources into one response. This is what shows MCP's strength
# over multiple separate API calls.
@mcp.tool()
def get_member_engagement_summary(email: str) -> dict:
    """
    Provides a comprehensive engagement summary for a single member, combining
    their event history, course completions, and engagement metrics into one
    unified response.

    This is the preferred tool for renewal conversations, account reviews,
    and any scenario where you need a complete picture of a member's activity.

    Args:
        email: The member's email address (required).

    Returns:
        A unified summary with events attended, courses completed, total credits,
        and engagement metrics.
    """
    events = EVENTS.get(email, [])
    courses = COURSES.get(email, [])
    engagement = ENGAGEMENT.get(email, {
        "email_opens_last_30_days": 0,
        "site_visits_last_30_days": 0,
        "last_interaction": "unknown",
        "engagement_score": "no_data",
    })
    total_credits = sum(course["credits"] for course in courses)
    return {
        "email": email,
        "events_attended": events,
        "events_count": len(events),
        "courses_completed": courses,
        "courses_count": len(courses),
        "total_credits": total_credits,
        "engagement": engagement,
    }


# ============================================================
# TOOL 5 — Get news mentions for a list of company accounts
# ============================================================
@mcp.tool()
def get_account_news(account_names: list) -> dict:
    """
    Retrieves recent news mentions for a list of company accounts.
    Useful for sales reps preparing for outreach or account reviews.

    Use this tool when a sales rep asks about recent activity, news, or
    relevant developments for their accounts.

    Args:
        account_names: A list of company / account names to look up.

    Returns:
        A dictionary keyed by account name with recent news headlines,
        sources, and dates.
    """
    result = {}
    for account in account_names:
        result[account] = ACCOUNT_NEWS.get(account, [])
    return {"news": result, "accounts_checked": len(account_names)}


# ============================================================
# START THE SERVER
# ============================================================
if __name__ == "__main__":
    import os
    # Render sets the PORT env variable; fall back to 8000 for local testing.
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)