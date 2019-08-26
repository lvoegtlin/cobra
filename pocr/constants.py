import os


class Constants:

    POCR_FOLDER = os.path.expanduser("~/.pocr")
    CONF_FILE_PATH = os.path.join(POCR_FOLDER, "config")
    PROJECT_FILE_PATH = os.path.join(POCR_FOLDER, "projects")
