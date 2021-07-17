from machine import add_machine_subparser
from supervisor import add_supervisor_subparser
import argparse


def main():
    parser = argparse.ArgumentParser(description='Start part of the Supervisor project')
    subparsers = parser.add_subparsers(title='Programs', required=True, help="Which program to invoke", dest="program")
    add_machine_subparser(subparsers)
    add_supervisor_subparser(subparsers)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
