import argparse
import sys


def get_params():
    parser = argparse.ArgumentParser(description="Project creation (pocr) command line tool")
    parser.add_argument("--install", help="Start the installation wizard.", action="store_true")
    parser.add_argument("--test", help="Puts pocr into testing mode", action="store_true")
    parser.add_argument("--clear", help="Clears all user files", action="store_true")
    # TODO option to create the repo private

    subparsers = parser.add_subparsers(help="The different functions of pocr", dest='command')

    # create subcommand
    create_parser = subparsers.add_parser("create", help="Create a new pocr project")
    create_parser.add_argument('-n', '--project-name',
                               help="Name of the project",
                               required=True,
                               type=str)
    create_parser.add_argument('-p', '--python-version',
                               help="Python version for the project. Default: 3.5",
                               required=False,
                               type=float,
                               default=3.5)
    create_parser.add_argument('-r', '--repo-name',
                               help="If you already have a github repo for the project. Enter the repo name.",
                               required=False,
                               type=str)
    create_parser.add_argument('-c', '--conda-name',
                               help="If you already have a conda environment for the project. Enter the name.",
                               required=False,
                               type=str)
    create_parser.add_argument('-gh', '--git-hook',
                               help="Does not install a pre-push git hook.",
                               action="store_false")
    # list subcommand
    list_parser = subparsers.add_parser("list", help="Lists all existing pocr projects")

    # # update subcommand
    # update_parser = subparsers.add_parser('update', help="Updates a existing pocr project")

    # remove subcommand
    remove_parser = subparsers.add_parser('remove', help="Remove a pocr project")
    remove_parser.add_argument('-n', '--name',
                               help="Name of the pocr project to remove",
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
