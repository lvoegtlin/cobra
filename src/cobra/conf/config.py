import copy
import yaml
import keyring
import pkg_resources

from src.cobra.utils.constants import Paths
from src.cobra.vcs import VCS


class Config(yaml.YAMLObject):
    __instance = None
    yaml_tag = u'!Config'

    def __init__(self, _used_vcs=None, _connection_type=None, _username=''):
        if Config.__instance:
            self.getInstance()
        self.vcses = []
        self.used_vcs = _used_vcs
        self.connection_type = _connection_type
        self.user_password_domain = "cobra_user_sec"
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

    # PRIVATE
    def __load_vcs(self):
        vcs = pkg_resources.resource_string(__name__, Paths.PACKAGE_VCS_PATH)
        yaml_file = yaml.safe_load_all(vcs.decode('UTF-8'))
        for vcs_list in yaml_file:
            for k, v in vcs_list.items():
                self._vcses.append(VCS(k, v['connection_types']))

    def __load_user_cred(self):
        self._sec = keyring.get_password(self.user_password_domain, self.username)

    # PUBLIC
    def save_user_cred(self):
        keyring.set_password(self.user_password_domain, self.username, self.sec)

    def load_config(self):
        with open(Paths.CONF_FILE_PATH, 'r') as f:
            config = yaml.load(f, Loader=yaml.Loader)
            self.connection_type = config.connection_type
            self.used_vcs = config.used_vcs
            self.username = config.username

            self.__load_vcs()
            self.__load_user_cred()

    def save_config(self):
        self.save_user_cred()
        with open(Paths.CONF_FILE_PATH, 'w') as f:
            obj_copy = copy.deepcopy(self.getInstance())
            del obj_copy._sec
            del obj_copy._vcses
            del obj_copy.user_password_domain
            yaml.dump(obj_copy, f)


if __name__ == '__main__':
    t = Config.getInstance()
    t.write_into_config(**{'test': 'test'})
