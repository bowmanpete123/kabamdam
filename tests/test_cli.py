from pathlib import Path
import shutil
from typer.testing import CliRunner
from pytest_kedge import TestSuite, TestCase
from kabamdam.main import app


def invoke_app(app, args, files=None):
    """Simple wrapper to bridge invoke with the mock filesystem."""
    if files:
        for p in [
            Path("docs"),
            Path("timesheets.md"),
            Path("README.md"),
            Path("custom.svg"),
            Path("other.md"),
            Path("custom_roadmap.md"),
        ]:
            if p.exists():
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
        for path, content in files.items():
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)

    return CliRunner().invoke(app, args).exit_code


cli_tests = TestSuite(
    target=invoke_app,
    scenarios=[
        TestCase(
            name="1_default_execution",
            input={
                "app": app,
                "args": [],
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",
                    "timesheets.md": "# Timesheets",
                    "README.md": "<!-- KABAMDAM:START --><!-- KABAMDAM:END -->",
                },
            },
            expected=0,
            test_failure_message="Default execution should return exit code 0",
        ),
        TestCase(
            name="2_override_paths",
            input={
                "app": app,
                "args": ["--roadmap-file", "other.md", "--output-svg", "custom.svg"],
                "files": {
                    "other.md": "# Roadmap",
                    "timesheets.md": "# Timesheets",
                    "README.md": "<!-- KABAMDAM:START --><!-- KABAMDAM:END -->",
                },
            },
            expected=0,
            test_failure_message="Path override should return exit code 0",
        ),
        TestCase(
            name="3_missing_roadmap",
            input={
                "app": app,
                "args": ["--roadmap-file", "missing.md"],
                "files": {"README.md": "<!-- KABAMDAM:START --><!-- KABAMDAM:END -->"},
            },
            expected=2,
            test_failure_message="Missing roadmap should return exit code 2",
        ),
        TestCase(
            name="4_update_markers",
            input={
                "app": app,
                "args": [],
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",
                    "timesheets.md": "# Timesheets",
                    "README.md": "<!-- KABAMDAM:START -->\nold content\n<!-- KABAMDAM:END -->",
                },
            },
            expected=0,
            test_failure_message="Updating markers should return exit code 0",
        ),
        TestCase(
            name="5_missing_markers",
            input={
                "app": app,
                "args": [],
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",
                    "timesheets.md": "# Timesheets",
                    "README.md": "# No Markers",
                },
            },
            expected=0,
            test_failure_message="Missing markers should return exit code 0 (Warning)",
        ),
        TestCase(
            name="6_partial_markers",
            input={
                "app": app,
                "args": [],
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",
                    "timesheets.md": "# Timesheets",
                    "README.md": "<!-- KABAMDAM:START -->",
                },
            },
            expected=1,
            test_failure_message="Partial markers should return exit code 1",
        ),
        TestCase(
            name="7_relative_path_root",
            input={
                "app": app,
                "args": [],
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",
                    "timesheets.md": "# Timesheets",
                    "README.md": "<!-- KABAMDAM:START --><!-- KABAMDAM:END -->",
                },
            },
            expected=0,
            test_failure_message="Relative path root should return exit code 0",
        ),
        TestCase(
            name="8_relative_path_nested",
            input={
                "app": app,
                "args": ["--readme-file", "docs/README.md"],
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",
                    "timesheets.md": "# Timesheets",
                    "docs/README.md": "<!-- KABAMDAM:START --><!-- KABAMDAM:END -->",
                },
            },
            expected=0,
            test_failure_message="Relative path nested should return exit code 0",
        ),
    ],
)
