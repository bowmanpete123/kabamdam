from pytest_kedge import TestSuite, TestCase
from kabamdam.parser import RoadmapTask, TaskStatus
from kabamdam.svg_generator import SVGGenerator


def refined_svg_target(tasks, name=""):
    generator = SVGGenerator()
    svg = generator.generate(tasks)

    if name == "scenario_1":
        return "No Roadmap Data available" in svg
    if name == "scenario_2":
        return all(
            x in svg
            for x in [
                "Epic A",
                "Epic B",
                'fill="#2ea44f"',
                'fill="#8b949e"',
                'fill="#0969da"',
            ]
        )
    if name == "scenario_3":
        return 'fill="#dbab09"' in svg
    if name == "scenario_4":
        return all(x in svg for x in ["Progress", "Lessons", "Design", "Planned"])
    return False


svg_tests = TestSuite(
    target=refined_svg_target,
    scenarios=[
        TestCase(
            name="scenario_1_empty_roadmap",
            input={"tasks": [], "name": "scenario_1"},
            expected=True,
            test_failure_message="Empty roadmap should show placeholder text",
        ),
        TestCase(
            name="scenario_2_epic_swimlanes",
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
                                status=TaskStatus.DONE,
                                level=3,
                                type="SUBTASK",
                            ),
                            RoadmapTask(
                                id="1.2",
                                description="Sub 2",
                                status=TaskStatus.TODO,
                                level=3,
                                type="SUBTASK",
                            ),
                        ],
                    ),
                    RoadmapTask(
                        id="2",
                        description="Epic B",
                        status=TaskStatus.ANALYSIS,
                        level=1,
                        type="EPIC",
                        subtasks=[
                            RoadmapTask(
                                id="2.1",
                                description="Sub 3",
                                status=TaskStatus.ANALYSIS,
                                level=3,
                                type="SUBTASK",
                            ),
                        ],
                    ),
                ],
                "name": "scenario_2",
            },
            expected=True,
            test_failure_message="EPIC swimlanes or colors are missing",
        ),
        TestCase(
            name="scenario_3_mixed_statuses",
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
                                description="Dev Task",
                                status=TaskStatus.DEVELOPMENT,
                                level=3,
                                type="SUBTASK",
                            ),
                            RoadmapTask(
                                id="1.2",
                                description="Test Task",
                                status=TaskStatus.TESTING,
                                level=3,
                                type="SUBTASK",
                            ),
                        ],
                    )
                ],
                "name": "scenario_3",
            },
            expected=True,
            test_failure_message="Development/Testing statuses should map to yellow (#dbab09)",
        ),
        TestCase(
            name="scenario_4_legend_rendering",
            input={"tasks": [], "name": "scenario_4"},
            expected=True,
            test_failure_message="Legend labels are missing",
        ),
    ],
)
