# mock_data.py
# Mock data for the demo MCP server.
# In production this would be replaced with real API calls (Cvent, Coursera, etc.).

# ============================================================
# EVENTS — events a member attended
# ============================================================
EVENTS = {
    # --- Real Salesforce contact: Shashwat Vaish (demo star) ---
    "shashwat.vaish@hytechpro.com": [
        {"name": "Annual Summit 2026", "date": "2026-03-15", "type": "Conference"},
        {"name": "Spring Leadership Workshop", "date": "2026-04-22", "type": "Workshop"},
        {"name": "Tech Networking Night", "date": "2026-05-10", "type": "Networking"},
    ],
    # --- Original demo emails ---
    "alice@example.com": [
        {"name": "Annual Summit 2026", "date": "2026-03-15", "type": "Conference"},
        {"name": "Spring Workshop", "date": "2026-04-22", "type": "Workshop"},
        {"name": "Tech Networking", "date": "2026-05-10", "type": "Networking"},
    ],
    "bob@example.com": [
        {"name": "Annual Summit 2026", "date": "2026-03-15", "type": "Conference"},
        {"name": "Leadership Forum", "date": "2026-02-18", "type": "Forum"},
    ],
    "carol@example.com": [
        {"name": "Annual Summit 2025", "date": "2025-03-20", "type": "Conference"},
    ],
}

# ============================================================
# COURSES — courses a member completed
# ============================================================
COURSES = {
    "shashwat.vaish@hytechpro.com": [
        {"name": "Foundations of Industry", "completed_date": "2025-11-10", "credits": 5},
        {"name": "Advanced Skills Workshop", "completed_date": "2026-01-22", "credits": 8},
        {"name": "Leadership Essentials", "completed_date": "2026-04-05", "credits": 6},
    ],
    "alice@example.com": [
        {"name": "Foundations of Industry", "completed_date": "2025-11-10", "credits": 5},
        {"name": "Advanced Skills Workshop", "completed_date": "2026-01-22", "credits": 8},
        {"name": "Leadership Essentials", "completed_date": "2026-04-05", "credits": 6},
    ],
    "bob@example.com": [
        {"name": "Foundations of Industry", "completed_date": "2025-12-15", "credits": 5},
    ],
    "carol@example.com": [],  # No courses completed
}

# ============================================================
# ENGAGEMENT METRICS
# ============================================================
ENGAGEMENT = {
    "shashwat.vaish@hytechpro.com": {
        "email_opens_last_30_days": 14,
        "site_visits_last_30_days": 9,
        "last_interaction": "2026-06-12",
        "engagement_score": "high",
    },
    "alice@example.com": {
        "email_opens_last_30_days": 12,
        "site_visits_last_30_days": 8,
        "last_interaction": "2026-06-10",
        "engagement_score": "high",
    },
    "bob@example.com": {
        "email_opens_last_30_days": 4,
        "site_visits_last_30_days": 2,
        "last_interaction": "2026-05-28",
        "engagement_score": "medium",
    },
    "carol@example.com": {
        "email_opens_last_30_days": 0,
        "site_visits_last_30_days": 0,
        "last_interaction": "2024-11-15",
        "engagement_score": "low",
    },
    "david@example.com": {
        "email_opens_last_30_days": 8,
        "site_visits_last_30_days": 5,
        "last_interaction": "2026-06-08",
        "engagement_score": "high",
    },
}

# ============================================================
# ACCOUNT NEWS — for sales/employee agent use case
# ============================================================
ACCOUNT_NEWS = {
    "Acme Corp": [
        {"headline": "Acme Corp announces $20M Series B funding", "source": "TechCrunch", "date": "2026-06-12"},
        {"headline": "Acme Corp expands into European market", "source": "Bloomberg", "date": "2026-05-30"},
    ],
    "Globex Inc": [
        {"headline": "Globex Inc partners with major retailer", "source": "Reuters", "date": "2026-06-08"},
    ],
    "Initech": [],  # No recent news
}