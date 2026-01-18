import subprocess
from pathlib import Path
import shutil
from pytest_kedge import TestSuite, TestCase


def pre_commit_target(files, staged_files=None):
    """
    Simulates a git environment and runs pre-commit.
    """
    sandbox = Path("tests/sandbox_pre_commit")
    if sandbox.exists():
        shutil.rmtree(sandbox)
    sandbox.mkdir(parents=True)

    try:
        # Initialize Git
        subprocess.run(["git", "init"], cwd=sandbox, capture_output=True, check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"], cwd=sandbox, check=True
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"], cwd=sandbox, check=True
        )

        # Setup files
        for path, content in files.items():
            full_path = sandbox / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

        # Add basic config
        config_content = """
repos:
  - repo: local
    hooks:
      - id: kabamdam
        name: kabamdam
        entry: kabamdam
        language: system
        files: ^(docs/roadmap/ROADMAP\\.md|timesheets\\.md)$
        pass_filenames: false
"""
        (sandbox / ".pre-commit-config.yaml").write_text(config_content)

        # Initial commit
        subprocess.run(["git", "add", "."], cwd=sandbox, check=True)
        subprocess.run(["git", "commit", "-m", "initial"], cwd=sandbox, check=True)

        # Modify and stage files
        if staged_files:
            for path, content in staged_files.items():
                (sandbox / path).write_text(content)
                subprocess.run(["git", "add", path], cwd=sandbox, check=True)

        # Run pre-commit
        result = subprocess.run(
            ["pre-commit", "run"], cwd=sandbox, capture_output=True, text=True
        )

        # Detect modification failure vs real failure
        modified = "files were modified by this hook" in result.stdout
        passed = "Passed" in result.stdout
        skipped = "Skipped" in result.stdout
        failed = "Failed" in result.stdout and not modified

        return {
            "exit_code": result.returncode,
            "modified": modified,
            "passed": passed,
            "skipped": skipped,
            "failed": failed,
        }
    finally:
        if sandbox.exists():
            shutil.rmtree(sandbox)


pre_commit_tests = TestSuite(
    target=pre_commit_target,
    scenarios=[
        TestCase(
            name="scenario_1_trigger_on_roadmap",
            input={
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",
                    "README.md": "<!-- KABAMDAM:START --><!-- KABAMDAM:END -->",
                },
                "staged_files": {"docs/roadmap/ROADMAP.md": "# Updated Roadmap"},
            },
            # Pre-commit returns 1 if files are modified, which we expect here
            expected={
                "exit_code": 1,
                "modified": True,
                "passed": False,
                "skipped": False,
                "failed": False,
            },
            test_failure_message="Hook should have modified the README and returned 1",
        ),
        TestCase(
            name="scenario_2_trigger_on_timesheets",
            input={
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",  # Need this for default main
                    "timesheets.md": "# Timesheets",
                    "README.md": "<!-- KABAMDAM:START --><!-- KABAMDAM:END -->",
                },
                "staged_files": {"timesheets.md": "| Date | Progress |"},
            },
            expected={
                "exit_code": 1,
                "modified": True,
                "passed": False,
                "skipped": False,
                "failed": False,
            },
            test_failure_message="Hook should have triggered on timesheets and modified README",
        ),
        TestCase(
            name="scenario_3_bypass_on_unrelated",
            input={
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",
                    "src/main.py": "print('hello')",
                },
                "staged_files": {"src/main.py": "print('updated')"},
            },
            expected={
                "exit_code": 0,
                "modified": False,
                "passed": False,
                "skipped": True,
                "failed": False,
            },
            test_failure_message="Hook should have been skipped for unrelated file",
        ),
        TestCase(
            name="scenario_4_successful_update",
            input={
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",
                    "README.md": "<!-- KABAMDAM:START --><!-- KABAMDAM:END -->",
                },
                "staged_files": {"docs/roadmap/ROADMAP.md": "# Roadmap v2"},
            },
            expected={
                "exit_code": 1,
                "modified": True,
                "passed": False,
                "skipped": False,
                "failed": False,
            },
            test_failure_message="Hook failed to modify file as expected",
        ),
        TestCase(
            name="scenario_5_failure_blocks_commit",
            input={
                "files": {
                    "docs/roadmap/ROADMAP.md": "# Roadmap",
                    "README.md": "<!-- KABAMDAM:START -->",  # Partial
                },
                "staged_files": {"docs/roadmap/ROADMAP.md": "# Roadmap fail"},
            },
            expected={
                "exit_code": 1,
                "modified": False,
                "passed": False,
                "skipped": False,
                "failed": True,
            },
            test_failure_message="Hook should have failed (not modified) on invalid markers",
        ),
    ],
)
