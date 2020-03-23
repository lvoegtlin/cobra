import os

from src.cobra.conf.config import Config
from src.cobra.connenction_types import ConnectionType
from src.cobra.utils.constants import Paths


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

        conf_file_path = tmp_path / "load_config"
        conf_file_path.write_text(config_content)

        monkeypatch.setattr(Paths, "CONF_FILE_PATH", conf_file_path.__str__())

        conf = Config.getInstance()

        conf.load_config()
        conf._sec = "testSec"
        assert conf.used_vcs.name == "Github"
        assert conf.connection_type.name == "ssh"
        assert conf.connection_type.url == "git@github.com:"
        assert conf.username == "testUser"
        assert conf._sec == "testSec"
        assert conf.vcses[0].name == "Github"
        conf.used_vcs = None

    def test_save_config(self, tmp_path, monkeypatch):
        conf = Config.getInstance()

        conf_file_path = tmp_path / "save_config"

        conf.username = "Test"
        conf.connection_type = ConnectionType("TestConType", "TestUrl")

        monkeypatch.setattr(Paths, "CONF_FILE_PATH", conf_file_path.__str__())

        conf.save_config()

        assert os.path.exists(conf_file_path.__str__())

        import yaml
        with open(conf_file_path.__str__(), 'r') as f:
            config = yaml.load(f, Loader=yaml.Loader)
            assert config.username == "Test"
            assert config.connection_type.name == "TestConType"
            assert config.connection_type.url == "TestUrl"
            assert config.used_vcs is None
