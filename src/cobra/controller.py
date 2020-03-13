import os
import subprocess
import sys

from github import UnknownObjectException
from tabulate import tabulate

from src.cobra.conf.config import Config
from src.cobra.project import Project
from src.cobra.utils.command_line import get_params
from src.cobra.utils.constants import Texts
from src.cobra.utils.exceptions import ProjectNameAlreadyExists
from src.cobra.utils.utils import get_object_from_list_by_name, ask_questions, user_password_dialog, \
    check_requirements, first_usage, get_github_user, check_env_exists, \
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
        installation()
        print('cobra successfully installed!')
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

        if os.path.basename(os.getcwd()) != project.repo_name:
            delete_path(os.path.join(os.getcwd(), '.cobra'))
            project.project_path = os.path.join(os.getcwd(), project.repo_name)
        else:
            project.project_path = os.getcwd()
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
    Project.create_project_parts(project, **kwargs)

    project.create_project_file()

    # save path, conda name, name, git link, python version into project file
    project.append_project()

    print("****************************************************")
    print("****************************************************")
    print("Successfully created project {}".format(project.project_name))
    print("****************************************************")
    print("****************************************************")


def listing(**kwargs):
    projects = Project.get_projects()
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
