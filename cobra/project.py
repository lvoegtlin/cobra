import os
import yaml

from cobra.utils.constants import Paths
from cobra.utils.exceptions import ProjectNameAlreadyExists, NoCobraFileFound


class Project(yaml.YAMLObject):
    yaml_tag = u'!Project'

    def __init__(self, project_path, project_name, conda_name, repo_name, repo_user, vcs, python_version):
        self.project_path = os.path.join(project_path, project_name)
        self.project_name = project_name
        self.conda_name = conda_name
        self.repo_name = repo_name
        self.repo_user = repo_user
        self.vcs = vcs
        self.python_version = python_version

    def __repr__(self):
        return "{}\t{}\t{}\t{}".format(self._project_name, self._conda_name, self._vcs, self._python_version)

    # STATIC

    @staticmethod
    def load_projects():
        with open(Paths.PROJECT_FILE_PATH, 'r') as f:
            return yaml.load(f, Loader=yaml.Loader) or None

    @staticmethod
    def save_projects(projects: list):
        with open(Paths.PROJECT_FILE_PATH, 'r') as f:
            yaml_dict = yaml.safe_load(f) or {}
        yaml_dict.update(projects)
        with open(Paths.PROJECT_FILE_PATH, 'w') as f:
            yaml.dump(yaml_dict, f)

    @staticmethod
    def create_project_file(project):
        with open(os.path.join(project.project_path, ".cobra"), 'w') as f:
            yaml.dump(project, f)

    @staticmethod
    def append_project(project):
        yaml_dict = Project.project_exists(project.project_name)
        yaml_dict[project.project_name] = project
        with open(Paths.PROJECT_FILE_PATH, 'a') as f:
            yaml.dump(yaml_dict, f)

    @staticmethod
    def remove_project(project_name):
        with open(Paths.PROJECT_FILE_PATH, 'r') as f:
            yaml_dict = yaml.load(f, Loader=yaml.Loader) or {}
        project = yaml_dict[project_name]
        del yaml_dict[project_name]

        if yaml_dict:
            with open(Paths.PROJECT_FILE_PATH, 'w') as f:
                yaml.dump(yaml_dict, f)
        else:
            open(Paths.PROJECT_FILE_PATH, 'w').close()

        return project

    @staticmethod
    def project_exists(project_name: str):
        with open(Paths.PROJECT_FILE_PATH, 'r') as f:
            yaml_dict = yaml.load(f, Loader=yaml.Loader)
        if type(yaml_dict) is not dict:
            return {}
        if project_name in yaml_dict:
            raise ProjectNameAlreadyExists()
        return yaml_dict

    @staticmethod
    def project_from_file():
        # search for the .cobra file
        if os.path.exists(".cobra"):
            with open(".cobra", 'r') as f:
                project = yaml.load(f, Loader=yaml.Loader)
        else:
            raise NoPocrFileFound()
        return project

    # GETTERS / SETTERS

    @property
    def project_path(self):
        return self._project_path

    @project_path.setter
    def project_path(self, value):
        self._project_path = value

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, value):
        self._project_name = value

    @property
    def conda_name(self):
        return self._conda_name

    @conda_name.setter
    def conda_name(self, value):
        self._conda_name = value

    @property
    def vcs(self):
        return self._vcs

    @vcs.setter
    def vcs(self, value):
        self._vcs = value

    @property
    def python_version(self):
        return self._python_version

    @python_version.setter
    def python_version(self, value):
        self._python_version = value

    @property
    def repo_name(self):
        return self._repo_name

    @repo_name.setter
    def repo_name(self, value):
        self._repo_name = value

    @property
    def repo_user(self):
        return self._repo_user

    @repo_user.setter
    def repo_user(self, value):
        self._repo_user = value
