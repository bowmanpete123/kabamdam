#  RoadMap SOP
## Purpose
The purpose of this document is to act as SOP for the RoadMap files that exist as a part of the project structure
## Sections

- **Requirements List**: I've separated the requirements list into three groups based on how they're being dealt with
    - **Work In Progress**: This is the section for things you're actually working on, try to limit the amount in here, these are where I tend to flesh out the requirements into lower level requirements
- **Further Requirements**: Think of these as higher level features that are still currently to be worked on later on in the project timeline
- **Scope Creep**: These features are so off base that they'll need to be a different project basically use this as a dumping ground for all of your "wow we should make a podcast" moments

## Status Notation

The requirements in the roadmap follow a simple convention to keep track
of the project:

> TODO ⇒ Doing (Analysis ⇒ Development ⇒ Testing) ⇒ Done
The notation for this is as follows:

1. **To-do**: (*) - requirements will sit in this state by default
2. **Doing**: which will be broken down into the following steps:
    1. **Analysis**: (a) - We have no idea how to build this, so we're figuring it out **note this is usually not required because the analysis should be done here.**
    2. **Development**: (d) - feature is being created
    3. **Testing**: (t) - feature has been created and is being checked for functionality
3. **Done**: (/) - feature has been completed and functional

## Requirement Levels

I've created a system where each requirement be broken up into three leaves, where the third level is considered as detailed as necessary for a high-level plan.
Below is an example of the three levels:

1. Highest Level Requirement (Think Jira Epic Level)
    1. Second Level Requirement (Think Story Level)
        1. Third Level Requirement (Think Sub-task or Bug that a story is broken into)

### Discussion of Bugs and Subtasks

- Subtask 
    - (this is a piece of a requirement that whose completion is considered the most atomic piece of work)
-  Bug 
    - (this is a piece of a requirement where earlier development work didn't work out right therefore something needs to be fixed)
    - Bugs are notated as an indented version of a subtask, they contain two sentences, a brief bug description and what needs to be done to fix it (in theory)
