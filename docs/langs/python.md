# Python

## Set up and use
Setting up Python 3 in VS Code: https://code.visualstudio.com/docs/python/python-tutorial
* `py -m pip install --upgrade pip` : it installs and upgrades pip
* `py -m pip install MODULE`: it installs the required module

## Creating and using virtual environments
* `py -m venv .VIRTUALENVIRONMENTNAME`: it creates/uses the virtual environment specified in the path, then selectable in the terminal
* `py -m deactivate`: it destroys the current virtual environment

## Requirements
* `py -m pip freeze > requirements.txt`: it prints a file called _requirements_ with all the package necessary to the current project (they can be retrieved by the command `py -m pip install -r requirements.txt`)