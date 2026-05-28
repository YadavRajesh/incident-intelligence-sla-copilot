from fastapi.testclient import TestClient
from src.api.api import app

client = TestClient(app)

def test_analyze_incident():

    payload = {
        "incident_number": "INC200145",
        "short_description": "SAP production order creation failing after deployment",
        "description": "Users are unable to create sales orders in SAP production environment after the latest transport deployment.",
        "urgency": "1",
        "state": "Open",
        "opened_at": "2026-05-16 08:00:00",
        "sla_due": "2026-05-16 12:00:00",
        "assignment_group": "SAP Support",
        "business_service": "Order Management",
        "cmdb_ci": "SAP-PRD-01"
    }

    response = client.post("/analyze-incident", json=payload)

    assert response.status_code == 200

    response_json = response.json()

    assert response_json is not None