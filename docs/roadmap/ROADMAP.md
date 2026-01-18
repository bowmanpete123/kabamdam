# Project Roadmap

The goal of `kabamdam` is to provide a "Status as Code" workflow. It parses a project's `Roadmap.md` (kanban) and `timesheets.md` (diary/log) to generate a visual SVG status indicator suitable for embedding in a `README.md`. It is designed to be run as a dev dependency, likely via a pre-commit hook.

## Work In Progress

- (d) 1. Core Engine
    - (/) 1.1 Roadmap Parser
        - (/) 1.1.1 Parse GFM task lists from `Roadmap.md`
        - (/) 1.1.2 Map task status to internal data structure
        - (/) 1.1.3 Distinguish Subtasks vs Bugs (hierarchical classification)
    - (/) 1.2 Timesheet Parser
        - (/) 1.2.1 Parse log entries from `timesheets.md`
        - (/) 1.2.2 Extract timestamps and activity labels
    - (/) 1.3 SVG Generator
        - (/) 1.3.1 Design SVG Heatmap (4 colors: Progress, Lessons, Design, Planned)
        - (/) 1.3.2 Implement Bug Icons in status list
        - (/) 1.3.3 Render parsed data into SVG template
- (/) 2. Tooling & Integration
    - (/) 2.1 CLI Interface ("Wrap up" command)
        - (/) 2.1.1 Implement pipeline: parse -> render -> inject README sections
        - (/) 2.1.2 Include "drill-down" links to Roadmap and Timesheets in README
    - (*) 2.2 Pre-commit Hook
        - (*) 2.2.1 Create `.pre-commit-hooks.yaml` config

## Further Requirements

- **Enhanced Visuals**:
    - Gantt Chart Rendering
    - Custom Color Palettes
- **External Sync**:
    - GitHub Issues Integration

## Scope Creep

- **Web Dashboard**:
- **AI Roadmap Prediction**: