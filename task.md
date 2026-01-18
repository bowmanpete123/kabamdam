# Task: SVG Heatmap (1.3.1)

**Requirement**: Design and implement a visual SVG Heatmap that represents project task statuses across different categories (Progress, Lessons, Design, Planned).

## Micro-Plan (Architect)

### Unit: SVGGenerator
- **Target Source File**: `src/kabamdam/svg_generator.py`
- **Target Test File**: `tests/test_svg_generator.py`
- **Spec File**: `docs/specs/svg_generator_spec.md`

- [x] [BA] Define behavioral scenarios for SVGGenerator (Epic Swimlanes) <!-- id: 100 -->
    - [x] Scenario 1: Empty Roadmap <!-- id: 110 -->
    - [x] Scenario 2: EPIC Swimlanes <!-- id: 111 -->
    - [x] Scenario 3: Mixed Statuses in Lane <!-- id: 112 -->
    - [x] Scenario 4: Legend Rendering <!-- id: 113 -->
- [x] [TE] Implement Kedge Test Suite for SVGGenerator <!-- id: 101 -->
- [x] [DEV] Implement SVGGenerator class (DOP & Pydantic) <!-- id: 102 -->
- [x] [QA] Verify full project quality suite <!-- id: 103 -->

## Status
- Core Engine: (d)
- Roadmap Parser: (/)
- 1.3.1 SVG Heatmap: (*)
