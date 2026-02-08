# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt:
```
Analyze the existing extract_action_items() function in week2/app/services/extract.py. Implement an LLM-powered alternative, extract_action_items_llm(), that uses Ollama to extract action items via a large language model. Use structured outputs (Pydantic model + JSON schema) to ensure the LLM returns a well-formatted JSON response. Use the llama3.1:8b model. Handle edge cases like empty input.
```

Generated Code Snippets:
```
week2/app/services/extract.py: lines 6, 8, 68-99
- Line 6: Added `from pydantic import BaseModel` import
- Line 8: Already had `from ollama import chat`
- Lines 68-70: Added `ActionItems` Pydantic model defining the structured output schema
- Lines 73-99: Added `extract_action_items_llm()` function that calls Ollama with structured JSON output and parses the response using Pydantic validation
```

### Exercise 2: Add Unit Tests
Prompt:
```
Write unit tests for extract_action_items_llm() in week2/tests/test_extract.py covering multiple inputs: bullet lists, keyword-prefixed lines (TODO, ACTION), empty input, no action items, and mixed content. Use unittest.mock.patch to mock the Ollama chat call so tests run fast and deterministically.
```

Generated Code Snippets:
```
week2/tests/test_extract.py: lines 3-5, 28-97
- Lines 3-5: Added imports for json, unittest.mock (patch, MagicMock), and extract_action_items_llm
- Lines 28-33: Helper function _mock_ollama_response() to create mock Ollama responses
- Lines 36-46: test_llm_extract_bullet_list — tests bullet list input
- Lines 49-59: test_llm_extract_keyword_prefixed — tests keyword-prefixed lines (TODO, ACTION)
- Lines 62-66: test_llm_extract_empty_input — tests empty/whitespace input without calling Ollama
- Lines 69-77: test_llm_extract_no_action_items — tests text with no action items
- Lines 80-97: test_llm_extract_mixed_content — tests mixed content (checkboxes, bullets, plain text)
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt:
```
Refactor the backend code focusing on: (1) well-defined API contracts/schemas — replace all Dict[str, Any] request/response types with Pydantic BaseModel classes for automatic validation and API documentation; (2) app lifecycle — move init_db() from module-level side effect to FastAPI lifespan context manager so the database initializes on server startup rather than on import; (3) fix a bug in the mark_done endpoint where bool("false") evaluates to True due to Python truthy semantics; (4) error handling — add try/except around database and extraction operations in write endpoints to return clear 500 error messages instead of unhandled exceptions.
```

Generated/Modified Code Snippets:
```
week2/app/routers/notes.py: lines 6, 13-19, 25-29, 32-37
- Line 6: Added `from pydantic import BaseModel`
- Lines 13-14: Added CreateNoteRequest schema (content: str)
- Lines 16-19: Added NoteResponse schema (id, content, created_at)
- Lines 25-31: Refactored create_note() to use CreateNoteRequest input and NoteResponse output, removing manual validation; added try/except error handling for database operations
- Lines 34-39: Refactored get_single_note() to use NoteResponse output

week2/app/routers/action_items.py: lines 3, 6, 14-38, 44-53, 56-59
- Line 3: Cleaned up imports (removed unused Any, Dict, List)
- Line 6: Added `from pydantic import BaseModel`
- Lines 14-16: Added ExtractRequest schema (text: str, save_note: bool = False)
- Lines 18-20: Added ActionItemOut schema (id, text)
- Lines 22-24: Added ExtractResponse schema (note_id, items)
- Lines 26-31: Added ActionItemDetail schema (id, note_id, text, done, created_at)
- Lines 33-34: Added MarkDoneRequest schema (done: bool = True) — fixes bug where "false" string was treated as True
- Lines 36-38: Added MarkDoneResponse schema (id, done)
- Lines 44-57: Refactored extract() to use Pydantic models; added try/except error handling for extraction and database operations
- Lines 60-69: Refactored list_all() to use Pydantic models
- Lines 72-78: Refactored mark_done() to use MarkDoneRequest/MarkDoneResponse; added try/except error handling

week2/app/main.py: lines 3, 14-18, 20
- Line 3: Added `from contextlib import asynccontextmanager`
- Lines 14-18: Added lifespan context manager wrapping init_db()
- Line 20: Passed lifespan to FastAPI constructor
- Removed unused imports (Any, Dict, Optional, HTTPException, db)
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt:
```
Part 1: Integrate the LLM-powered extraction as a new endpoint. Add a POST /action-items/extract-llm route that calls extract_action_items_llm() with the same request/response schema as the existing /extract endpoint. Update the frontend to add an "Extract LLM" button that triggers extraction via the new endpoint.

Part 2: Expose a GET /notes endpoint to retrieve all saved notes. Add a "List Notes" button to the frontend that fetches and displays them.
```

Generated Code Snippets:
```
week2/app/routers/action_items.py: lines 9, 61-75
- Line 9: Added extract_action_items_llm to the import
- Lines 61-75: Added POST /action-items/extract-llm endpoint that calls extract_action_items_llm(), reusing ExtractRequest/ExtractResponse schemas

week2/app/routers/notes.py: lines 35-41
- Lines 35-41: Added GET /notes endpoint (list_notes) that calls db.list_notes() and returns List[NoteResponse]

week2/frontend/index.html: lines 27-28, 32, 73-107, 109-129
- Line 27: Added "Extract LLM" button
- Line 28: Added "List Notes" button
- Line 32: Added <div id="notes"> container for displaying notes
- Lines 73-107: JavaScript handler for "Extract LLM" button — POSTs to /action-items/extract-llm and renders action item checkboxes
- Lines 109-129: JavaScript handler for "List Notes" button — GETs /notes and displays each note with ID, timestamp, and content
```


### Exercise 5: Generate a README from the Codebase
Prompt:
```
Analyze the current week2 codebase — including main.py, routers, services, db.py, tests, and pyproject.toml — and generate a well-structured README.md. Include: a brief project overview, setup and run instructions (conda, poetry, Ollama), a table of all API endpoints with methods and descriptions, and instructions for running the test suite.
```

Generated Code Snippets:
```
week2/README.md: entire file (new)
- Generated a complete README covering project overview, prerequisites, installation steps, how to run the server, API endpoint tables (Notes, Action Items, Frontend), and test instructions.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 