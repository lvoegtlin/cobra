import yaml
import keyring

from pocr.constants import Constants
from pocr.vcs import VCS


class Settings:

    __instance = None

    def __init__(self):
        if Settings.__instance:
            self.getInstance()
        self.vcses = []
        self.used_vcs = None
        self.connection_type = None
        self.user_password_domain = "pocr_user_pass"
        self.token_domain = "pocr_token"
        self.username = ''

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = Settings()
        return cls.__instance

    @property
    def vcses(self):
        if not self._vcses:
            self.__load_vcs()
        return self._vcses

    def __load_vcs(self):
        with open("./pocr/conf/vcs.yml", 'r') as vcs:
            yaml_file = yaml.safe_load_all(vcs)
            for vcs_list in yaml_file:
                for k, v in vcs_list.items():
                    self._vcses.append(VCS(k, v['connection_types']))

    @property
    def used_vcs(self):
        return self._used_vcs

    @used_vcs.setter
    def used_vcs(self, value):
        self._used_vcs = value

    @property
    def connection_type(self):
        return self._connection_type

    @connection_type.setter
    def connection_type(self, value):
        self._connection_type = value

    @vcses.setter
    def vcses(self, value):
        self._vcses = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    def save_user_cred(self, username, password):
        keyring.set_password(self.user_password_domain, username, password)

    def save_auth_token(self, token):
        keyring.set_password(self.token_domain, "token", token)

    def write_into_yaml_file(self, file_path, **kwargs: dict):
        assert kwargs
        with open(file_path, 'r') as f:
            yaml_dict = yaml.safe_load(f) or {}
        yaml_dict.update(kwargs)
        with open(file_path, 'w') as f:
            yaml.dump(yaml_dict, f)

    def save_config(self):
        config_dict = {'vcs_name': self.used_vcs,
                       'connection_type': self.connection_type,
                       'username': self.username,
                       'token_domain': self.token_domain,
                       'password_domain': self.user_password_domain}
        self.write_into_yaml_file(Constants.CONF_FILE_PATH, **config_dict)


if __name__ == '__main__':
    t = Settings.getInstance()
    t.write_into_config(**{'test': 'test'})
