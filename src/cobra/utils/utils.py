import json
import os
import shutil
import subprocess
import sys

from PyInquirer import prompt
from github import Github, GithubException, UnknownObjectException
from src.cobra.conf.config import Config
from src.cobra.utils.constants import Texts, Structures, Paths


def get_object_from_list_by_name(filter_str, input_list):
    return next(filter(lambda x: filter_str in x.name, input_list), None)


def build_question(interface_type: str, message: str, name: str, iter_list: list):
    question = {
        'type': interface_type,
        'name': name,
        'message': message,
    }

    if interface_type == 'list':
        if type(iter_list[0]) == str:
            choices = iter_list
        else:
            choices = [item.name for item in iter_list]
        question['choices'] = choices

    return question


def ask_questions(types: list, messages: list, names: list, iter_list: list):
    questions = [build_question(t, m, n, l) for t, m, n, l in zip(types, messages, names, iter_list)]
    return prompt(questions)


def check_env_exists(name):
    # execute command
    envs = subprocess.check_output(['conda', 'env', 'list', '--json']).decode('utf-8')
    # create a dict
    envs = json.loads(envs.replace('\n', ''))['envs']
    # just get the basename of the conda env path
    envs = [os.path.basename(e) for e in envs]
    if name in envs:
        return True
    return False


def dialog_username_password():
    # username and password
    username_password = ask_questions(['input', 'password'],
                                      [Texts.USERNAME_TEXT, Texts.PASSWORD_TEXT],
                                      ['username', 'password'],
                                      [[], []])
    username = username_password['username']
    password = username_password['password']
    github = Github(login_or_token=username, password=password)
    return github, username, password


def user_password_dialog(error=None):
    if error is None:
        error = {}
    try:
        if not error:
            github, username, password = dialog_username_password()
            auth = github.get_user().create_authorization(scopes=Structures.AUTH_SCOPES,
                                                          note='cobra')
        else:
            if error['key'] == 0:
                print(error['message'])
                github, username, password = dialog_username_password()
                auth = github.get_user().create_authorization(scopes=Structures.AUTH_SCOPES,
                                                              note='cobra')

            if error['key'] == 1:
                print(error['message'])
                github, username, password = error['cred']
                tfa = ask_questions(['input'], [Texts.TFA_TEXT], ['tfa'], [[]])['tfa']
                auth = github.get_user().create_authorization(scopes=Structures.AUTH_SCOPES,
                                                              onetime_password=tfa,
                                                              note='cobra')

        sec = auth.token or ""
        github = Github(sec)

        # to test if the github object has a correct authentication
        github.get_user().id

        Config.getInstance().username = username
        Config.getInstance().sec = sec
    except GithubException as e:
        error_msg = {}
        if e.status == 422:
            error_msg['message'] = Texts.TOKEN_ALREADY_EXISTS_TEXT
            error_msg['key'] = 1
        if e.status == 401:
            if e.data['message'] == 'Bad credentials':
                error_msg['key'] = 0
            else:
                error_msg['key'] = 1
            error_msg['message'] = e.data['message']
        error_msg['cred'] = (github, username, password)
        return error_msg


def duplication_check(project):
    # [repo, pull, conda]
    res = []
    None if check_repo_exists('/'.join([project.repo_user, project.repo_name])) else res.append('create_repo')
    None if check_git_pull() else res.append('pull_repo')
    None if check_env_exists(project.conda_name) else res.append('create_environment')
    return res


def check_git_pull():
    return os.path.exists(os.path.join(os.getcwd(), '.git'))


def check_repo_exists(full_repo_name):
    try:
        Github().get_repo(full_repo_name)
    except UnknownObjectException:
        return False
    except GithubException:
        return False
    return True


def create_files_folders():
    # create folder
    os.mkdir(Paths.COBRA_FOLDER)

    # create conf file
    open(Paths.CONF_FILE_PATH, 'a').close()
    # Config.getInstance().write_into_yaml_file(Constants.CONF_FILE_PATH, **Constants.CONF_DICT)
    # project file {'TestProject': {infos}}
    open(Paths.PROJECT_FILE_PATH, 'a').close()


def check_requirements():
    if shutil.which("conda") is None:
        raise Exception(
            "Conda is not installed! https://docs.conda.io/projects/conda/en/latest/user-guide/install/")
    if sys.version_info[0] < 3 and sys.version_info[1] < 5:
        raise Exception("The default python version is lower then 3.5. Please update!")


def first_usage():
    """
    Checks if the pocr config file is existing.
    If this file is existing we know that it is not first usage and so the function returns false.
    Else vise versa.

    :return:
        boolean: if its first usage or not
    """
    return not os.path.exists(Paths.COBRA_FOLDER)


def get_github_user():
    # get github user
    github = Github(Config.getInstance().sec)
    user = github.get_user()
    return user


def delete_path(path: str):
    # check if path is pointing to a file or folder
    if os.path.exists(path):
        try:
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
        except PermissionError:
            print("Permission error for deleting the folder."
                  " Please delete it by hand or try again.")
