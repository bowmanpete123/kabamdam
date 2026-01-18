from datetime import datetime
import re
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class TimesheetEntry(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Raw fields
    raw_date: Optional[str] = None
    progress: Optional[str] = None
    lessons: Optional[str] = None
    design: Optional[str] = None
    planned: Optional[str] = None
    comments: Optional[str] = None

    # Extracted fields
    timestamp: Optional[datetime] = None
    task_id: Optional[str] = None
    from_status: Optional[str] = None
    to_status: Optional[str] = None


class TimesheetParser:
    DATE_REGEX = re.compile(
        r"^(?P<hour>\d{2})(?P<minute>\d{2}):(?P<day>\d{2})[./](?P<month>\d{2})[./](?P<year>\d{4})$"
    )
    PROGRESS_REGEX = re.compile(
        r"^(?P<id>[\d\.]+)(?:\s*(?:-)?\s*(?:\((?P<from>[^)]+)\))?\s*->\s*(?:\((?P<to>[^)]+)\))?)?$"
    )
    TABLE_ROW_RE = re.compile(r"^\s*\|(?P<cells>.*)\|\s*$")

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

            match = self.TABLE_ROW_RE.match(line)
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

                    timestamp = None
                    if raw_date:
                        date_match = self.DATE_REGEX.match(raw_date)
                        if not date_match:
                            raise ValueError(f"Invalid date format: {raw_date}")
                        timestamp = datetime(
                            int(date_match.group("year")),
                            int(date_match.group("month")),
                            int(date_match.group("day")),
                            int(date_match.group("hour")),
                            int(date_match.group("minute")),
                        )

                    task_id = None
                    from_status = None
                    to_status = None
                    if progress:
                        progress_match = self.PROGRESS_REGEX.match(progress)
                        if not progress_match:
                            raise ValueError(f"Invalid progress format: {progress}")
                        task_id = progress_match.group("id")
                        from_status = progress_match.group("from")
                        to_status = progress_match.group("to")

                    entry = TimesheetEntry(
                        raw_date=raw_date,
                        progress=progress,
                        comments=comments,
                        lessons=lessons,
                        design=design,
                        planned=planned,
                        timestamp=timestamp,
                        task_id=task_id,
                        from_status=from_status,
                        to_status=to_status,
                    )
                    entries.append(entry)
            else:
                headers_found = False

        return entries
