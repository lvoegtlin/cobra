import subprocess
import json

from PyInquirer import prompt

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


if __name__ == '__main__':
    check_env_exists('ICDAR_Tutorial')
