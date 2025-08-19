# Mochi Flashcards MCP Server

## Setup

Install dependencies:
```bash
uv sync
```

### Claude Desktop

1. Get your Mochi API key from your "Account settings" in the Mochi app.

2. Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "mochi-flashcards": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "/path/to/mochi-flashcards-mcp-server",
           "python",
           "server.py"
         ],
         "env": {
           "MOCHI_API_KEY": "your_api_key_here"
         }
       }
     }
   }
   ```

3. Replace `/path/to/mochi-flashcards-mcp-server` with actual path and add your API key

4. Restart Claude Desktop