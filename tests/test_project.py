import os
from pathlib import Path

import pytest
from src.cobra.project import Project
from src.cobra.utils.constants import Paths
from src.cobra.utils.exceptions import ProjectNameAlreadyExists

from tests.utils.utils import create_mock_cobra_file, create_mock_project


class TestProject:
    def test_create_project_file(self, tmp_path):
        project = create_mock_project(tmp_path)

        # create project folder
        complete_path = Path(project.project_path)
        complete_path.mkdir()

        project.create_project_file()
        assert os.path.exists((complete_path / '.cobra').__str__())
        assert os.stat((complete_path / '.cobra').__str__()).st_size != 0

    def test_project_from_file(self, tmp_path, monkeypatch):
        create_mock_cobra_file(tmp_path)

        monkeypatch.chdir(tmp_path)
        project = Project.project_from_file()
        project.project_path = (tmp_path / project.project_name).__str__()

        assert project.project_path == (tmp_path / 'projectName').__str__()
        assert project.project_name == "projectName"
        assert project.python_version == 3.6
        assert project.repo_name == "repoName"
        assert project.repo_user == "repoUser"
        assert project.vcs is None
        assert project.__repr__() == "{}\t{}\t{}\t{}".format("projectName", 'condaName', None, 3.6)

    def test_append_project(self, tmp_path, monkeypatch):
        project_file_path = tmp_path / "project"
        monkeypatch.setattr(Paths, 'PROJECT_FILE_PATH', project_file_path.__str__())
        project_file_path.write_text("")

        project = create_mock_project(tmp_path)
        project.append_project()

        with pytest.raises(ProjectNameAlreadyExists) as exp:
            Project.project_exists(project.project_name)

        assert os.stat(project_file_path.__str__()).st_size != 0
        assert exp.type is ProjectNameAlreadyExists

    def test_remove_project(self, tmp_path, monkeypatch):
        project_file_path = tmp_path / "project"
        monkeypatch.setattr(Paths, 'PROJECT_FILE_PATH', project_file_path.__str__())
        project_file_path.write_text("")
        create_mock_project(project_file_path).append_project()

        project = Project.remove_project("projectName")

        assert os.stat(project_file_path.__str__()).st_size == 0
        assert type(Project.project_exists(project.project_name)) == dict

    def test_get_projects_empty(self, tmp_path, monkeypatch):
        project_file_path = tmp_path / "project"
        monkeypatch.setattr(Paths, 'PROJECT_FILE_PATH', project_file_path.__str__())
        project_file_path.write_text("")

        assert Project.get_projects() is None

    def test_get_projects(self, tmp_path, monkeypatch):
        project_file_path = tmp_path / "project"
        monkeypatch.setattr(Paths, 'PROJECT_FILE_PATH', project_file_path.__str__())
        project_file_path.write_text("")
        create_mock_project(project_file_path).append_project()

        projects = Project.get_projects()
        project = projects['projectName']

        assert projects is not None
        assert project.project_name == 'projectName'
        assert project.conda_name == 'condaName'
        assert project.project_path == (project_file_path / 'projectName').__str__()
        assert project.python_version == 3.6
        assert project.repo_name == 'repoName'
        assert project.repo_user == 'repoUser'
        assert project.vcs is None

    def test_project_exists_not(self, tmp_path, monkeypatch):
        project_file_path = tmp_path / "project"
        monkeypatch.setattr(Paths, 'PROJECT_FILE_PATH', project_file_path.__str__())
        project_file_path.write_text("")

        assert os.stat(project_file_path.__str__()).st_size == 0
        assert Project.project_exists("projectName") == {}

    def test_project_exists(self, tmp_path, monkeypatch):
        project_file_path = tmp_path / "project"
        monkeypatch.setattr(Paths, 'PROJECT_FILE_PATH', project_file_path.__str__())
        project_file_path.write_text("")
        create_mock_project(project_file_path).append_project()

        with pytest.raises(ProjectNameAlreadyExists) as exp:
            print(Project.project_exists("projectName"))

        assert os.stat(project_file_path.__str__()).st_size != 0
        assert exp.type == ProjectNameAlreadyExists
