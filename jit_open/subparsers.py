import argparse

from . import doc_split


def add_default_parser(self, func, *args, **kwargs):
    """
    """
    subparser = self.add_parser(func.func_name, *args, **kwargs)

    subparser.set_defaults(func=func)
    if not subparser.description:
        subparser.description = doc_split(func)

    return subparser


argparse._SubParsersAction.add_default_parser = add_default_parser
