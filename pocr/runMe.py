import os
import shutil
import sys

from pocr.conf.settings import Settings
from pocr.constants import Constants
from pocr.utils.command_line import get_params


class POCR:

    def __init__(self):
        self.args = get_params()

    def main(self):
        # requirements check
        self.check_requirements()

        if self.args.install:
            if self.first_usage():
                self.run_installation()
            else:
                print("POCR is already installed!")

        ## yes, install
        ### check for programms
        ### get user info
        ### save
        ## no, parse the input
        pass

    def first_usage(self):
        """
        Checks if the pocr config file is existing.
        If this file is existing we know that it is not first usage and so the function returns false.
        Else vise versa.

        :return:
            boolean: if its first usage or not
        """
        return not os.path.exists(Constants.POCR_FOLDER)

    # install wizard
    def run_installation(self):
        # create files

        # TODO create git hook (conda list -r --json -> returns json with the revision)

        print("Chose the vcs you want to use (for all projects)")
        vcs_selection = ""
        while type(vcs_selection) is not int:
            for i, vcs in enumerate(Settings.getInstance().vcses):
                print("{}) {}".format(i, vcs.name))
            try:
                vcs_selection = int(input("select: "))
            except ValueError:
                print("Please enter an integer")
        Settings.getInstance().used_vcs = vcs_selection

        # finish vcs install (ssh http selection; username and password or token)

        self.create_files_folders()

        # save infos
        pass

    def create_files_folders(self):
        # create folder
        os.mkdir(Constants.POCR_FOLDER)

        # create conf file
        open(Constants.CONF_FILE_PATH, 'a').close()
        Settings.getInstance().write_into_yaml_file(Constants.CONF_FILE_PATH, **Constants.CONF_DICT)
        # project file {'TestProject': {infos}}
        open(Constants.PROJECT_FILE_PATH, 'a').close()

    def check_requirements(self):
        if shutil.which("conda") is None:
            raise Exception(
                "Conda is not installed! https://docs.conda.io/projects/conda/en/latest/user-guide/install/")
        if sys.version_info[0] < 3 and sys.version_info[1] < 5:
            raise Exception("The default python version is lower then 3.5. Please update!")


def entry_point():
    POCR().main()


if __name__ == '__main__':
    entry_point()
