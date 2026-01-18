import pytest
from kabamdam.timesheet import TimesheetParser


def test_parse_multi_column_contributions():
    content = """
| Date | Progress | Comments | Lessons | Design | Planned |
| --- | --- | --- | --- | --- | --- |
| 2327:21.10.2025 | 1.1.1 - (*) -> (d) | Good start | Need regex | Pydantic | 1.1.2 - (a) -> (d) |
"""
    parser = TimesheetParser()
    entries = parser.parse_string(content)

    assert len(entries) == 1
    entry = entries[0]
    assert entry.raw_date == "2327:21.10.2025"
    assert entry.timestamp.year == 2025
    assert entry.timestamp.month == 10
    assert entry.timestamp.day == 21
    assert entry.timestamp.hour == 23
    assert entry.timestamp.minute == 27

    assert entry.progress == "1.1.1 - (*) -> (d)"
    assert entry.task_id == "1.1.1"
    assert entry.from_status == "*"
    assert entry.to_status == "d"

    assert entry.comments == "Good start"


def test_handle_empty_date_cells():
    content = """
| Date | Progress | Comments | Lessons | Design | Planned |
| --- | --- | --- | --- | --- | --- |
| 2327:21.10.2025 | 1.1.1 | | | | |
|                 | 1.1.2 | | | | |
"""
    parser = TimesheetParser()
    entries = parser.parse_string(content)

    assert len(entries) == 2
    assert entries[0].raw_date == "2327:21.10.2025"
    assert entries[1].raw_date is None or entries[1].raw_date.strip() == ""


def test_ignore_empty_rows():
    content = """
| Date | Progress | Comments | Lessons | Design | Planned |
| --- | --- | --- | --- | --- | --- |
| 2327:21.10.2025 | 1.1.1 | | | | |
| | | | | | |
"""
    parser = TimesheetParser()
    entries = parser.parse_string(content)

    assert len(entries) == 1
    assert entries[0].progress == "1.1.1"


def test_aggregation_contribution_points():
    entry = TimesheetParser.create_entry(
        progress="1.1.1", lessons="Learned X", design="Design Y", planned="Plan Z"
    )
    # This helper might be used by the SVG generator later
    # For now, we just ensure the entry has the data
    assert entry.progress == "1.1.1"
    assert entry.lessons == "Learned X"
    assert entry.design == "Design Y"
    assert entry.planned == "Plan Z"


def test_parse_full_file_ignoring_template():
    # Constructing a content similar to timesheets_example.md
    content = """
# Timesheets
## Template
| Date | Progress | Comments | Lessons | Design | Planned |
| --- | --- | --- | --- | --- | --- |
| format | roadmap | description | anything | decisions | planned |

## Timesheet Records
| Date | Progress | Comments | Lessons | Design | Planned |
| --- | --- | --- | --- | --- | --- |
| 2327:21.10.2025 | 1.1.1 | | | | |

| Date | Progress | Comments | Lessons | Design | Planned |
| --- | --- | --- | --- | --- | --- |
| 1630:13.12.2025 | 1.1.2 | | | | |
"""
    parser = TimesheetParser()
    entries = parser.parse_string(content)

    # Template should be ignored (1 entry), plus the 2 valid entries = 2 entries total
    # Actually, the template row "format | roadmap..." should be filtered out.
    assert len(entries) == 2
    assert entries[0].raw_date == "2327:21.10.2025"
    assert entries[1].raw_date == "1630:13.12.2025"


def test_malformed_date_raises_value_error():
    content = """
| Date | Progress | Comments | Lessons | Design | Planned |
| --- | --- | --- | --- | --- | --- |
| malformed_date | 1.1.1 | | | | |
"""
    parser = TimesheetParser()
    with pytest.raises(ValueError, match="Invalid date format"):
        parser.parse_string(content)


def test_malformed_progress_raises_value_error():
    content = """
| Date | Progress | Comments | Lessons | Design | Planned |
| --- | --- | --- | --- | --- | --- |
| 2327:21.10.2025 | malformed_progress | | | | |
"""
    parser = TimesheetParser()
    with pytest.raises(ValueError, match="Invalid progress format"):
        parser.parse_string(content)


def test_file_not_found():
    parser = TimesheetParser()
    with pytest.raises(FileNotFoundError):
        parser.parse_file("non_existent_timesheet.md")
