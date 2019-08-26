import argparse
import os
import shutil
import sys
from constants import Constants

supported_vcs = ["github"]


def main():
    parse = argparse.ArgumentParser(description="Project creation (pocr) command line tool")
    parse.add_argument("--install", help="Start the installation wizzard.", action="store_true")

    args = parse.parse_args()

    # requirements check
    check_requirements()

    if args.install:
        if first_usage():
            run_installation()
        else:
            print("POCR is already installed!")

    ## yes, install
    ### check for programms
    ### get user info
    ### save
    ## no, parse the input
    pass


def first_usage():
    """
    Checks if the pocr config file is existing.
    If this file is existing we know that it is not first usage and so the function returns false.
    Else vise versa.

    :return:
        boolean: if its first usage or not
    """
    return not os.path.exists(Constants.POCR_FOLDER)


# install wizard
def run_installation():
    # create files
    create_files_folders()

    print("Chose the vcs you use")
    for i, vcs in enumerate(supported_vcs):
        print("{}) {}".format(i, vcs))
    text = input("select: ")
    print(text)
    pass


def create_files_folders():
    # create folder
    os.mkdir(Constants.POCR_FOLDER)
    # create conf file
    open(Constants.CONF_FILE_PATH, 'a').close()
    # project file
    open(Constants.PROJECT_FILE_PATH, 'a').close()


def check_requirements():
    if shutil.which("conda") is None:
        raise Exception("Conda is not installed! https://docs.conda.io/projects/conda/en/latest/user-guide/install/")
    if sys.version_info[0] < 3 and sys.version_info[1] < 5:
        raise Exception("The default python version is lower then 3.5. Please update!")

