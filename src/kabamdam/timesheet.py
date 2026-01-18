import re
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class TimesheetEntry(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_date: Optional[str] = None
    progress: Optional[str] = None
    lessons: Optional[str] = None
    design: Optional[str] = None
    planned: Optional[str] = None
    comments: Optional[str] = None


class TimesheetParser:
    @staticmethod
    def create_entry(**kwargs) -> TimesheetEntry:
        return TimesheetEntry(**kwargs)

    def parse_file(self, file_path: str | Path) -> List[TimesheetEntry]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return self.parse_string(path.read_text())

    def parse_string(self, content: str) -> List[TimesheetEntry]:
        lines = content.splitlines()
        entries = []

        current_header = ""
        headers_found = False

        # Simple table row regex: | col1 | col2 | ... |
        table_row_pattern = re.compile(r"^\s*\|(?P<cells>.*)\|\s*$")

        for line in lines:
            line_stripped = line.strip()

            # Detect headers
            if line_stripped.startswith("#"):
                current_header = line_stripped.lstrip("#").strip().lower()
                headers_found = False
                continue

            # Skip template sections
            if "template" in current_header:
                continue

            match = table_row_pattern.match(line)
            if match:
                cells_raw = match.group("cells").split("|")
                cells = [c.strip() for c in cells_raw]

                # Detect header/separator
                if all(re.match(r"^[-:\s]+$", c) for c in cells) and any(
                    "-" in c for c in cells
                ):
                    headers_found = True
                    continue

                if "date" in [c.lower() for c in cells] and "progress" in [
                    c.lower() for c in cells
                ]:
                    headers_found = True
                    continue

                if headers_found:
                    # We expect 6 columns: Date, Progress, Comments, Lessons, Design, Planned
                    # Pad cells if necessary
                    while len(cells) < 6:
                        cells.append("")

                    raw_date = cells[0] if cells[0] else None
                    progress = cells[1] if cells[1] else None
                    comments = cells[2] if cells[2] else None
                    lessons = cells[3] if cells[3] else None
                    design = cells[4] if cells[4] else None
                    planned = cells[5] if cells[5] else None

                    # Check if row is empty
                    if not any(
                        [raw_date, progress, lessons, design, planned, comments]
                    ):
                        continue

                    # Ignore rows with placeholder values like "format" or "Progress" (case-insensitive)
                    if raw_date and "format" in raw_date.lower():
                        continue
                    if (
                        progress
                        and "progress" in progress.lower()
                        and "roadmap" in progress.lower()
                    ):
                        continue

                    entry = TimesheetEntry(
                        raw_date=raw_date,
                        progress=progress,
                        comments=comments,
                        lessons=lessons,
                        design=design,
                        planned=planned,
                    )
                    entries.append(entry)
            else:
                in_table = False
                headers_found = False

        return entries
