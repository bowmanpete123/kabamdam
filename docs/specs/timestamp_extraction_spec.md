# Spec: Timestamp & Label Extraction

This requirement focuses on transforming the raw strings captured in 1.2.1 into structured Python objects for the `TimesheetEntry`.

## Data Model Updates

The `TimesheetEntry` model will be updated to include validated fields:

```python
from datetime import datetime
from typing import Optional

class TimesheetEntry(BaseModel):
    # Raw fields (kept for reference)
    raw_date: Optional[str] = None
    progress: Optional[str] = None
    
    # Extracted fields
    timestamp: Optional[datetime] = None
    task_id: Optional[str] = None
    from_status: Optional[str] = None
    to_status: Optional[str] = None
```

## Extraction Rules

### 1. Date & Time Extraction
**Regex**: `(?P<hour>\d{2})(?P<minute>\d{2}):(?P<day>\d{2})[./](?P<month>\d{2})[./](?P<year>\d{4})`
- Example: `2327:21./10/2025` or `1630:13.12.2025`.
- Should handle both `.` and `/` as separators.

### 2. Progress/Activity Extraction
**Regex**: `(?P<id>[\d\.]+)\s*(?:-)?\s*(?:\((?P<from>.)\))?\s*->\s*(?:\((?P<to>.)\))?`
- Example: `1.4.1- (*) -> (d)`
- `task_id` = "1.4.1"
- `from_status` = "*"
- `to_status` = "d"

## Behavioral Scenarios

### Scenario 1: Parse full timestamp
**Input**: `2327:21./10/2025`
**Expected Output**: `datetime(2025, 10, 21, 23, 27)`

### Scenario 2: Parse transition
**Input**: `1.4.1- (d) -> (t)`
**Expected Output**: `task_id="1.4.1"`, `from_status="d"`, `to_status="t"`

### Scenario 3: Optional components
**Input**: `1.4.3 - (d) -> (t)` (note the space before hyphen)
**Expected Output**: Correct extraction.

### Scenario 4: Error Handling
- If a `raw_date` or `progress` string is present but fails to match the required regex, the parser **MUST raise a ValueError**.
- Silent failure with `None` is forbidden to prevent invalid data in the heatmap.
