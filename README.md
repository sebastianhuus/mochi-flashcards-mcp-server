# Mochi Flashcards MCP Server

## Setup

Install dependencies:
```bash
uv sync
```

You don't need to run the server unless you will interface with it directly. Claude Desktop is capable of hosting it by itself.

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

## Available Tools

* **`mochi_list_decks`** - List all decks in your account (with optional pagination)
* **`mochi_list_cards`** - List cards, optionally filtered by deck ID (with pagination and configurable limit)
* **`mochi_create_card`** - Create a new card in a specific deck with content and optional tags
* **`mochi_get_card`** - Get details of a specific card by its ID
* **`mochi_update_card`** - Update card content, move between decks, or archive/unarchive cards
* **`mochi_delete_card`** - Permanently delete a card by its ID
* **`mochi_search_cards_by_tags`** - Search cards by tags with flexible filtering (any, all, exclude, deck, case sensitivity). Finds cards with manual or content-based tags. (Client-side filtering, may be slow for large collections)
* **`mochi_list_all_tags`** - List all unique tags across your cards, optionally scoped to a deck. Can include usage counts for each tag.
* **`mochi_analyze_card_tags`** - Analyze a card's tags to show which come from content hashtags vs manual tags. Explains how to remove each type.
* **`mochi_remove_content_tags`** - Remove tags from a card by editing its content to remove hashtags. Updates the card content accordingly.
- **`mochi_list_decks`** - List all decks in your account (with optional pagination)
- **`mochi_list_cards`** - List cards, optionally filtered by deck ID (with pagination and configurable limit)
- **`mochi_create_card`** - Create a new card in a specific deck with content and optional tags
- **`mochi_get_card`** - Get details of a specific card by its ID
- **`mochi_update_card`** - Update card content, move between decks, or archive/unarchive cards
- **`mochi_delete_card`** - Permanently delete a card by its ID

# Credits
Kudos to [d42me](https://github.com/d42me/mochi-flashcards-mcp-server) for the original repo this was forked from. It was a bit inactive so I did my own spin on this
