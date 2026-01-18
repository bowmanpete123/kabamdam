from kabamdam.parser import RoadmapTask, TaskStatus, RoadmapParser
from kabamdam.svg_generator import SVGGenerator
from pathlib import Path


def manual_verification():
    # Use the sample files or mock data
    parser = RoadmapParser()
    roadmap_path = Path("docs/roadmap/ROADMAP.md")
    if roadmap_path.exists():
        tasks = parser.parse_file(roadmap_path)
    else:
        # Fallback to dummy data
        tasks = [
            RoadmapTask(
                id="1",
                description="Manual Verification Epic",
                status=TaskStatus.TODO,
                level=1,
                type="EPIC",
                subtasks=[
                    RoadmapTask(
                        id="1.1",
                        description="Done Subtask",
                        status=TaskStatus.DONE,
                        level=3,
                        type="SUBTASK",
                    ),
                    RoadmapTask(
                        id="1.2",
                        description="Testing Subtask",
                        status=TaskStatus.TESTING,
                        level=3,
                        type="SUBTASK",
                    ),
                    RoadmapTask(
                        id="1.3",
                        description="Dev Bug",
                        status=TaskStatus.DEVELOPMENT,
                        level=3,
                        type="BUG",
                    ),
                    RoadmapTask(
                        id="1.4",
                        description="Todo Bug",
                        status=TaskStatus.TODO,
                        level=3,
                        type="BUG",
                    ),
                ],
            )
        ]

    generator = SVGGenerator()
    svg = generator.generate(tasks)

    output_path = Path("verification_output.svg")
    output_path.write_text(svg)
    print(f"Generated SVG for manual verification at {output_path.absolute()}")


if __name__ == "__main__":
    manual_verification()
