from src.cobra.utils.utils import first_usage, check_git_pull, create_files_folders, delete_path
from src.cobra.utils.constants import Paths


class TestUtils:
    def test_not_first_usage(self, tmp_path, monkeypatch):
        cobra_home_dir = tmp_path / ".cobra"
        cobra_home_dir.mkdir()
        monkeypatch.setattr(Paths, "COBRA_FOLDER", cobra_home_dir)
        assert not first_usage()

    def test_first_usage(self, tmp_path, monkeypatch):
        cobra_home_dir = tmp_path / ".cobra"
        monkeypatch.setattr(Paths, "COBRA_FOLDER", cobra_home_dir)
        assert first_usage()

    def test_check_git_pull(self, tmp_path, monkeypatch):
        git_home_dir = tmp_path / ".git"
        git_home_dir.mkdir()

        monkeypatch.setattr("os.getcwd", lambda: tmp_path.__str__())
        assert check_git_pull()

    def test_check_git_not_pull(self, tmp_path, monkeypatch):
        monkeypatch.setattr("os.getcwd", lambda: tmp_path.__str__())
        assert not check_git_pull()

    def test_create_files_folders(self, tmp_path, monkeypatch):
        import os
        cobra_home_dir = tmp_path / ".cobra"
        monkeypatch.setattr(Paths, "COBRA_FOLDER", cobra_home_dir)
        monkeypatch.setattr(Paths, "CONF_FILE_PATH", cobra_home_dir / "config")
        monkeypatch.setattr(Paths, "PROJECT_FILE_PATH", cobra_home_dir / "projects")
        create_files_folders()

        cobra_path = (tmp_path / ".cobra").__str__()
        # checks folder exists
        assert os.path.exists(cobra_path)
        # checks project files exists
        assert os.path.exists(os.path.join(cobra_path, "projects"))
        # checks config files exists
        assert os.path.exists(os.path.join(cobra_path, "config"))

    def test_delete_path_folder(self, tmp_path):
        import os
        dummy_folder = tmp_path / "dummy"
        dummy_folder.mkdir()
        assert os.path.exists(dummy_folder.__str__())
        delete_path(dummy_folder.__str__())
        assert not os.path.exists(dummy_folder.__str__())

    def test_delete_path_file(self, tmp_path):
        import os
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.mkdir()
        assert os.path.exists(dummy_file.__str__())
        delete_path(dummy_file.__str__())
        assert not os.path.exists(dummy_file.__str__())
