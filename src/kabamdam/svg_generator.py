from pydantic import BaseModel
from kabamdam.parser import RoadmapTask, TaskStatus
from typing import List


class SVGConfig(BaseModel):
    width: int = 800
    row_height: int = 60
    square_size: int = 20
    padding: int = 10
    label_width: int = 150
    colors: dict = {
        TaskStatus.DONE: "#2ea44f",
        TaskStatus.ANALYSIS: "#0969da",
        TaskStatus.DEVELOPMENT: "#dbab09",
        TaskStatus.TESTING: "#dbab09",
        TaskStatus.TODO: "#8b949e",
    }


class SVGGenerator:
    def __init__(self, config: SVGConfig = None):
        self.config = config or SVGConfig()

    def generate(self, tasks: List[RoadmapTask]) -> str:
        if not tasks:
            return self._generate_empty_state()

        epics = [t for t in tasks if t.type == "EPIC"]
        canvas_height = (
            len(epics) * self.config.row_height
        ) + 100  # Extra space for legend

        svg_parts = [
            f'<svg width="{self.config.width}" height="{canvas_height}" viewBox="0 0 {self.config.width} {canvas_height}" xmlns="http://www.w3.org/2000/svg">'
        ]

        for i, epic in enumerate(epics):
            y_offset = (i * self.config.row_height) + self.config.padding

            # Label
            svg_parts.append(
                f'<text x="{self.config.padding}" y="{y_offset + 30}" font-family="sans-serif" font-size="14" fill="#24292f">{epic.description}</text>'
            )

            # Atomic items (subtasks/bugs) - flattening the hierarchy
            atomic_tasks = self._get_atomic_tasks(epic)
            # Sort atomic tasks to maintain consistent flow by status
            # Status order: TODO -> (ANALYSIS/DEVELOPMENT/TESTING) -> DONE
            status_order = [
                TaskStatus.TODO,
                TaskStatus.ANALYSIS,
                TaskStatus.DEVELOPMENT,
                TaskStatus.TESTING,
                TaskStatus.DONE,
            ]
            atomic_tasks.sort(key=lambda t: status_order.index(t.status))

            for j, task in enumerate(atomic_tasks):
                x_offset = self.config.label_width + (j * (self.config.square_size + 5))
                color = self.config.colors.get(task.status, "#8b949e")
                svg_parts.append(
                    f'<rect x="{x_offset}" y="{y_offset + 10}" width="{self.config.square_size}" height="{self.config.square_size}" fill="{color}" rx="3" />'
                )

        svg_parts.append(self._generate_legend(canvas_height - 40))
        svg_parts.append("</svg>")

        return "\n".join(svg_parts)

    def _get_atomic_tasks(self, task: RoadmapTask) -> List[RoadmapTask]:
        """Recursively extract level 3+ tasks (Subtasks and Bugs)."""
        atomics = []
        if task.level >= 3:
            atomics.append(task)
        for sub in task.subtasks:
            atomics.extend(self._get_atomic_tasks(sub))
        return atomics

    def _generate_empty_state(self) -> str:
        canvas_height = 200
        svg = f'''<svg width="{self.config.width}" height="{canvas_height}" xmlns="http://www.w3.org/2000/svg">
    <text x="50%" y="40%" text-anchor="middle" font-family="sans-serif" font-size="20" fill="#8b949e">No Roadmap Data available</text>
    {self._generate_legend(canvas_height - 40)}
</svg>'''
        return svg

    def _generate_legend(self, y_offset: int) -> str:
        labels = [
            ("#2ea44f", "Progress"),
            ("#0969da", "Lessons"),
            ("#dbab09", "Design"),
            ("#8b949e", "Planned"),
        ]
        legend_parts = []
        for i, (color, label) in enumerate(labels):
            x = 20 + (i * 120)
            legend_parts.append(
                f'<rect x="{x}" y="{y_offset}" width="15" height="15" fill="{color}" rx="3" />'
            )
            legend_parts.append(
                f'<text x="{x + 20}" y="{y_offset + 12}" font-family="sans-serif" font-size="12" fill="#57606a">{label}</text>'
            )
        return "\n".join(legend_parts)
