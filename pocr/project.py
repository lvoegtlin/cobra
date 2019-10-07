import yaml


def load_projects():
    pass


def save_project():
    pass


class Project(yaml.YAMLObject):
    yaml_tag = u'!Project'

    def __init__(self, path=None, name=None, conda_name=None, vcs=None, python=None):
        self.path = path
        self.name = name
        self.conda_name = conda_name
        self.vcs = vcs
        self.python = python

    def __repr__(self):
        return "{}\t{}\t{}\t{}".format(self.name, self.conda_name, self.vcs, self.python)
