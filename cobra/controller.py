import inspect
import os
import shutil
import subprocess
import sys

import pkg_resources
from github import UnknownObjectException
from cobra.utils.module_functions import ModuleFunctions
from tabulate import tabulate

from cobra.conf.config import Config
from cobra.project import Project
from cobra.utils.command_line import get_params
from cobra.utils.constants import Texts, Paths
from cobra.utils.exceptions import ProjectNameAlreadyExists
from cobra.utils.utils import get_object_from_list_by_name, ask_questions, user_password_dialog, \
    duplication_check, check_requirements, first_usage, get_github_user, check_env_exists, \
    delete_path, create_files_folders


def main():
    # read args
    args = get_params()

    # requirements check
    check_requirements()

    if args.install:
        if first_usage():
            installation()
            print('cobra successfully installed!')
            sys.exit(1)
        else:
            print("cobra is already installed!")
            sys.exit(1)

    if first_usage():
        print('cobra not installed! us the command "cobra --install" first')
        sys.exit(1)

    if args.command == 'create':
        create(**args.__dict__)

    if args.command == 'list':
        listing(**args.__dict__)

    if args.command == 'remove':
        remove(**args.__dict__)

    if args.clear:
        subprocess.run("./cobra/clean.sh", shell=True)


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


def create(name, python_version, from_file, **kwargs):
    # load config
    Config.getInstance().load_config()

    if from_file:
        print("Creating project from file")
        project = Project.project_from_file()
        print(".cobra file found. Continue processing...")
        name = project.project_name
    else:
        project = Project(os.getcwd(),
                          name,
                          "repo_name" in kwargs if kwargs['repo_name'] else name,
                          "conda_name" in kwargs if kwargs['conda_name'] else name,
                          Config.getInstance().username,
                          Config.getInstance().used_vcs,
                          python_version)

    # check for if project exists
    Project.project_exists(name)

    # creat missing elements
    create_project_parts(project, **kwargs)

    # save file in cobra folder
    Project.create_project_file(project)

    # save path, conda name, name, git link, python version into project file
    Project.append_project(project)


def create_project_parts(project, git_hook, **kwargs):
    # check for modules existing
    check_mask = duplication_check(project)
    MODULE_FUNCTIONS = dict(inspect.getmembers(ModuleFunctions, predicate=inspect.isfunction))

    for mask in check_mask:
            MODULE_FUNCTIONS[mask](project)

    if git_hook:
        if os.path.basename(os.getcwd()) == project.repo_name:
            copy_to = os.path.join(os.getcwd(), '.git', 'hooks', 'post-commit')
        else:
            copy_to = os.path.join(os.getcwd(), project.repo_name, '.git', 'hooks', 'post-commit')

        shutil.copy(pkg_resources.resource_filename(__name__, Paths.PACKAGE_GIT_HOOK_PATH), copy_to)


def listing(**kwargs):
    projects = Project.load_projects()
    if projects:
        headers = vars(next(iter(projects.values()))).keys()
        headers = [h[1:] for h in headers]
        projects = [list(vars(p).values()) for p in projects.values()]
        print(tabulate(projects, headers=headers))
    else:
        print("There are no cobra projects! Use the 'create' command to create some projects.")


def remove(name, folder, repo, conda, remove_all, **kwargs):
    # remove the project from the project file
    try:
        Project.project_exists(name)
        print("Project does not exist")
        if not kwargs['test']:
            sys.exit(1)
    except ProjectNameAlreadyExists:
        project = Project.remove_project(name)
        print("Successfully removed cobra project {} from the project file".format(name))

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
                print('Permission problem, please reinstall cobra (--clean; --install)')

    if folder:
        delete_path(project.project_path)
        print("Successfully removed folders")
    else:
        delete_path(os.path.join(project.project_path, ".cobra"))
        print("Removed .cobra file")

    if conda:
        if check_env_exists(project.conda_name):
            try:
                # remove env
                subprocess.check_output(['conda', 'env', 'remove', '-y', '--name', project.conda_name])
                print("Successfully removed conda environment")
            except subprocess.CalledProcessError:
                print('Environment was not deactivated!')
                print('Remove the environment by hand with the following command:\n')
                print('conda deactivate\n')
                print('conda env remove --name ' + project.conda_name + '-y')
                print('\n')
        else:
            print("Conda environment does not exist")


def entry_point():
    main()


if __name__ == '__main__':
    entry_point()
