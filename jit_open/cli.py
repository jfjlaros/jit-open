import argparse

from . import doc_split, usage, version
from .jit_open import *


def jit_open():
    """
    """
    pass


def main():
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage[0], epilog=usage[1])
    parser.add_argument('-v', action='version', version=version(parser.prog))

    try:
        args = parser.parse_args()
    except IOError, error:
        parser.error(error)

    try:
        jit_open(
            **{k: v for k, v in vars(args).items()
            if k not in ('func', 'subcommand')})
    except (ValueError, IOError), error:
        parser.error(error)


if __name__ == '__main__':
    main()
