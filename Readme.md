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
- ABS can be installed in Kali Linux using the script install.sh
    - Running install.sh installs ABS in the user's home directory
    - The script creates a desktop shortcut for the user
    - The script creates a new script: abs-gui, that the user can run manually if they wish
- The Packager can be ran on Windows as a standalone exe file
    - Located under Packager/dist
