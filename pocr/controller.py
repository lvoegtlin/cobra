from __future__ import print_function, unicode_literals

import git
from github import Github

from pocr.conf.config import Config
from pocr.utils.constants import Texts
from pocr.project import Project
from pocr.utils.command_line import get_params
from pocr.utils.utils import get_object_from_list_by_name, ask_questions, user_password_dialog, \
    duplication_check, create_files_folders, check_requirements, first_usage

import subprocess
import shutil
import os


def main():
    # read args
    args = get_params()

    # requirements check
    check_requirements()

    if args.install:
        if first_usage():
            installation()
            print('POCR successfully installed!')
        else:
            print("POCR is already installed!")

    if args.command == 'create':
        create(**args.__dict__)

    if args.clear:
        subprocess.run("./pocr/clean.sh", shell=True)


def create(project_name, python_version, git_hook, **kwargs):
    git_exist = 'repo' in kwargs
    conda_exist = 'conda' in kwargs

    # load config
    Config.getInstance().load_config()

    # get github user
    github = Github(Config.getInstance().sec)
    user = github.get_user()

    # checks if the different modules already exists
    # TODO give option to connect existing github repo or/and conda env
    duplication_check(project_name, user, not git_exist, not conda_exist)

    # create git repo
    if kwargs['test']:
        return

    if not git_exist:
        user.create_repo(project_name, auto_init=True)
        repo_name = project_name
    else:
        repo_name = kwargs['repo']

    # pull repo
    cwd = os.getcwd()
    git_url = "{}{}/{}.git".format(Config.getInstance().connection_type.url, Config.getInstance().username, repo_name)
    git.Git(cwd).clone(git_url)

    if not conda_exist:
        conda_name = project_name
    else:
        conda_name = kwargs['conda']

    # create conda
    arguments = ["--name", conda_name]
    if python_version:
        arguments.append("python={}".format(python_version))
    # can not use conda api because it does not work
    os.system("conda create {}".format(' '.join(arguments)))

    if git_hook:
        shutil.copy('./pocr/utils/pre-commit', os.path.join(os.getcwd(), '.git', 'hooks', 'pre-commit'))

    # save path, conda name, name, git link, python version into project file
    Project.append_project(Project(os.getcwd(), project_name, conda_name, repo_name, Config.getInstance().used_vcs, python_version))


def installation():
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


def entry_point():
    main()


if __name__ == '__main__':
    entry_point()
