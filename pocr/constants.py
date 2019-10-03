import os


class Constants:

    POCR_FOLDER = os.path.expanduser("~/.pocr")
    CONF_FILE_PATH = os.path.join(POCR_FOLDER, "config")
    PROJECT_FILE_PATH = os.path.join(POCR_FOLDER, "projects")

    # default yaml structure for the config file
    CONF_DICT = {'vcs_name': None,
                 'connection_type': 'https',
                 'username': None,
                 'token_domain': None,
                 'password_domain': None}

    # ------------------------

    VCS_SELECT_TEXT = "Chose the vcs you want to use (for all projects)"
    CON_SELECT_TEXT = "Select the connection type:"
