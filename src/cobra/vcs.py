import yaml

from src.cobra.connenction_types import ConnectionType


class VCS(yaml.YAMLObject):
    yaml_tag = u'!VCS'

    def __init__(self, name, connection_types):
        self.name = name
        self.connection_types = self.__init_connection_types(connection_types)

    def __repr__(self):
        return "{}".format(self.name)

    # GETTERS / SETTERS

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def connection_types(self):
        return self._connection_types

    @connection_types.setter
    def connection_types(self, value):
        self._connection_types = value

    @staticmethod
    def __init_connection_types(connection_types):
        con_type_list = []
        for name, url in connection_types.items():
            con_type_list.append(ConnectionType(name, url))
        return con_type_list
