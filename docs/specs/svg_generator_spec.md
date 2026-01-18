# Spec: SVG Generator

The `SVGGenerator` takes structured data from the `RoadmapParser` (and eventually the `TimesheetParser`) and produces an SVG file representing project health.

## Requirement Traceability
- **Source**: `docs/roadmap/ROADMAP.md` -> **1.3 SVG Generator**
- **Unit**: `SVGGenerator`

## Visual Design

- **Canvas**: 800x (height based on EPIC count)
- **Grid Type**: Epic Swimlanes.
    - Each **EPIC** (Level 1 task) occupies a horizontal "Swimlane".
    - Each lane has a label on the left (Description).
    - **Atomic Tasks** (Subtasks/Bugs) within that Epic are rendered as colored squares in the lane.
    - Tasks are arranged horizontally within the lane, sorted by status (Planned -> Design -> Lessons -> Progress).
- **Categories (4 colors)**:
    - `DONE` -> `#2ea44f` (Progress)
    - `ANALYSIS` -> `#0969da` (Lessons)
    - `DEVELOPMENT`/`TESTING` -> `#dbab09` (Design/Implementation)
    - `TODO` -> `#8b949e` (Planned)

## Behavioral Scenarios

### Scenario 1: Empty Roadmap (Edge Case)
**Input**: `[]` (Empty list of tasks)
**Expected Output**: 
- A valid SVG string.
- No task rectangles.
- Text: "No Roadmap Data available" at the center.

### Scenario 2: EPIC Swimlane Rendering (Happy Path)
**Input**: 
- Epic A (contains Subtask 1 [DONE], Subtask 2 [TODO])
- Epic B (contains Subtask 3 [ANALYSIS])
**Expected Output**: 
- 2 horizontal "lanes" with labels "Epic A" and "Epic B".
- Lane A contains 2 squares (Green, Grey).
- Lane B contains 1 square (Blue).

### Scenario 3: Mixed Statuses in Swimlane (Happy Path)
**Input**: Epic with `DEVELOPMENT` and `TESTING` tasks.
**Expected Output**: The lane contains yellow squares for both development and testing statuses, fulfilling the "Design/Implementation" category.

### Scenario 4: Legend Rendering (Happy Path)
**Input**: Any task list.
**Expected Output**: A bottom section showing all 4 status colors with their corresponding labels (Progress, Lessons, Design, Planned).

## Data Schema (SVG Elements)
- `<svg>` wrapper with `xmlns="http://www.w3.org/2000/svg"`
- `<rect>` elements for the heatmap squares.
- `<text>` elements for labels and the legend.
