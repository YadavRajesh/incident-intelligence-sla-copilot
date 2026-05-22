from datetime import datetime

from dateutil import parser

from src.graph.state import (
    IncidentState
)

ACTIVE_STATUSES = {
    "open",
    "assigned",
    "work in progress",
    "awaiting user info"
}


URGENCY_MAP = {
    "1 - high": "HIGH",
    "1": "HIGH",
    "high": "HIGH",

    "2 - medium": "MEDIUM",
    "2": "MEDIUM",
    "medium": "MEDIUM",

    "3 - low": "LOW",
    "3": "LOW",
    "low": "LOW",
}


def sla_analysis_node(
    state: IncidentState
) -> IncidentState:

    current_status = str(
        state.get("state", "")
    ).strip().lower()

    # Skip inactive incidents
    if current_status not in ACTIVE_STATUSES:

        state["progress_pct"] = 0.0
        state["alert_type"] = "NONE"

        state["processing_logs"].append(
            "Incident inactive. SLA skipped."
        )

        return state

    try:

        opened_at = parser.parse(
            str(state["opened_at"]),
            dayfirst=True
        )

        sla_due = parser.parse(
            str(state["sla_due"]),
            dayfirst=True
        )

    except Exception:

        state["processing_logs"].append(
            "SLA date parsing failed"
        )

        return state

    now = datetime.now()

    total_seconds = (
        sla_due - opened_at
    ).total_seconds()

    elapsed_seconds = (
        now - opened_at
    ).total_seconds()

    remaining_seconds = (
        sla_due - now
    ).total_seconds()

    # SLA progress calculation
    if total_seconds <= 0:

        progress_pct = 100.0

    else:

        progress_pct = max(
            0.0,
            min(
                100.0,
                (elapsed_seconds / total_seconds)
                * 100
            )
        )

    urgency_raw = str(
        state.get("urgency", "")
    ).strip().lower()

    urgency = URGENCY_MAP.get(
        urgency_raw,
        "UNKNOWN"
    )

    # Alert classification
    alert_type = "NONE"

    if urgency == "HIGH" and progress_pct >= 30:

        alert_type = "ESCALATION"

    elif progress_pct >= 60:

        alert_type = "WARNING"

    # Update shared state
    state["progress_pct"] = round(
        progress_pct,
        2
    )

    state["sla_total_hours"] = round(
        total_seconds / 3600,
        2
    )

    state["sla_elapsed_hours"] = round(
        elapsed_seconds / 3600,
        2
    )

    state["sla_remaining_hours"] = round(
        remaining_seconds / 3600,
        2
    )

    state["alert_type"] = alert_type

    # Observability
    state["execution_path"].append(
        "sla_analysis_node"
    )

    state["processing_logs"].append(
        f"SLA analysis completed. "
        f"Alert type: {alert_type}"
    )

    return state