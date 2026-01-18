# Implementation Plan: SVG Heatmap (1.3.1)

The goal is to create a visual heatmap of project progress. This will be implemented in a data-oriented way, separating the SVG generation logic from the task data.

## Proposed Changes

- **`src/kabamdam/svg_generator.py`**: New class `SVGGenerator` for rendering the task list into an SVG grid.
- **`docs/specs/svg_generator_spec.md`**: Behavioral requirements and color mappings.

## Architectural Notes
- Use `Pydantic` for SVG configuration (colors, dimensions).
- Pure functions for calculating grid coordinates.
- Colors mapped to local work categories as per `ROADMAP.md`.
