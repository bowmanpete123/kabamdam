# Spec: Roadmap Parser

This unit is responsible for parsing the `Roadmap.md` file into a structured internal representation using **Pydantic** for validation.

## Data Model (Pydantic)

```python
from pydantic import BaseModel
from typing import List, Optional, Literal

## Data Model (Pydantic)

```python
from pydantic import BaseModel
from typing import List, Optional, Literal

class RoadmapTask(BaseModel):
    id: str
    description: str
    status: TaskStatus  # Enum defined in 1.1.2
    type: Literal["EPIC", "STORY", "SUBTASK", "BUG"]
    subtasks: List["RoadmapTask"] = []
    level: int 
```

### Type Classification Rules
- **EPIC**: Level 1 (Top-level items, usually 0 indentation).
- **STORY**: Level 2 (Direct children of an EPIC).
- **SUBTASK**: Level 3 (Direct children of a STORY).
- **BUG**: Level 4 (Indented under a SUBTASK).

## Behavioral Scenarios

### Scenario 1: Parse 4-level nesting
**Input**:
Indentation levels representing Level 1, 2, 3, and 4 items.
**Expected Output**:
- A Level 4 item should have `type = "BUG"`.
- A Level 3 item should have `type = "SUBTASK"`.
- A Level 2 item should have `type = "STORY"`.
- A Level 1 item should have `type = "EPIC"`.

### Scenario 2: Parse a simple task list with status mapping
**Input**:
```markdown
- (*) 1. Task A
- (d) 2. Task B
- (/) 3. Task C
```
**Expected Output**:
- `id="1", status="TODO"`
- `id="2", status="DOING"`
- `id="3", status="DONE"`

### Scenario 2: Parse nested hierarchy (3 tiers)
**Input**:
```markdown
- (d) 1. Epic
    - (d) 1.1 Story
        - (*) 1.1.1 Subtask
```
**Expected Output**:
Hierarchical structure where "Subtask" is in `Story.subtasks`, and "Story" is in `Epic.subtasks`.

### Scenario 3: Support specialized status codes
**Input**:
- `(a)` Analysis -> `DOING`
- `(t)` Testing -> `DOING`

### Scenario 4: Error Handling
- **Missing Status**: Default to `TODO` if a list item starts with `- [ ]` or `- ` but no code.
- **Malformed ID**: Parser should attempt to extract ID if present (e.g., `1.1.1`), otherwise generate one or treat it as description.
- **FileNotFound**: Raise `FileNotFoundError`.

### Scenario 5: Ignore noise
- Headers (`# ...`), comments, and plain paragraphs should be skipped unless they are part of a task list.
