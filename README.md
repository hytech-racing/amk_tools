# AMK Tool: CAN Message Editor
This is a tool for editing CAN Messages.

## Features
- Importing RAW/JSON CAN messages
- Exporting RAW/JSON CAN messages
- Editting values
- Checks for invalid values

## WIP
- Clearer descriptions
- Friendlier UI
- Easier installation
- Autopopulation of certain values based on others

# Installation
## Prerequisites
Python 3.7+
```
pip install PyQt5
```
## Cloning the Repository
```
git clone https://github.com/hytech-racing/amk_tools.git
cd amk_tools
```
## Running the UI
```
python ui.py
```

# Usage Guide
The user can build a CAN message from scratch, or go to File -> Import JSON or Import Raw and work from an existing message.

The user can export the message by File -> Export JSON or Export Raw
