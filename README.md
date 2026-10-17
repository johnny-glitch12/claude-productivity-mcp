# Claude Productivity MCP Server

A lightweight local MCP server that gives Claude practical productivity tools.

## What it does

Claude can call these tools:
- `create_note` — Save a markdown note
- `list_notes` — List all notes
- `read_note` — Read a specific note
- `search_notes` — Search notes by keyword
- `add_todo` — Add a todo item
- `list_todos` — List todos
- `complete_todo` — Mark a todo as done
- `count_words` — Word / character count
- `slugify` — Turn text into a URL-friendly slug

All data is stored locally in a `data/` folder next to the server. No external APIs or accounts needed.

## Quick start

1. Clone this repo:
   ```bash
   git clone https://github.com/johnny-glitch12/claude-productivity-mcp.git
   cd claude-productivity-mcp
   ```

2. Install the MCP SDK:
   ```bash
   pip install "mcp[cli]"
   ```

3. Run the server (for testing):
   ```bash
   python server.py
   ```

## Connect to Claude Desktop

Add this to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "productivity": {
      "command": "python",
      "args": ["/full/path/to/claude-productivity-mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop. The tools should appear.

## Connect to Claude Code

```bash
claude mcp add productivity -- python /full/path/to/claude-productivity-mcp/server.py
```

## Example prompts for Claude

- "Create a note called Meeting Ideas with these bullet points..."
- "List my todos"
- "Search my notes for the word project"
- "Turn this title into a slug: My Cool Project Idea"

MIT License. Contributions welcome.
