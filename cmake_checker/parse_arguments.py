import argparse
import sys
from pathlib import Path


def file_or_dir(path: str) -> Path:
    new_path = Path(path)
    if not new_path.exists():
        msg = "%s doesn't exist!" % path
        raise argparse.ArgumentTypeError(msg)
    return new_path


def parse_arguments() -> argparse.Namespace:
    arguments_parser = argparse.ArgumentParser()

    arguments_parser.add_argument('PATH',
                                  type=file_or_dir,
                                  nargs='+',
                                  help='Path to the file or directory where the checks should be done'
                                  )
    arguments_parser.add_argument('--warn-only',
                                  action='store_true',
                                  help='Program will return 0 even if violations are found'
                                  )
    arguments_parser.add_argument('--reporter',
                                  choices=['console', 'junit'],
                                  default='console',
                                  help='Specify type of reporter to output'
                                  )
    arguments_parser.add_argument('-o',
                                  '--output-file',
                                  type=argparse.FileType('w'),
                                  default=sys.stdout,
                                  help='Output results to file with given name'
                                  )
    arguments_parser.add_argument('--whitelist',
                                  type=argparse.FileType('r'),
                                  help='Whitelist file with rules to ignore certain files or dirs (.gitignore style)'
                                  )
    return arguments_parser.parse_args()
