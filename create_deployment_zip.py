import zipfile
import os

ZIP_NAME = "deployment.zip"

EXCLUDE = {
    "venv",
    ".git",
    ".vscode",
    "__pycache__"
}

with zipfile.ZipFile(
    ZIP_NAME,
    "w",
    zipfile.ZIP_DEFLATED
) as zipf:

    for root, dirs, files in os.walk("."):

        dirs[:] = [
            d for d in dirs
            if d not in EXCLUDE
        ]

        for file in files:

            if file == ZIP_NAME:
                continue

            filepath = os.path.join(root, file)

            arcname = os.path.relpath(
                filepath,
                "."
            )

            zipf.write(
                filepath,
                arcname.replace("\\", "/")
            )

print("deployment.zip created successfully")