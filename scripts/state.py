import json
import os
import tempfile
from datetime import datetime, timezone


def load_state(state_file: str) -> dict:
    if not os.path.exists(state_file):
        return {"processed": []}
    with open(state_file, "r", encoding="utf-8") as f:
        return json.load(f)


def is_duplicate(url: str, state: dict) -> bool:
    processed_urls = {entry["url"] for entry in state.get("processed", [])}
    return url in processed_urls


def mark_processed(url: str, title: str, output_file: str, state: dict) -> None:
    state.setdefault("processed", []).append({
        "url": url,
        "title": title,
        "output_file": output_file,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    })


def save_state(state: dict, state_file: str) -> None:
    dir_name = os.path.dirname(state_file) or "."
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False,
                                     suffix=".tmp", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        tmp_path = f.name
    os.replace(tmp_path, state_file)
