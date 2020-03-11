from cobra.conf.config import Config
from cobra.utils.utils import first_usage, check_git_pull, create_files_folders, delete_path
from cobra.utils.constants import Paths


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


class TestConfig:
    def test_get_instance(self):
        config1 = Config.getInstance()
        config2 = Config.getInstance()
        assert config1 == config2

    def test_load_config(self, tmp_path, monkeypatch):
        config_content = """!Config
                            _connection_type: &id001 !ConnectionType
                              _name: ssh
                              _url: 'git@github.com:'
                            _used_vcs: !VCS
                              _connection_types:
                              - !ConnectionType
                                _name: https
                                _url: https://github.com/
                              - *id001
                              _name: Github
                            _username: testUser"""

        conf_file_path = tmp_path / "config"
        conf_file_path.write_text(config_content)

        monkeypatch.setattr(Paths, "CONF_FILE_PATH", conf_file_path.__str__())

        conf = Config.getInstance()
        # overwrite the cred loading by a empty method
        conf.__load_user_cred = lambda: ""

        conf.load_config()
        conf._sec = "testSec"
        assert conf.used_vcs.name == "Github"
        assert conf.connection_type.name == "ssh"
        assert conf.connection_type.url == "git@github.com:"
        assert conf.username == "testUser"
        assert conf._sec == "testSec"

    def test_save_config(self):
        assert False

