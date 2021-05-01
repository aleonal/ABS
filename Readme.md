# Agent Build System
- Causation Extractor
    - Runs at the creation of a new project
    - The causation extractor groups together events from an ECELd project based on timing and salient artifacts
- Builder
    - The builder displays the relationships created by the causation extractor
    - Relationships can be selected and moved over to the dependencies table
    - The salient artifacts window allows users to add or remove salient artifacts, or change the color of salient artifacts
    - By default, salient artifacts are highlighted in red color
    - From the events in the dependencies table, the user can generate a script to be run by the runner
- Runner
    - ??
- Packager
    - The packager retrieves the virtual machines recognized by VirtualBox
    - From the packager the user can add multiple files and select which virtual machines to include
    - The packager will create a zip file with all included files at the specified directory

# Installation and Setup

- Sorting functions for dependencies & eveents in GUI?
    - This implies that we move sorting functions from CE to ProjectController OR implement front-end sorting separately altogether
    - Discuss as group how we hande the files
    - Does the frontend need backend functionality to be implemented at this point?
- Ask Diego about selecting directory problem in CreateProject.py
- How drag n' drop is being implemented
    - Can we edit items?
    - Do we need backend functions to edit items?



- use venv instead of abs_venv
- rename github to ABS
	- change ABS_DIR folder name in launcher
	- change launcher
