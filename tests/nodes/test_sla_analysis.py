from src.graph.nodes.sla_analysis import sla_analysis_node


def test_sla_analysis_warning():

    state = {
        "state": "Open",
        "opened_at": "2026-05-16 08:00:00",
        "sla_due": "2026-05-16 12:00:00",
        "urgency": "2",
        "processing_logs": [],
        "execution_path": []
    }

    result = sla_analysis_node(state)

    assert result["alert_type"] in ["WARNING", "ESCALATION", "NONE"]

    assert "progress_pct" in result

    assert "sla_analysis_node" in result["execution_path"]