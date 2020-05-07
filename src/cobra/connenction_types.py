import yaml


class ConnectionType(yaml.YAMLObject):
    yaml_tag = u'!ConnectionType'

    def __init__(self, _name, _url):
        self.name = _name
        self.url = _url

    # GETTERS / SETTERS
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
