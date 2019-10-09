import os


class Paths:

    POCR_FOLDER = os.path.expanduser("~/.pocr")
    CONF_FILE_PATH = os.path.join(POCR_FOLDER, "config")
    PROJECT_FILE_PATH = os.path.join(POCR_FOLDER, "projects")


class Structures:
    # default yaml structure for the config file
    AUTH_SCOPES = ['repo', 'delete_repo']


class Texts:
    VCS_SELECT_TEXT = "Chose the vcs hoster you want to use (for all projects)"
    CON_SELECT_TEXT = "Select the connection type:"
    USERNAME_TEXT = "Enter your username (of the VCS host)"
    PASSWORD_TEXT = "Enter your password (of the VCS host)"
    AUTH_TEXT = "What kind of Authentication do you want to use: (if 2FA chose token)"
    TOKEN_TEXT = "Enter the token"
    TFA_TEXT = "Enter the 2FA token"
