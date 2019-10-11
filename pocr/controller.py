import sys

import git
from github import Github
from tabulate import tabulate

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
            print('pocr successfully installed!')
            sys.exit(1)
        else:
            print("pocr is already installed!")
            sys.exit(1)

    if first_usage():
        print('pocr not installed! us the command "pocr --install" first')

    if args.command == 'create':
        create(**args.__dict__)

    if args.command == 'list':
        listing(**args.__dict__)

    if args.clear:
        subprocess.run("./pocr/clean.sh", shell=True)


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


def create(project_name, python_version, git_hook, **kwargs):
    git_exist = 'repo' in kwargs
    conda_exist = 'conda' in kwargs
    conda_name = project_name
    repo_name = project_name

    # load config
    Config.getInstance().load_config()

    # get github user
    github = Github(Config.getInstance().sec)
    user = github.get_user()

    # checks if the different modules already exists
    # TODO give option to connect existing github repo or/and conda env
    duplication_check(project_name, user, not git_exist, not conda_exist)

    if not kwargs['test']:
        if git_exist:
            repo_name = kwargs['repo']
        else:
            user.create_repo(project_name, auto_init=True)

        # pull repo
        cwd = os.getcwd()
        git_url = "{}{}/{}.git".format(Config.getInstance().connection_type.url, Config.getInstance().username, repo_name)
        git.Git(cwd).clone(git_url)

        if conda_exist:
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
    Project.append_project(
        Project(os.getcwd(), project_name, conda_name, repo_name, Config.getInstance().used_vcs, python_version)
    )


def listing(**kwargs):
    projects = Project.load_projects()
    if projects:
        headers = vars(next(iter(projects.values()))).keys()
        headers = [h[1:] for h in headers]
        projects = [list(vars(p).values()) for p in projects.values()]
        print(tabulate(projects, headers=headers))
    else:
        print("There are no pocr projects! Use the 'create' command to create some projects.")


def entry_point():
    main()


if __name__ == '__main__':
    entry_point()
