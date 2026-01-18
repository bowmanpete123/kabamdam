# Spec: Status Mapping

This requirement focuses on refining the internal representation of task statuses to align with the project's **RoadMap SOP** (`roadmapinfo.md`).

## Proposed Status Schema

We will replace the simple `Literal` status with a formal **Python Enum** to provide better structure and allow for sub-states within the "DOING" phase.

### Status Enum

```python
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "TODO"          # (*)
    ANALYSIS = "ANALYSIS"   # (a)
    DEVELOPMENT = "DEVELOPMENT" # (d)
    TESTING = "TESTING"     # (t)
    DONE = "DONE"          # (/)
```

### Mapping Logic

The parser will map characters as follows:
- `*` -> `TaskStatus.TODO`
- `a` -> `TaskStatus.ANALYSIS`
- `d` -> `TaskStatus.DEVELOPMENT`
- `t` -> `TaskStatus.TESTING`
- `/` -> `TaskStatus.DONE`
- ` ` (empty) -> `TaskStatus.TODO` (Default)

## Behavioral Scenarios

### Scenario 1: Detailed Status Extraction
**Input**:
```markdown
- (a) 1. Analysis Task
- (t) 2. Testing Task
```
**Expected Output**:
- Task 1: `status=TaskStatus.ANALYSIS`
- Task 2: `status=TaskStatus.TESTING`

### Scenario 2: High-Level Grouping
The `RoadmapTask` model should provide a helper property (e.g., `high_level_status`) that maps:
- `ANALYSIS`, `DEVELOPMENT`, `TESTING` -> `"DOING"`
- `TODO` -> `"TODO"`
- `DONE` -> `"DONE"`

This ensures compatibility with the SVG generator while keeping the internal data rich.

### Scenario 3: Validation
Invalid codes (if any) should default to `TODO` or raise a validation error depending on strictness. Given the SOP, we should be strict or have a fallback.
