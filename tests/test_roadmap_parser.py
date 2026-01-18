import pytest
from kabamdam.parser import RoadmapParser, TaskStatus


def test_parse_simple_list():
    content = """
- (*) 1. Task A
- (d) 2. Task B
- (/) 3. Task C
"""
    parser = RoadmapParser()
    tasks = parser.parse_string(content)

    assert len(tasks) == 3
    assert tasks[0].id == "1"
    assert tasks[0].status == TaskStatus.TODO
    assert tasks[0].high_level_status == "TODO"

    assert tasks[1].id == "2"
    assert tasks[1].status == TaskStatus.DEVELOPMENT
    assert tasks[1].high_level_status == "DOING"

    assert tasks[2].id == "3"
    assert tasks[2].status == TaskStatus.DONE
    assert tasks[2].high_level_status == "DONE"


def test_parse_nested_hierarchy():
    content = """
- (d) 1. Epic
    - (d) 1.1 Story
        - (*) 1.1.1 Subtask
"""
    parser = RoadmapParser()
    tasks = parser.parse_string(content)

    assert len(tasks) == 1
    epic = tasks[0]
    assert epic.description == "Epic"
    assert len(epic.subtasks) == 1

    story = epic.subtasks[0]
    assert story.description == "Story"
    assert story.id == "1.1"
    assert len(story.subtasks) == 1

    subtask = story.subtasks[0]
    assert subtask.description == "Subtask"
    assert subtask.id == "1.1.1"
    assert subtask.status == TaskStatus.TODO


def test_support_specialized_status_codes():
    content = """
- (a) 1. Analysis
- (t) 2. Testing
"""
    parser = RoadmapParser()
    tasks = parser.parse_string(content)

    assert tasks[0].status == TaskStatus.ANALYSIS
    assert tasks[0].high_level_status == "DOING"

    assert tasks[1].status == TaskStatus.TESTING
    assert tasks[1].high_level_status == "DOING"


def test_ignore_noise():
    content = """
# Project Roadmap
Some intro text.

- (*) 1. Task
   
This is a paragraph.
"""
    parser = RoadmapParser()
    tasks = parser.parse_string(content)

    assert len(tasks) == 1
    assert tasks[0].id == "1"


def test_file_not_found():
    parser = RoadmapParser()
    with pytest.raises(FileNotFoundError):
        parser.parse_file("non_existent_file.md")


def test_missing_status_defaults_to_todo():
    content = """
- 1. Implicit Task
"""
    parser = RoadmapParser()
    tasks = parser.parse_string(content)

    assert tasks[0].status == TaskStatus.TODO
