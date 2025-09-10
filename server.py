import os
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("mochi-cards")

MOCHI_API_BASE = "https://app.mochi.cards/api"
MOCHI_API_KEY = os.getenv("MOCHI_API_KEY")


async def make_mochi_request(
    url: str, method: str = "GET", data: dict = None
) -> dict[str, Any] | None:
    """Make a request to the Mochi API with proper error handling."""
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = (MOCHI_API_KEY, "") if MOCHI_API_KEY else None

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(
                    url, headers=headers, auth=auth, timeout=30.0
                )
            elif method == "POST":
                response = await client.post(
                    url, headers=headers, json=data, auth=auth, timeout=30.0
                )
            elif method == "DELETE":
                response = await client.delete(
                    url, headers=headers, auth=auth, timeout=30.0
                )

            response.raise_for_status()
            return response.json() if response.content else None
        except Exception as e:
            return {"error": str(e)}


@mcp.tool()
async def mochi_list_decks(bookmark: str = None) -> str:
    """List all decks in your Mochi account.

    Args:
        api_key: Your Mochi API key
        bookmark: Optional bookmark for pagination
    """
    url = f"{MOCHI_API_BASE}/decks"
    if bookmark:
        url += f"?bookmark={bookmark}"

    response = await make_mochi_request(url)

    if not response or "error" in response:
        return f"Error fetching decks: {response.get('error', 'Unknown error')}"

    decks = response.get("docs", [])
    result = "Your Mochi Decks:\n\n"

    for deck in decks:
        result += f"ID: {deck.get('id')}\nName: {deck.get('name')}\n\n"

    if response.get("bookmark"):
        result += f"\nMore decks available. Use bookmark: {response.get('bookmark')}"

    return result


@mcp.tool()
async def mochi_create_card(deck_id: str, content: str, tags: list = None) -> str:
    """Create a new card in a Mochi deck.

    Args:
        api_key: Your Mochi API key
        deck_id: The ID of the deck to add the card to
        content: Markdown content for the card
        tags: Optional list of tags to add to the card
    """
    url = f"{MOCHI_API_BASE}/cards"

    data = {"content": content, "deck-id": deck_id}

    if tags:
        data["manual-tags"] = tags

    response = await make_mochi_request(url, method="POST", data=data)

    if not response or "error" in response:
        return f"Error creating card: {response.get('error', 'Unknown error')}"

    return f"Card created successfully with ID: {response.get('id')}"


@mcp.tool()
async def mochi_get_card(card_id: str) -> str:
    """Get details of a specific Mochi card.

    Args:
        api_key: Your Mochi API key
        card_id: The ID of the card to retrieve
    """
    url = f"{MOCHI_API_BASE}/cards/{card_id}"

    response = await make_mochi_request(url)

    if not response or "error" in response:
        return f"Error fetching card: {response.get('error', 'Unknown error')}"

    result = f"Card ID: {response.get('id')}\n"
    result += f"Deck ID: {response.get('deck-id')}\n"
    result += f"Content: {response.get('content')}\n"
    result += f"Created: {response.get('created-at', {}).get('date')}\n"
    result += f"Updated: {response.get('updated-at', {}).get('date')}\n"

    if response.get("tags"):
        result += f"Tags: {', '.join(response.get('tags'))}\n"

    return result


@mcp.tool()
async def mochi_update_card(
    card_id: str,
    content: str = None,
    deck_id: str = None,
    archived: bool = None,
    tags: list = None,
) -> str:
    """Update an existing Mochi card.

    Args:
        api_key: Your Mochi API key
        card_id: The ID of the card to update
        content: Optional new markdown content
        deck_id: Optional new deck ID to move the card to
        archived: Optional boolean to archive/unarchive the card
        tags: Optional list of tags to replace existing tags
    """
    url = f"{MOCHI_API_BASE}/cards/{card_id}"

    data = {}
    if content is not None:
        data["content"] = content
    if deck_id is not None:
        data["deck-id"] = deck_id
    if archived is not None:
        data["archived?"] = archived
    if tags is not None:
        data["manual-tags"] = tags

    response = await make_mochi_request(
        url,
        method="POST",
        data=data,
    )

    if not response or "error" in response:
        return f"Error updating card: {response.get('error', 'Unknown error')}"

    return f"Card {card_id} updated successfully"


@mcp.tool()
async def mochi_delete_card(card_id: str) -> str:
    """Delete a Mochi card permanently.

    Args:
        api_key: Your Mochi API key
        card_id: The ID of the card to delete
    """
    url = f"{MOCHI_API_BASE}/cards/{card_id}"

    response = await make_mochi_request(url, method="DELETE")

    if response and "error" in response:
        return f"Error deleting card: {response.get('error')}"

    return f"Card {card_id} deleted successfully"


@mcp.tool()
async def mochi_list_cards(deck_id: str | None = None, limit: int = 10, bookmark: str | None = None) -> str:
    """List cards, optionally filtered by deck.

    Args:
        deck_id: Optional deck ID to filter cards by
        limit: Number of cards per page (1-100, default 10)
        bookmark: Optional bookmark for pagination
    """
    url = f"{MOCHI_API_BASE}/cards"
    params = []
    
    if deck_id:
        params.append(f"deck-id={deck_id}")
    if limit != 10:
        params.append(f"limit={limit}")
    if bookmark:
        params.append(f"bookmark={bookmark}")
    
    if params:
        url += "?" + "&".join(params)

    response = await make_mochi_request(url)

    if not response or "error" in response:
        return f"Error fetching cards: {response.get('error', 'Unknown error')}"

    cards = response.get("docs", [])
    result = f"Cards {'for deck ' + deck_id if deck_id else ''}:\n\n"

    for card in cards:
        result += f"ID: {card.get('id')}\n"
        result += f"Name: {card.get('name', 'Untitled')}\n"
        result += f"Deck ID: {card.get('deck-id')}\n"
        
        content = card.get('content', '')
        content_preview = content[:100] + '...' if len(content) > 100 else content
        result += f"Content: {content_preview}\n"
        
        if card.get('tags'):
            result += f"Tags: {', '.join(card.get('tags'))}\n"
        
        result += f"Created: {card.get('created-at', {}).get('date')}\n\n"

    if response.get("bookmark"):
        result += f"More cards available. Use bookmark: {response.get('bookmark')}"

    return result


if __name__ == "__main__":
    mcp.run(transport="stdio")
