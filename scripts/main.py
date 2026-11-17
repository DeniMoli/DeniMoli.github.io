#!/usr/bin/env python3
"""
Blog post automation pipeline.

Usage:
    python scripts/main.py [--config scripts/config.yaml]

Environment:
    Set pipeline.dry_run: true in config.yaml to test without committing.
"""
import argparse
import logging
import os
import sys
from pathlib import Path

import yaml

SCRIPTS_DIR = Path(__file__).parent
REPO_ROOT = SCRIPTS_DIR.parent
BLOGS_DIR = REPO_ROOT / "content" / "blogs"
STATE_FILE = str(SCRIPTS_DIR / "processed.json")

# Add scripts/ to path so relative imports work when run from repo root
sys.path.insert(0, str(SCRIPTS_DIR))

from converter import build_post_file
from fetcher import fetch_all_sources
from publisher import PublishError, get_next_post_number, git_commit_and_push, write_post
from scraper import ScrapeError, scrape_article
from state import load_state, mark_processed, save_state


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def run(config_path: str) -> None:
    config = load_config(config_path)
    state = load_state(STATE_FILE)
    dry_run = config["pipeline"]["dry_run"]

    if dry_run:
        logging.info("=== DRY RUN MODE — no git operations will be performed ===")

    candidates = fetch_all_sources(config, state)
    if not candidates:
        logging.info("No new relevant articles found.")
        return

    logging.info(f"Processing {len(candidates)} article(s)...")

    for candidate in candidates:
        logging.info(f"--- Processing: {candidate.title}")
        try:
            scraped = scrape_article(candidate, config)
            next_num = get_next_post_number(str(BLOGS_DIR))
            post_file = build_post_file(scraped, candidate, next_num, config)
            output_path = write_post(post_file, str(BLOGS_DIR))

            rel_output = os.path.relpath(output_path, str(REPO_ROOT))
            files_to_add = post_file.files_to_add + [rel_output]

            git_commit_and_push(
                str(REPO_ROOT),
                files_to_add,
                scraped.title,
                dry_run,
            )

            mark_processed(candidate.url, scraped.title, post_file.filename, state)
            save_state(state, STATE_FILE)
            logging.info(f"Done: {post_file.filename}")

        except ScrapeError as e:
            logging.warning(f"Skipping '{candidate.title}': {e}")
            # Continue to next article

        except PublishError as e:
            logging.error(f"Git error for '{candidate.title}': {e}")
            break  # Git failure is unrecoverable — stop the run


def main() -> None:
    setup_logging()
    parser = argparse.ArgumentParser(description="Blog automation pipeline")
    parser.add_argument(
        "--config",
        default=str(SCRIPTS_DIR / "config.yaml"),
        help="Path to config.yaml",
    )
    args = parser.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
