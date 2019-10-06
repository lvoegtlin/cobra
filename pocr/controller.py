from __future__ import print_function, unicode_literals

import git
from github import Github

from pocr.conf.config import Config
from pocr.constants import Constants
from pocr.utils.command_line import get_params
from pocr.utils.utils import get_object_from_list_by_name, ask_questions

import subprocess
import shutil
import sys
import os


def main():
    # read args
    args = get_params()
    
    # requirements check
    check_requirements()

    if args.install:
        if first_usage():
            run_installation()
            print('POCR successfully installed!')
        else:
            print("POCR is already installed!")

    if args.command == 'create':
        create_project(**args.__dict__)

    if args.test:
        subprocess.run("./pocr/clean.sh", shell=True)


def create_project(name, python_version, git_hook, **kwargs):
    # load config
    load_config()
    # create git repo
    if not kwargs['test']:
        github = Github(Config.getInstance().sec)
        user = github.get_user()
        user.create_repo(name, auto_init=True)

        # pull repo
        cwd = os.getcwd()
        git_url = "{}{}/{}.git".format(Config.getInstance().connection_type.url, Config.getInstance().username, name)
        git.Git(cwd).clone(git_url)
        # create conda
        arguments = ["--name", name]
        if python_version:
            arguments.append("python={}".format(python_version))
        # can not use conda api because it does not work
        os.system("conda create {}".format(' '.join(arguments)))

        if git_hook:
            shutil.copy('./pocr/utils/pre-commit', os.path.join(os.getcwd(), '.git', 'hooks', 'pre-commit'))


def load_config():
    # load config
    Config.getInstance().load_config()


def first_usage():
    """
    Checks if the pocr config file is existing.
    If this file is existing we know that it is not first usage and so the function returns false.
    Else vise versa.

    :return:
        boolean: if its first usage or not
    """
    return not os.path.exists(Constants.POCR_FOLDER)


# install wizard
def run_installation():
    """
    With this method the user installs the tool. That means he creates the config and the project file,
    enters the user credentials as well as defines the connection type.
    """

    # ask for the vcs which are stored in the vc.yml file
    vcs_selection = ask_questions(['list'], [Constants.VCS_SELECT_TEXT], ['vcs'], [Config.getInstance().vcses])
    used_vcs = Config.getInstance().used_vcs = get_object_from_list_by_name(vcs_selection['vcs'],
                                                                            Config.getInstance().vcses)

    # finish vcs install (ssh http selection; TODO: username and password or token)
    auth_selection = ""
    while auth_selection != "Token":
        if auth_selection == 'Username/Password':
            print("username/password option not availabe at the moment")
        # chose for toke or user/password
        auth_selection = ask_questions(['list'], [Constants.AUTH_TEXT], ['auth'], [['Username/Password', 'Token']])
        auth_selection = auth_selection['auth']

    # if token
    if auth_selection == 'Token':
        print("If you dont have a token, create one here {}".format(used_vcs.token_create_url))
        username_token = ask_questions(['input', 'input'],
                                       [Constants.USERNAME_TEXT, Constants.TOKEN_TEXT],
                                       ['username', 'token'],
                                       [[], []])
        Config.getInstance().username = username_token['username']
        Config.getInstance().sec = username_token['token']
        Config.getInstance().save_user_cred()
    # else
    else:
        username_password = ask_questions(['input', 'password'],
                                          [Constants.USERNAME_TEXT, Constants.PASSWORD_TEXT],
                                          ['username', 'password'],
                                          [[], []])
        Config.getInstance().username = username_password['username']
        Config.getInstance().password = username_password['password']

    con_selection = ask_questions(['list'], [Constants.CON_SELECT_TEXT], ['con_type'], [used_vcs.connection_types])
    Config.getInstance().connection_type = get_object_from_list_by_name(con_selection['con_type'],
                                                                        used_vcs.connection_types)

    # create files and folders
    create_files_folders()

    # save infos
    Config.getInstance().save_config()


def create_files_folders():
    # create folder
    os.mkdir(Constants.POCR_FOLDER)

    # create conf file
    open(Constants.CONF_FILE_PATH, 'a').close()
    # Config.getInstance().write_into_yaml_file(Constants.CONF_FILE_PATH, **Constants.CONF_DICT)
    # project file {'TestProject': {infos}}
    open(Constants.PROJECT_FILE_PATH, 'a').close()


def check_requirements():
    if shutil.which("conda") is None:
        raise Exception(
            "Conda is not installed! https://docs.conda.io/projects/conda/en/latest/user-guide/install/")
    if sys.version_info[0] < 3 and sys.version_info[1] < 5:
        raise Exception("The default python version is lower then 3.5. Please update!")


def entry_point():
    main()


if __name__ == '__main__':
    entry_point()
