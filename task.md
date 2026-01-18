# Task: Implement SVG Heatmap Enhancements (1.3.1 - 1.3.3)

## Unit: SVG Palette and Legend
- **Target Source File**: `src/kabamdam/svg_generator.py`
- **Target Test File**: `tests/test_svg_generator.py`
- **Spec File**: `specs/1.3.1_behaviors.md`
- [x] Update `SVGConfig.colors` to match 4-color scheme <!-- id: 7 -->
- [x] Update `SVGGenerator._generate_legend` labels <!-- id: 8 -->
- [x] Scenario: `DONE` maps to Progress (#2ea44f) <!-- id: 13 -->
- [x] Scenario: `TESTING` maps to Lessons (#8250df) <!-- id: 14 -->
- [x] Scenario: `ANALYSIS`/`DEVELOPMENT` map to Design (#0969da) <!-- id: 15 -->
- [x] Scenario: `TODO` maps to Planned (#8b949e) <!-- id: 16 -->
- [x] Tests Ready: `tests/test_svg_generator.py` (Kedge) <!-- id: 19 -->
- [x] Implemented <!-- id: 21 -->

## Unit: Bug Visual Indicator
- **Target Source File**: `src/kabamdam/svg_generator.py`
- **Target Test File**: `tests/test_svg_generator.py`
- **Spec File**: `specs/1.3.1_behaviors.md`
- [x] Implement bug icon rendering in `SVGGenerator` <!-- id: 9 -->
- [x] Ensure `_get_atomic_tasks` correctly handles hierarchy for bugs <!-- id: 10 -->
- [x] Scenario: Render BUG with white circle icon <!-- id: 17 -->
- [x] Scenario: Render SUBTASK as plain square <!-- id: 18 -->
- [x] Tests Ready: `tests/test_svg_generator.py` (Kedge) <!-- id: 20 -->
- [x] Implemented <!-- id: 22 -->

## Unit: Integration & Verification
- **Target Source File**: `src/kabamdam/svg_generator.py`
- **Target Test File**: `tests/test_svg_generator.py`
- [x] Run `mise run test` to verify changes <!-- id: 11 -->
- [x] Manually verify generated SVG output <!-- id: 12 -->


---

# Next Workflow: [Code Reviewer](./roles/code_reviewer.md)
