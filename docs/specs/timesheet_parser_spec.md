# Spec: Timesheet Parser

This unit is responsible for parsing the `timesheets.md` file (implemented as markdown tables) into a structured internal representation designed to generate **Multi-Color Heatmap Visualizations**.

## Data Model (Pydantic)

```python
from pydantic import BaseModel
from typing import List, Optional

class TimesheetEntry(BaseModel):
    raw_date: Optional[str] = None  # HHMM:DD.MM.YYYY
    progress: Optional[str] = None  # e.g., "1.1.1 - (*) -> (d)"
    lessons: Optional[str] = None
    design: Optional[str] = None
    planned: Optional[str] = None
    comments: Optional[str] = None
```

## File Format (`timesheets.md`)

The format uses markdown tables with columns: `Date`, `Progress`, `Comments`, `Lessons`, `Design`, `Planned`.

```markdown
| Date | Progress | Comments | Lessons | Design | Planned |
| --- | --- | --- | --- | --- | --- |
| 2327:21./10/2025     | 1.1.1 - (*) -> (d)   |     |     |     | 1.1.2 - (a) -> (d) |
|                     | 1.1.2 - (d) -> (t)   |     |     |     | ... |
```

- **Date Field**: `HHMM:DD.MM.YYYY`.
- **No Inheritance**: Empty date cells remain `None`. The parser should capture the row exactly as it appears.
- **Progress/Planned Field**: Often contains `{task_id} - {state_transition}`.

## Behavioral Scenarios

### Scenario 1: Parse multi-column contributions
**Input**:
A row with content in `Progress`, `Lessons`, and `Design`.
**Expected Output**:
An entry with all corresponding fields populated. The heatmap engine will treat this as three different contribution points (potentially different colors).

### Scenario 2: Handle empty date cells
**Input**:
A row where the `Date` column is blank.
**Expected Output**:
`raw_date = None`. (Note: The visualization layer will need to decide how to handle these, e.g., associating them with the table's "session" or ignoring them if no date is found in the block).

### Scenario 3: Aggregation for Heatmap
The parser should provide a helper to extract "Contribution Points":
- Each non-blank `Progress` cell.
- Each non-blank `Lessons` cell.
- Each non-blank `Design` cell.
- Each non-blank `Planned` cell.

### Scenario 4: Ignore template tables
**Input**:
A table located under a `## Template` header or containing placeholder values (e.g., "format #.#.#").
**Expected Output**:
The parser should skip the entire template table.

### Scenario 5: Full File Integration
**Input**:
A file with headers, descriptive text, a template table, and multiple record tables (like `timesheets_example.md`).
**Expected Output**:
The parser should selectively extract only the meaningful rows from the record tables, ignoring noise and the template.

### Scenario 6: Ignore empty rows
**Input**:
A table row where all columns (Date, Progress, Comments, Lessons, Design, Planned) are blank or contain only whitespace.
**Expected Output**:
Skip the row.

### Scenario 7: Error Handling
- **Invalid Date Format**: Report raw string.
- **FileNotFound**: Raise `FileNotFoundError`.
