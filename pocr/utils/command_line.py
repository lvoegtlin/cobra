import argparse


def get_params():
    parser = argparse.ArgumentParser(description="Project creation (pocr) command line tool")
    parser.add_argument("--install", help="Start the installation wizard.", action="store_true")
    parser.add_argument("--test", help="Puts pocr into testing mode", action="store_true")

    subparsers = parser.add_subparsers(help="The different functions of pocr", dest='command')

    # create subcommand
    create_parser = subparsers.add_parser("create", help="Create a new pocr project")
    create_parser.add_argument('-n', '--name',
                               help="Name of the project",
                               required=True,
                               type=str)
    create_parser.add_argument('-ps', '--python-version',
                               help="Python version for the project. Default: System version",
                               required=False,
                               type=float,
                               default=None)

    # update subcommand

    # remove subcommand

    # settings subcommand

    return parser.parse_args()
