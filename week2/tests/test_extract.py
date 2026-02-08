import os
import json
import pytest
from unittest.mock import patch, MagicMock

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# --- Unit tests for extract_action_items_llm() ---

def _mock_ollama_response(action_items: list[str]) -> MagicMock:
    """Helper to create a mock Ollama chat response with structured output."""
    mock_response = MagicMock()
    mock_response.message.content = json.dumps({"action_items": action_items})
    return mock_response


@patch("week2.app.services.extract.chat")
def test_llm_extract_bullet_list(mock_chat):
    """Test LLM extraction with bullet-list input."""
    mock_chat.return_value = _mock_ollama_response([
        "Buy groceries",
        "Fix the login bug",
    ])

    text = "- Buy groceries\n- Fix the login bug\nThe weather is nice."
    items = extract_action_items_llm(text)

    assert items == ["Buy groceries", "Fix the login bug"]
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_llm_extract_keyword_prefixed(mock_chat):
    """Test LLM extraction with keyword-prefixed lines (TODO, ACTION)."""
    mock_chat.return_value = _mock_ollama_response([
        "Write unit tests",
        "Review pull request",
    ])

    text = "TODO: Write unit tests\nACTION: Review pull request\nJust a regular note."
    items = extract_action_items_llm(text)

    assert items == ["Write unit tests", "Review pull request"]
    mock_chat.assert_called_once()


def test_llm_extract_empty_input():
    """Test LLM extraction with empty input returns empty list without calling Ollama."""
    # No need to mock — empty input should short-circuit before calling Ollama
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   ") == []
    assert extract_action_items_llm("\n\n") == []


@patch("week2.app.services.extract.chat")
def test_llm_extract_no_action_items(mock_chat):
    """Test LLM extraction when text contains no action items."""
    mock_chat.return_value = _mock_ollama_response([])

    text = "The meeting went well. Everyone was happy."
    items = extract_action_items_llm(text)

    assert items == []
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_llm_extract_mixed_content(mock_chat):
    """Test LLM extraction with mixed content (checkboxes, bullets, plain text)."""
    mock_chat.return_value = _mock_ollama_response([
        "Set up database",
        "Implement API endpoint",
        "Write tests",
    ])

    text = """Notes from meeting:
- [ ] Set up database
* Implement API endpoint
1. Write tests
Some narrative sentence."""
    items = extract_action_items_llm(text)

    assert len(items) == 3
    assert "Set up database" in items
    assert "Implement API endpoint" in items
    assert "Write tests" in items
