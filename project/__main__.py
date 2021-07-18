from machine import add_machine_subparser
from supervisor import add_supervisor_subparser
import argparse
import logging


def main():
    """
    Start one of the subprojects

    Parses command line arguments and delegates them to the relevant subparser
    """

    parser = argparse.ArgumentParser(description="Start part of the Supervisor project")
    subparsers = parser.add_subparsers(
        title="Programs", required=True, help="Which program to invoke", dest="program"
    )

    parser.add_argument(
        "-log",
        "--log",
        default="warning",
        help=(
            "Provide logging level. "
            "Example --log debug', default='warning'"
        )
    )


    add_machine_subparser(subparsers)
    add_supervisor_subparser(subparsers)
    args = parser.parse_args()
    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }
    level = levels.get(args.log.lower())

    if level is None:
        raise ValueError(
            f"log level given: {args.log}"
            f" -- must be one of: {' | '.join(levels.keys())}"
        )

    logging.basicConfig(level=level)
    args.func(args)


if __name__ == "__main__":
    main()
