import argparse
import sys
from pathlib import Path

from cmake_checker.verifier import Verifier
from cmake_checker.reporter import Reporter


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
    arguments_parser.add_argument('-o',
                                  '--output-file',
                                  type=argparse.FileType('w'),
                                  default=sys.stdout,
                                  help='Output results to file with given name'
                                  )
    arguments_parser.add_argument('--reporter',
                                  choices=['console', 'junit'],
                                  default='console',
                                  help='Specify type of reporter to output'
                                  )
    return arguments_parser.parse_args()


def compute_exit_code(violations: list, warn_only: bool) -> int:
    if warn_only is True:
        return 0
    if any(len(v) for f, v in violations):
        return -1
    return 0


def main():
    arguments = parse_arguments()

    verify = Verifier()
    files_with_info = verify.check_path(arguments.PATH)
    reporter = Reporter.create(arguments.reporter, files_with_info)
    report = reporter.generate_report()
    arguments.output_file.write(report)

    sys.exit(compute_exit_code(files_with_info, arguments.warn_only))


main()
