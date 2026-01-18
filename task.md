# Task: Implement CLI Interface (2.1)

## Unit: CLI Scaffolding
- **Target Source File**: `src/kabamdam/main.py`
- **Target Test File**: `tests/test_cli.py`
- **Spec File**: `specs/2.1_behaviors.md`
- [x] Initialize `typer` app in `src/kabamdam/main.py` <!-- id: 23 -->
- [x] Add `[project.scripts]` entry to `pyproject.toml` <!-- id: 31 -->
- [x] Tests Ready: `tests/test_cli.py` (8 scenarios) <!-- id: 39 -->
- [x] Scenario: Default execution with `kabamdam` <!-- id: 32 -->
- [x] Scenario: Override paths via options <!-- id: 33 -->
- [x] Scenario: Handle missing roadmap file <!-- id: 34 -->

## Unit: README Update Logic
- **Target Source File**: `src/kabamdam/main.py`
- **Target Test File**: `tests/test_cli.py`
- **Spec File**: `specs/2.1_behaviors.md`
- [x] Tests Ready: `tests/test_cli.py` (8 scenarios) <!-- id: 40 -->
- [x] Implement `update_readme` function with marker detection <!-- id: 25 -->
- [x] Scenario: Update existing markers correctly <!-- id: 35 -->
- [x] Scenario: Handle missing markers gracefully <!-- id: 36 -->
- [x] Scenario: Calculate relative paths for nested files <!-- id: 37 -->

## Unit: Pipeline Orchestration
- **Target Source File**: `src/kabamdam/main.py`
- **Target Test File**: `tests/test_cli.py`
- **Spec File**: `specs/2.1_behaviors.md`
- [x] Tests Ready: `tests/test_cli.py` (8 scenarios) <!-- id: 41 -->
- [x] Integrate Parsers and SVGGenerator <!-- id: 27 -->
- [x] Implement robust error handling (IOErrors, Partial markers) <!-- id: 38 -->




## Unit: Integration & Verification
- **Target Source File**: `src/kabamdam/main.py`
- **Target Test File**: `tests/test_cli.py`
- [ ] Run full pipeline and verify README update <!-- id: 29 -->
- [ ] Run `mise run test` for CLI coverage <!-- id: 30 -->
