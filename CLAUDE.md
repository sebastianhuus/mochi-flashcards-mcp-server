# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides integration with Mochi flashcards. It allows Claude Desktop to interact with the Mochi API for managing flashcards and decks.

## Development Commands

Install dependencies:
```bash
uv sync
```

Run the server directly (for testing):
```bash
uv run python server.py
```

## Architecture

The project is built on FastMCP framework and consists of:

- `server.py`: Main MCP server implementation with 5 tools for Mochi API integration
- `pyproject.toml`: Python project configuration using uv for dependency management

### Core Components

**MCP Tools**: All tools use HTTP basic auth with the MOCHI_API_KEY
- `mochi_list_decks`: Lists user's decks with pagination support
- `mochi_create_card`: Creates cards with markdown content and optional tags
- `mochi_get_card`: Retrieves card details by ID
- `mochi_update_card`: Updates card content, deck assignment, archive status, or tags
- `mochi_delete_card`: Permanently deletes cards

**API Integration**: 
- Base URL: `https://app.mochi.cards/api`
- Authentication: HTTP Basic Auth with API key as username
- All requests use async httpx client with 30s timeout
- Error handling returns formatted error messages

## Configuration

The server requires `MOCHI_API_KEY` environment variable. When used with Claude Desktop, this is configured in the MCP servers section of `claude_desktop_config.json`.

## Key Implementation Details

- Single-file architecture in `server.py`
- Uses FastMCP decorator pattern for tool registration
- Centralized HTTP client in `make_mochi_request()` helper
- All tools return formatted strings for Claude consumption
- Supports optional parameters for flexible card management