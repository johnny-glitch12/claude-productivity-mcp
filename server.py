#!/usr/bin/env python3
"""Productivity MCP server for Claude."""
from pathlib import Path
import json
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("productivity")

DATA_DIR = Path(__file__).parent / "data"
NOTES_DIR = DATA_DIR / "notes"
TODOS_FILE = DATA_DIR / "todos.json"

def ensure_dirs():
    DATA_DIR.mkdir(exist_ok=True)
    NOTES_DIR.mkdir(exist_ok=True)
    if not TODOS_FILE.exists():
        TODOS_FILE.write_text("[]")

@mcp.tool()
def create_note(title: str, content: str) -> str:
    """Create a new markdown note. Title becomes the filename."""
    ensure_dirs()
    slug = title.lower().replace(" ", "-").replace("/", "-")[:80]
    path = NOTES_DIR / f"{slug}.md"
    if path.exists():
        return f"Note already exists: {slug}"
    text = f"# {title}\n\nCreated: {datetime.now().isoformat()}\n\n{content}\n"
    path.write_text(text)
    return f"Created note: {slug}"

@mcp.tool()
def list_notes() -> list[str]:
    """List all note titles."""
    ensure_dirs()
    return sorted([p.stem for p in NOTES_DIR.glob("*.md")])

@mcp.tool()
def read_note(title: str) -> str:
    """Read the full content of a note by its title/slug."""
    ensure_dirs()
    slug = title.lower().replace(" ", "-")
    path = NOTES_DIR / f"{slug}.md"
    if not path.exists():
        return f"Note not found: {title}"
    return path.read_text()

@mcp.tool()
def search_notes(query: str) -> list[str]:
    """Search note titles and content for a keyword."""
    ensure_dirs()
    query = query.lower()
    results = []
    for path in NOTES_DIR.glob("*.md"):
        text = path.read_text().lower()
        if query in text or query in path.stem.lower():
            results.append(path.stem)
    return results

@mcp.tool()
def add_todo(task: str) -> str:
    """Add a new todo item."""
    ensure_dirs()
    todos = json.loads(TODOS_FILE.read_text())
    todos.append({"task": task, "done": False, "created": datetime.now().isoformat()})
    TODOS_FILE.write_text(json.dumps(todos, indent=2))
    return f"Added todo: {task}"

@mcp.tool()
def list_todos() -> list[dict]:
    """List all todos."""
    ensure_dirs()
    return json.loads(TODOS_FILE.read_text())

@mcp.tool()
def complete_todo(task: str) -> str:
    """Mark a todo as done by matching the task text."""
    ensure_dirs()
    todos = json.loads(TODOS_FILE.read_text())
    for t in todos:
        if t["task"].lower() == task.lower() and not t["done"]:
            t["done"] = True
            TODOS_FILE.write_text(json.dumps(todos, indent=2))
            return f"Completed: {task}"
    return f"Todo not found or already done: {task}"

@mcp.tool()
def count_words(text: str) -> dict:
    """Return word count and character count for the given text."""
    words = len(text.split())
    chars = len(text)
    return {"words": words, "characters": chars}

@mcp.tool()
def slugify(text: str) -> str:
    """Convert text into a URL-friendly slug."""
    return text.lower().replace(" ", "-").replace("/", "-").strip("-")

if __name__ == "__main__":
    mcp.run(transport="stdio")
