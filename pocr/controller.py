import sys
import subprocess
import shutil
import os
import pkg_resources

import git
from github import UnknownObjectException
from tabulate import tabulate

from pocr.conf.config import Config
from pocr.utils.constants import Texts, Paths
from pocr.project import Project
from pocr.utils.command_line import get_params
from pocr.utils.exceptions import ProjectNameAlreadyExists, CondaAlreadyExists
from pocr.utils.utils import get_object_from_list_by_name, ask_questions, user_password_dialog, \
    duplication_check, create_files_folders, check_requirements, first_usage, get_github_user, check_env_exists


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
        sys.exit(1)

    if args.command == 'create':
        create(**args.__dict__)

    if args.command == 'list':
        listing(**args.__dict__)

    if args.command == 'remove':
        remove(**args.__dict__)

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

    user = get_github_user()

    # checks if the different modules already exists
    # TODO give option to connect existing github repo or/and conda env
    duplication_check(project_name, user, not git_exist, not conda_exist)

    if not kwargs['test']:
        if git_exist:
            print("You provided a git repo...")
            repo_name = kwargs['repo']
        else:
            print("Creating a repo...")
            user.create_repo(project_name, auto_init=True)
            print("Repo creation successful")

        # pull repo
        print("Pulling the repo...")
        cwd = os.getcwd()
        git_url = "{}{}/{}.git".format(Config.getInstance().connection_type.url, Config.getInstance().username, repo_name)
        git.Git(cwd).clone(git_url)
        print("Pulling done")

        if conda_exist:
            conda_name = kwargs['conda']

        # create conda
        print("Creating conda environment...")
        arguments = ["--name", conda_name]
        if python_version:
            arguments.append("python={}".format(python_version))
        # can not use conda api because it does not work
        os.system("conda create -y {}".format(' '.join(arguments)))

        # initial environment file creating
        os.system("touch " + os.path.join(os.getcwd(), repo_name, "environment.yml"))

        if git_hook:
            shutil.copy(pkg_resources.resource_filename(__name__, Paths.PACKAGE_GIT_HOOK_PATH),
                        os.path.join(os.getcwd(), repo_name, '.git', 'hooks', 'pre-commit'))

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


def remove(name, folder, repo, conda, remove_all, **kwargs):
    # remove the project from the project file
    try:
        Project.project_exists(name)
        print("Project does not exist")
        if not kwargs['test']:
            sys.exit(1)
    except ProjectNameAlreadyExists:
        project = Project.remove_project(name)
        print("Successfully removed pocr project {} from the project file".format(name))

    # load config
    Config.getInstance().load_config()

    # github user object
    user = get_github_user()

    if remove_all:
        repo = True
        conda = True
        folder = True

    if repo:
        try:
            repo = user.get_repo(project.repo_name)
            repo.delete()
            print("Successfully removed repo")
        except UnknownObjectException as e:
            if e.status == 404:
                print("Repo could not be deleted! Not existing")
            if e.status == 403:
                print('Permission problem, please reinstall pocr (--clean; --install)')
    if folder:
        try:
            shutil.rmtree(project.project_path)
            print("Successfully removed folders")
        except PermissionError:
            print("Permission error for deleting the project {} folder."
                  " Please delete it by hand or try again.".format(project.project_path))
    if conda:
        try:
            check_env_exists(project.conda_name)
            print("Conda environment does not exist")
        except CondaAlreadyExists:
            # deactivate env
            subprocess.check_output(['conda', 'deactivate'])
            # remove env
            subprocess.check_output(['conda', 'env', 'remove', '--name', project.conda_name])
            print("Successfully removed conda environment")


def entry_point():
    main()


if __name__ == '__main__':
    entry_point()
