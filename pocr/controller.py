from __future__ import print_function, unicode_literals

import git
from github import Github, UnknownObjectException

from pocr.conf.config import Config
from pocr.constants import Paths, Texts
from pocr.utils.exceptions import ProjectNameAlreadyExists, CondaAlreadyExists
from pocr.project import Project
from pocr.utils.command_line import get_params
from pocr.utils.utils import get_object_from_list_by_name, ask_questions, check_env_exists, user_password_dialog

import subprocess
import shutil
import sys
import os


def main():
    # read args
    args = get_params()

    # requirements check
    check_requirements()

    if args.install:
        if first_usage():
            run_installation()
            print('POCR successfully installed!')
        else:
            print("POCR is already installed!")

    if args.command == 'create':
        create_project(**args.__dict__)

    if args.clear:
        subprocess.run("./pocr/clean.sh", shell=True)


def create_project(name, python_version, git_hook, **kwargs):
    # load config
    load_config()

    # get github user
    github = Github(Config.getInstance().sec)
    user = github.get_user()

    # checks if the different modules already exists
    # TODO give option to connect existing github repo or/and conda env
    duplication_check(name, user)

    # create git repo
    if not kwargs['test']:
        user.create_repo(name, auto_init=True)

        # pull repo
        cwd = os.getcwd()
        git_url = "{}{}/{}.git".format(Config.getInstance().connection_type.url, Config.getInstance().username, name)
        git.Git(cwd).clone(git_url)

        # create conda
        arguments = ["--name", name]
        if python_version:
            arguments.append("python={}".format(python_version))
        # can not use conda api because it does not work
        os.system("conda create {}".format(' '.join(arguments)))

        if git_hook:
            shutil.copy('./pocr/utils/pre-commit', os.path.join(os.getcwd(), '.git', 'hooks', 'pre-commit'))

        # save path, conda name, name, git link, python version into project file
    Project.append_project(Project(os.getcwd(), name, name, Config.getInstance().used_vcs, python_version))


def duplication_check(project_name, github_user):
    # Check if project name already exists
    try:
        # project check
        Project.project_exists(project_name)
        # github check
        github_user.get_repo(project_name)
        # conda check
        check_env_exists(project_name)
    except ProjectNameAlreadyExists:
        print("Project name is already in use")
        sys.exit(1)
    except UnknownObjectException:
        print(
            "The Github user {} already has a repository named {}".format(Config.getInstance().username, project_name))
        sys.exit(1)
    except CondaAlreadyExists:
        print("There exists already a conda environment named {}".format(project_name))


def load_config():
    # load config
    Config.getInstance().load_config()


def first_usage():
    """
    Checks if the pocr config file is existing.
    If this file is existing we know that it is not first usage and so the function returns false.
    Else vise versa.

    :return:
        boolean: if its first usage or not
    """
    return not os.path.exists(Paths.POCR_FOLDER)


# install wizard
def run_installation():
    """
    With this method the user installs the tool. That means he creates the config and the project file,
    enters the user credentials as well as defines the connection type.
    """

    # ask for the vcs which are stored in the vc.yml file
    vcs_selection = ask_questions(['list'], [Texts.VCS_SELECT_TEXT], ['vcs'], [Config.getInstance().vcses])
    used_vcs = Config.getInstance().used_vcs = get_object_from_list_by_name(vcs_selection['vcs'],
                                                                            Config.getInstance().vcses)

    # finish vcs install (ssh http selection; username and password or token)
    error = user_password_dialog()
    while error:
        error = user_password_dialog(error) or {}

    con_selection = ask_questions(['list'], [Texts.CON_SELECT_TEXT], ['con_type'], [used_vcs.connection_types])
    Config.getInstance().connection_type = get_object_from_list_by_name(con_selection['con_type'],
                                                                        used_vcs.connection_types)

    # create files and folders
    create_files_folders()

    # save infos
    Config.getInstance().save_config()


def create_files_folders():
    # create folder
    os.mkdir(Paths.POCR_FOLDER)

    # create conf file
    open(Paths.CONF_FILE_PATH, 'a').close()
    # Config.getInstance().write_into_yaml_file(Constants.CONF_FILE_PATH, **Constants.CONF_DICT)
    # project file {'TestProject': {infos}}
    open(Paths.PROJECT_FILE_PATH, 'a').close()


def check_requirements():
    if shutil.which("conda") is None:
        raise Exception(
            "Conda is not installed! https://docs.conda.io/projects/conda/en/latest/user-guide/install/")
    if sys.version_info[0] < 3 and sys.version_info[1] < 5:
        raise Exception("The default python version is lower then 3.5. Please update!")


def entry_point():
    main()


if __name__ == '__main__':
    entry_point()
