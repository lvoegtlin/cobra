from pocr.connenction_types import ConnectionType


class VCS:

    def __init__(self, name, values):
        self.name = name
        self.connection_types = self.__init_connection_types(values['connection_types'])
        self.token_create_url = values['token_url']

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

    @property
    def token_create_url(self):
        return self._token_create_url

    @token_create_url.setter
    def token_create_url(self, value):
        self._token_create_url = value

    def __init_connection_types(self, connection_types):
        con_type_list = []
        for name, url in connection_types.items():
            con_type_list.append(ConnectionType(name, url))
        return con_type_list
