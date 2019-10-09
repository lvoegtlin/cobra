import subprocess
import json

from PyInquirer import prompt
from github import Github, GithubException

from pocr.conf.config import Config
from pocr.constants import Texts, Structures
from pocr.utils.exceptions import CondaAlreadyExists


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
    envs = subprocess.check_output(['conda', 'env', 'list', '--json']).decode('utf-8')
    envs = json.loads(envs.replace('\n', ''))
    if name not in envs:
        raise CondaAlreadyExists()


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
        else:
            if error['key'] == 0:
                print(error['message'])
                github, username, password = dialog_username_password()
                usr = github.get_user()
                sec = usr.get_authorization(usr.id)
                github = Github(sec)

            if error['key'] == 1:
                print(error['message'])
                github, username, password = error['cred']
                tfa = ask_questions(['input'], [Texts.TFA_TEXT], ['tfa'], [[]])['tfa']
                auth = github.get_user().create_authorization(scopes=Structures.AUTH_SCOPES,
                                                              onetime_password=tfa,
                                                              note='pocr')
                sec = auth.token
                github = Github(auth.token)

            # to test if the github object has a correct authentication
        github.get_user().id

        Config.getInstance().username = username
        Config.getInstance().sec = sec
    except GithubException as e:
        error_msg = {}
        if e.data['message'] == 'Bad credentials':
            error_msg['key'] = 0
        else:
            error_msg['key'] = 1
        error_msg['message'] = e.data['message']
        error_msg['cred'] = (github, username, password)
        return error_msg


if __name__ == '__main__':
    check_env_exists('ICDAR_Tutorial')
