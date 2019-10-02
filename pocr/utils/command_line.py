import argparse


def get_params():
    parse = argparse.ArgumentParser(description="Project creation (pocr) command line tool")
    parse.add_argument("--install", help="Start the installation wizard.", action="store_true")

    return parse.parse_args()
