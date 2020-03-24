from src.cobra.project import Project


def create_mock_cobra_file(path):
    content = """!Project
                _conda_name: condaName
                _project_name: projectName
                _python_version: 3.6
                _repo_name: repoName
                _repo_user: repoUser
                _vcs: null"""

    project_file_path = path / ".cobra"
    project_file_path.write_text(content)


def create_mock_project(path):
    project_path = path
    project_name = "projectName"
    conda_name = "condaName"
    repo_name = "repoName"
    repo_user = "repoUser"
    vcs = None
    python_version = 3.6

    return Project(project_path.__str__(), project_name, conda_name, repo_name, repo_user, vcs, python_version)
