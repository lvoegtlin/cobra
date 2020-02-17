import argparse
import sys


def get_params():
    parser = argparse.ArgumentParser(description="Cobra command line tool")
    parser.add_argument("--install", help="Start the installation wizard.", action="store_true")
    parser.add_argument("--test", help="Puts cobra into testing mode", action="store_true")
    parser.add_argument("--clear", help="Clears all user files", action="store_true")
    # TODO option to create the repo private

    subparsers = parser.add_subparsers(help="The different functions of cobra", dest='command')

    # create subcommand
    create_parser = subparsers.add_parser("create", help="Create a new cobra project")
    create_group = create_parser.add_mutually_exclusive_group(required=True)
    create_group.add_argument('-n', '--name',
                              help="Name of the project",
                              type=str)
    create_group.add_argument('-f', '--from-file',
                              help="Searches in the current directory for a .cobra file"
                                   " and creates a project based on this",
                              action="store_true")

    create_parser.add_argument('-p', '--python-version',
                               help="Python version for the project. Default: 3.5",
                               required=False,
                               type=float,
                               default=3.5)
    create_parser.add_argument('-r', '--repo-name',
                               help="If you already have a github repo for the project."
                                    " Enter it in the following format: (username/reponame)",
                               required=False,
                               type=str)
    create_parser.add_argument('-c', '--conda-name',
                               help="If you already have a conda environment for the project. Enter the name.",
                               required=False,
                               type=str)
    create_parser.add_argument('-gh', '--git-hook',
                               help="Does not install a post-commit git hook.",
                               action="store_false")
    # list subcommand
    list_parser = subparsers.add_parser("list", help="Lists all existing cobra projects")

    # # update subcommand
    # update_parser = subparsers.add_parser('update', help="Updates a existing cobra project")

    # remove subcommand
    remove_parser = subparsers.add_parser('remove', help="Remove a cobra project")
    remove_parser.add_argument('-n', '--name',
                               help="Name of the cobra project to remove",
                               required=True,
                               type=str)
    remove_parser.add_argument('-r', '--repo',
                               help="Also removes the remote repository",
                               action="store_true")
    remove_parser.add_argument('-c', '--conda',
                               help="Also removes the conda environment from the system",
                               action="store_true")
    remove_parser.add_argument('-f', '--folder',
                               help="Also removes the local folder",
                               action="store_true")
    remove_parser.add_argument('-a', '--remove-all',
                               help="Remove everything (repo, folder, conda)",
                               action="store_true")

    # config subcommand TODO Do we need that option?

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()
