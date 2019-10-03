from PyInquirer import prompt


def get_object_from_list_by_name(filter_str, list):
    return next(filter(lambda x: filter_str in x.name, list), None)


def build_question(iter_list: list, message: str, name: str):
    choices = [item.name for item in iter_list]
    question = {
                'type': 'list',
                'name': name,
                'message': message,
                'choices': choices,
                }

    return question


def ask_questions(iter_list: list, messages: list, names: list):
    questions = [build_question(l, m, n) for l, m, n in zip(iter_list, messages, names)]
    return prompt(questions)
