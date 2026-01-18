from pytest_kedge import TestSuite, TestCase
from kabamdam.parser import RoadmapTask, TaskStatus
from kabamdam.svg_generator import SVGGenerator


def roadmap_svg_target(tasks, name=""):
    generator = SVGGenerator()
    svg = generator.generate(tasks)

    if name == "palette_verification":
        # Check colors
        results = {
            "progress": 'fill="#2ea44f"' in svg,
            "lessons": 'fill="#8250df"' in svg,
            "design": 'fill="#0969da"' in svg,
            "planned": 'fill="#8b949e"' in svg,
        }
        return all(results.values())

    if name == "legend_verification":
        # Check legend text
        labels = ["Progress", "Lessons", "Design", "Planned"]
        return all(label in svg for label in labels)

    if name == "bug_icon_verification":
        # Check for circle indicating a bug
        return "<circle" in svg and 'fill="white"' in svg

    if name == "subtask_no_icon":
        # Ensure no circle if only subtasks
        return "<circle" not in svg

    return False


svg_tests = TestSuite(
    target=roadmap_svg_target,
    scenarios=[
        TestCase(
            name="palette_verification",
            input={
                "tasks": [
                    RoadmapTask(
                        id="1",
                        description="Epic A",
                        status=TaskStatus.TODO,
                        level=1,
                        type="EPIC",
                        subtasks=[
                            RoadmapTask(
                                id="1.1",
                                description="S1",
                                status=TaskStatus.DONE,
                                level=3,
                                type="SUBTASK",
                            ),
                            RoadmapTask(
                                id="1.2",
                                description="S2",
                                status=TaskStatus.TESTING,
                                level=3,
                                type="SUBTASK",
                            ),
                            RoadmapTask(
                                id="1.3",
                                description="S3",
                                status=TaskStatus.ANALYSIS,
                                level=3,
                                type="SUBTASK",
                            ),
                            RoadmapTask(
                                id="1.4",
                                description="S4",
                                status=TaskStatus.TODO,
                                level=3,
                                type="SUBTASK",
                            ),
                        ],
                    )
                ],
                "name": "palette_verification",
            },
            expected=True,
            test_failure_message="New 4-color palette mapping is incorrect",
        ),
        TestCase(
            name="legend_labels",
            input={"tasks": [], "name": "legend_verification"},
            expected=True,
            test_failure_message="Legend labels 'Progress', 'Lessons', 'Design', 'Planned' are missing",
        ),
        TestCase(
            name="bug_icon_rendering",
            input={
                "tasks": [
                    RoadmapTask(
                        id="1",
                        description="Epic A",
                        status=TaskStatus.TODO,
                        level=1,
                        type="EPIC",
                        subtasks=[
                            RoadmapTask(
                                id="1.1",
                                description="Bug 1",
                                status=TaskStatus.DEVELOPMENT,
                                level=3,
                                type="BUG",
                            ),
                        ],
                    )
                ],
                "name": "bug_icon_verification",
            },
            expected=True,
            test_failure_message="Bug icon (white circle) is missing in SVG",
        ),
        TestCase(
            name="subtask_no_icon",
            input={
                "tasks": [
                    RoadmapTask(
                        id="1",
                        description="Epic A",
                        status=TaskStatus.TODO,
                        level=1,
                        type="EPIC",
                        subtasks=[
                            RoadmapTask(
                                id="1.1",
                                description="Sub 1",
                                status=TaskStatus.DEVELOPMENT,
                                level=3,
                                type="SUBTASK",
                            ),
                        ],
                    )
                ],
                "name": "subtask_no_icon",
            },
            expected=True,
            test_failure_message="Visual icon found on SUBTASK (should only be on BUG)",
        ),
    ],
)
