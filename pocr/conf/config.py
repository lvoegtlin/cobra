import copy

import yaml
import keyring

from pocr.constants import Constants
from pocr.vcs import VCS


class Config(yaml.YAMLObject):

    __instance = None
    yaml_tag = u'!Config'

    def __init__(self, _used_vcs=None, _connection_type=None, _username=''):
        if Config.__instance:
            self.getInstance()
        self.vcses = []
        self.used_vcs = _used_vcs
        self.connection_type = _connection_type
        self.user_password_domain = "pocr_user_sec"
        self.username = _username
        self.sec = ''


    # GETTER / SETTER
    @property
    def vcses(self):
        if not self._vcses:
            self.__load_vcs()
        return self._vcses

    @vcses.setter
    def vcses(self, value):
        self._vcses = value

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

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def sec(self):
        return self._sec

    @sec.setter
    def sec(self, value):
        self._sec = value

    # STATIC / CLASS
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = Config()
        return cls.__instance

    def write_into_yaml_file(self, file_path):
        with open(file_path, 'w') as f:
            obj_copy = copy.deepcopy(self.getInstance())
            del obj_copy._sec
            del obj_copy._vcses
            del obj_copy.user_password_domain
            yaml.dump(obj_copy, f)

    # PRIVATE
    def __load_vcs(self):
        with open("./pocr/conf/vcs.yml", 'r') as vcs:
            yaml_file = yaml.safe_load_all(vcs)
            for vcs_list in yaml_file:
                for k, v in vcs_list.items():
                    self._vcses.append(VCS(k, v['connection_types'], v['token_url']))

    # PUBLIC
    def save_user_cred(self, username, sec):
        self._username = username
        self._sec = sec
        keyring.set_password(self.user_password_domain, username, sec)

    def save_config(self):
        self.write_into_yaml_file(Constants.CONF_FILE_PATH)

    def load_config(self):
        with open(Constants.CONF_FILE_PATH, 'r') as f:
            config = yaml.load(f, Loader=yaml.Loader)
            for k, v in config.items():
                self.getInstance()[k] = v


if __name__ == '__main__':
    t = Config.getInstance()
    t.write_into_config(**{'test': 'test'})