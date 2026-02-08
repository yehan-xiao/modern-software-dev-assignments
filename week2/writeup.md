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
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 