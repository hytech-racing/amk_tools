Various tools for AMK inverters/motors:
# AMK Tool: CAN Message Editor
This is a tool for editing CAN Messages for the AMK inverter.

## Features
- Importing RAW/JSON CAN messages
- Exporting RAW/JSON CAN messages
- Editing values
- Checks for invalid values
- Displays Error and Warning Pop-ups

## WIP
- Drop-down selection for possible signal IDs
- Autopopulation of certain values based on others
- Bug fixes
- Friendlier UI
- Not having to run as admin

## Installation
### Windows
Go to [Releases](https://github.com/hytech-racing/amk_tools/releases) and follow the installation guide of the latest release.
### Mac & Linux
#### Prerequisites
Python 3.7+
```
pip install PyQt5
```
#### Cloning the Repository
```terminal
cd (directory/of/your/choice)
git clone https://github.com/hytech-racing/amk_tools.git
cd amk_tools/msg_editor
```
#### Running the UI
```
python ui.py
```

##### Usage Guide
The user can build a CAN message from scratch, or go to File -> Import JSON or Import Raw and work from an existing message.

The user can export the message by File -> Export JSON or Export Raw (The default directory is the downloads folder).

There are example files in msg_editor/data that you can import.

