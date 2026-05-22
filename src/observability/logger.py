import json
from datetime import datetime


LOG_FILE = (
    "data/logs/workflow_execution.jsonl"
)


def log_workflow_execution(payload):

    payload["timestamp"] = (
        datetime.now().isoformat()
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(payload)
            + "\n"
        )