import copy
import inspect
import os
import shutil

import pkg_resources
import yaml
from src.cobra.utils.constants import Paths
from src.cobra.utils.exceptions import ProjectNameAlreadyExists, NoCobraFileFound
from src.cobra.utils.module_functions import ModuleFunctions
from src.cobra.utils.utils import duplication_check


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

    def create_project_file(self):
        with open(os.path.join(self.project_path, ".cobra"), 'w') as f:
            obj_copy = copy.deepcopy(self)
            del obj_copy._project_path
            yaml.dump(obj_copy, f)

    def append_project(self):
        yaml_dict = Project.project_exists(self.project_name)
        yaml_dict[self.project_name] = self
        with open(Paths.PROJECT_FILE_PATH, 'a') as f:
            yaml.dump(yaml_dict, f)

    # STATIC
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
    def get_projects():
        with open(Paths.PROJECT_FILE_PATH, 'r') as f:
            return yaml.load(f, Loader=yaml.Loader) or None

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
            raise NoCobraFileFound()
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

    @staticmethod
    def create_project_parts(project, git_hook, **kwargs):
        # check for modules existing
        check_mask = duplication_check(project)
        MODULE_FUNCTIONS = dict(inspect.getmembers(ModuleFunctions, predicate=inspect.isfunction))

        for mask in check_mask:
            MODULE_FUNCTIONS[mask](project)

        if git_hook:
            copy_to = os.path.join(project.project_path, '.git', 'hooks', 'post-commit')
            shutil.copy(pkg_resources.resource_filename(__name__, Paths.PACKAGE_GIT_HOOK_PATH), copy_to)
