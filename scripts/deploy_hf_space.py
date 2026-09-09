#!/usr/bin/env python3
"""Create/update the permanent Hugging Face Space for MOLE-AI."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from huggingface_hub import HfApi, whoami

ROOT = Path(__file__).resolve().parents[1]
SPACE_NAME = "MOLE-AI"
INCLUDE = [
    "v2_app.py",
    "requirements.txt",
    "mole_ai",
    "assets",
    "data",
    "LICENSE",
]


def main() -> None:
    user = whoami()["name"]
    repo_id = f"{user}/{SPACE_NAME}"
    api = HfApi()

    api.create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="streamlit",
        exist_ok=True,
        private=False,
    )

    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "space"
        dest.mkdir()

        shutil.copy2(ROOT / "SPACE_README.md", dest / "README.md")
        for item in INCLUDE:
            src = ROOT / item
            target = dest / item
            if src.is_dir():
                shutil.copytree(
                    src,
                    target,
                    ignore=shutil.ignore_patterns(
                        "__pycache__",
                        "*.pyc",
                        "*.save",
                        "app_*backup*.py",
                        "app_before_*.py",
                        "app_phase*.py",
                    ),
                )
            elif src.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)

        # Ensure package inits exist for HF packaging
        for pkg in [
            "mole_ai/agents",
            "mole_ai/workflows",
            "mole_ai/ranking",
            "mole_ai/reports",
        ]:
            init = dest / pkg / "__init__.py"
            init.parent.mkdir(parents=True, exist_ok=True)
            init.touch(exist_ok=True)

        api.upload_folder(
            folder_path=str(dest),
            repo_id=repo_id,
            repo_type="space",
            commit_message="Deploy MOLE-AI v2 to Hugging Face Spaces",
        )

    url = f"https://huggingface.co/spaces/{repo_id}"
    app_url = f"https://{user.lower().replace('_', '-')}-{SPACE_NAME.lower()}.hf.space"
    print(f"SPACE_URL={url}")
    print(f"APP_HINT={app_url}")


if __name__ == "__main__":
    main()
