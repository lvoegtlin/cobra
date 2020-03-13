import os

import git

from src.cobra.conf.config import Config
from src.cobra.utils.utils import get_github_user


class ModuleFunctions:

    @staticmethod
    def pull_repo(project):
        # pull repo
        print("Pulling the repo...")
        cwd = os.getcwd()
        git_url = "{}{}/{}.git".format(Config.getInstance().connection_type.url, Config.getInstance().username,
                                       project.repo_name)
        git.Git(cwd).clone(git_url)
        print("Pulling done")

    @staticmethod
    def create_repo(project):
        print("Creating a repo...")
        user = get_github_user()
        user.create_repo(project.repo_name, auto_init=True)
        print("Repo creation successful")

    @staticmethod
    def create_environment(project):
        # create conda
        print("Creating conda environment...")
        if os.path.exists(os.path.join(project.project_path, "environment.yml")):
            print("Found environment.yml file...")
            arguments = ["env", "create", "-f", os.path.join(project.project_path, "environment.yml")]
        else:
            arguments = ["create", "-y", "--name", project.conda_name, "python={}".format(project.python_version)]
        # can not use conda api because it does not work
        os.system("conda {}".format(' '.join(arguments)))
