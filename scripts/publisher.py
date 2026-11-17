import logging
import os
import re
import subprocess

from converter import BlogPostFile

logger = logging.getLogger(__name__)


class PublishError(Exception):
    pass


def get_next_post_number(blogs_dir: str) -> int:
    try:
        files = os.listdir(blogs_dir)
    except FileNotFoundError:
        return 1
    numbers = []
    for f in files:
        m = re.match(r"^(\d+)\.", f)
        if m:
            numbers.append(int(m.group(1)))
    return max(numbers) + 1 if numbers else 1


def write_post(post_file: BlogPostFile, blogs_dir: str) -> str:
    base_slug = re.sub(r"^\d+\. (.+)\.md$", r"\1", post_file.filename)
    num = int(re.match(r"^(\d+)\.", post_file.filename).group(1))

    slug = base_slug
    suffix = 2
    while os.path.exists(os.path.join(blogs_dir, f"{num}. {slug}.md")):
        slug = f"{base_slug}-{suffix}"
        suffix += 1

    filename = f"{num}. {slug}.md"
    output_path = os.path.join(blogs_dir, filename)
    content = post_file.frontmatter + "\n\n" + post_file.body + "\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"Written: {output_path}")
    return output_path


def git_commit_and_push(
    repo_root: str,
    files: list[str],
    title: str,
    dry_run: bool,
) -> None:
    if dry_run:
        logger.info(f"DRY RUN: would commit {len(files)} file(s) with message: auto: add post '{title}'")
        for f in files:
            logger.info(f"  - {f}")
        return

    commit_message = f"auto: add post '{title}'"

    def run(cmd: list[str]) -> None:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise PublishError(
                f"Command failed: {' '.join(cmd)}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )
        if result.stdout.strip():
            logger.debug(result.stdout.strip())

    run(["git", "-C", repo_root, "add"] + files)
    run(["git", "-C", repo_root, "commit", "-m", commit_message])
    run(["git", "-C", repo_root, "push", "origin", "master"])
    logger.info(f"Pushed commit: {commit_message}")
