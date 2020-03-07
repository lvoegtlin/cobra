# Cobra

[![PyPI version](https://badge.fury.io/py/cobra-projects.svg)](https://badge.fury.io/py/cobra-projects)

Cobra is a project creation and management tool for python and git.
It creates a conda environment and a github repository based on your requirements.


## Requirements
* Python >= 3.6
* [Conda](https://docs.conda.io/en/latest/miniconda.html)
* [Github](https://github.com)

You can use the base conda to install cobra. 

```conda config --set auto_activate_base true```

## Installation
You have three different options to install cobra. Just always keep in mind that the python version need to be > 3.5.

### pip
If your pip path is pointing to the pip3 you can also you just pip.
```
pip3 install cobra-projects
```

Then execute the command
```
cobra --install
```
and follow the instructions.

### github
1. Download the sourcecode from [github](https://github.com/lvoegtlin/cobra).
2. Move into the cobra root directory (folder which contains the setup.py file) ```cd cobra```
3. Install it ```pip install .```

Then execute the command
```
cobra --install
```
and follow the instructions.


## Uninstallation
If you have to re-install or uninstall cobra:
1. Delete the access token from your github page  (Settings -> Developer settings -> Personal access tokens -> delete (cobra)
2. ```rm -rf ~/.cobra```
3. ```pip3/pip uninstall cobra-projects```

## Usage
```
usage: cobra [-h] [--install] [--test] [--clear] {create,list,remove} ...

Project creation (cobra) command line tool

positional arguments:
  {create,list,remove}  The different functions of cobra
    create              Create a new cobra project
    list                Lists all existing cobra projects
    remove              Remove a cobra project

optional arguments:
  -h, --help            show this help message and exit
  --install             Start the installation wizard.
  --test                Puts cobra into testing mode
  --clear               Clears all user files

```

### Create
To create a new project you can use the ```create``` command. 
The minimum requirements is the ```-n``` parameter to give the project a name.
You can also lik the project with already existing conda environments or github repos.

CARE:
The ```-gh, --git-hook``` command is in beta. This command exports before each git commit the conda environment.

```
usage: cobra create [-h] -n PROJECT_NAME [-p PYTHON_VERSION] [-r REPO_NAME]
                   [-c CONDA_NAME] [-gh]

optional arguments:
  -h, --help            show this help message and exit
  -n PROJECT_NAME, --project-name PROJECT_NAME
                        Name of the project
  -p PYTHON_VERSION, --python-version PYTHON_VERSION
                        Python version for the project. Default: 3.5
  -r REPO_NAME, --repo-name REPO_NAME
                        If you already have a github repo for the project.
                        Enter the repo name.
  -c CONDA_NAME, --conda-name CONDA_NAME
                        If you already have a conda environment for the
                        project. Enter the name.
  -gh, --git-hook       Install a pre-commit git hook which updates the conda
                        environment file before you commit. This is just
                        working, if the current environment is the 
                        environment of the project!

```

### List
This command lists all the cobra project with some additional information. 
```
usage: cobra list [-h]

optional arguments:
  -h, --help  show this help message and exit

```

### Remove
After some time you want to remove a project from your system. 
This you can do with the remove command.
The remove command with out additional options will just delete the cobra project from the system but not the files, environment or the repository.
If you want to remove the the files, environment or repository use the below shown parameters.

```
usage: cobra remove [-h] -n NAME [-r] [-c] [-f] [-a]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of the cobra project to remove
  -r, --repo            Also removes the remote repository
  -c, --conda           Also removes the conda environment from the system
  -f, --folder          Also removes the local folder
  -a, --remove-all      Remove everything (repo, folder, conda)

```

### TODO
- [ ] Create repo with template
- [ ] Create conda Dockerfile
- [ ] Automatically build docker container and push it to dockerhub
