from enum import Enum
import re
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from typing import List


class TaskStatus(str, Enum):
    TODO = "TODO"  # (*)
    ANALYSIS = "ANALYSIS"  # (a)
    DEVELOPMENT = "DEVELOPMENT"  # (d)
    TESTING = "TESTING"  # (t)
    DONE = "DONE"  # (/)


class RoadmapTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str
    description: str
    status: TaskStatus
    subtasks: List["RoadmapTask"] = Field(default_factory=list)
    level: int

    @property
    def high_level_status(self) -> str:
        if self.status in (
            TaskStatus.ANALYSIS,
            TaskStatus.DEVELOPMENT,
            TaskStatus.TESTING,
        ):
            return "DOING"
        return self.status.value


class RoadmapParser:
    STATUS_MAP = {
        "*": TaskStatus.TODO,
        "a": TaskStatus.ANALYSIS,
        "d": TaskStatus.DEVELOPMENT,
        "t": TaskStatus.TESTING,
        "/": TaskStatus.DONE,
    }

    def parse_file(self, file_path: str | Path) -> List[RoadmapTask]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return self.parse_string(path.read_text())

    def parse_string(self, content: str) -> List[RoadmapTask]:
        lines = content.splitlines()
        tasks = []
        stack = []  # Stack of (indent_level, task_object)

        # Regex to match: optional indentation, hyphen, space, optional status '(x)', space, ID (optional), description
        # Example: "    - (d) 1.1 Story"
        pattern = r"^(?P<indent>\s*)-\s+(?:\((?P<status_code>.)\)\s+)?(?:(?P<id>[\d\.]+)\s+)?(?P<description>.*)$"
        regex = re.compile(pattern)

        for line in lines:
            match = regex.match(line)
            if not match:
                continue

            indent = len(match.group("indent"))
            status_code = match.group("status_code")
            task_id = match.group("id") or ""
            if task_id.endswith("."):
                task_id = task_id[:-1]
            description = match.group("description") or ""

            # Map status
            status = self.STATUS_MAP.get(status_code, TaskStatus.TODO)

            # Find parent by indentation
            while stack and stack[-1][0] >= indent:
                stack.pop()

            level = len(stack) + 1

            new_task = RoadmapTask(
                id=task_id,
                description=description.strip(),
                status=status,
                level=level,
                subtasks=[],
            )

            if not stack:
                # Root level task
                tasks.append(new_task)
            else:
                # Add to parent's subtasks
                stack[-1][1].subtasks.append(new_task)

            stack.append((indent, new_task))

        return tasks
