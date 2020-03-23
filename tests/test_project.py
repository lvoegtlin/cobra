import os

from src.cobra.project import Project


class TestProject:
    def test_create_project_file(self, tmp_path):
        project_path = tmp_path
        project_name = "projectName"
        conda_name = "condaName"
        repo_name = "repoName"
        repo_user = "repoUser"
        vcs = None
        python_version = 3.6

        # create project folder
        complete_path = project_path / project_name
        complete_path.mkdir()
        project = Project(project_path.__str__(), project_name, conda_name, repo_name, repo_user, vcs, python_version)

        project.create_project_file()
        assert os.path.exists((complete_path / '.cobra').__str__())
        assert os.stat((complete_path / '.cobra').__str__()).st_size != 0

    def test_project_from_file(self, tmp_path, monkeypatch):
        content = """!Project
                    _conda_name: condaName
                    _project_name: projectName
                    _python_version: 3.6
                    _repo_name: repoName
                    _repo_user: repoUser
                    _vcs: null"""

        project_file_path = tmp_path / ".cobra"
        project_file_path.write_text(content)

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

