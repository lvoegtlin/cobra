import os


class Paths:
    COBRA_FOLDER = os.path.expanduser("~/.cobra")
    CONF_FILE_PATH = os.path.join(COBRA_FOLDER, "config")
    PROJECT_FILE_PATH = os.path.join(COBRA_FOLDER, "projects")
    PACKAGE_VCS_PATH = os.path.sep + 'vcs.yml'
    PACKAGE_GIT_HOOK_PATH = os.path.join('utils', 'post-commit')


class Structures:
    # default yaml structure for the config file
    AUTH_SCOPES = ['repo', 'delete_repo']


class Texts:
    VCS_SELECT_TEXT = "Chose the vcs host you want to use (for all projects)"
    CON_SELECT_TEXT = "Select the connection type:"
    USERNAME_TEXT = "Enter your username (of the VCS host)"
    PASSWORD_TEXT = "Enter your password (of the VCS host)"
    AUTH_TEXT = "What kind of Authentication do you want to use: (if 2FA chose token)"
    TOKEN_TEXT = "Enter the token"
    TFA_TEXT = "Enter the 2FA token"
    TOKEN_ALREADY_EXISTS_TEXT = "Token already exists. Please delete the token (https://github.com/settings/tokens)"
