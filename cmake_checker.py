import argparse
import sys
from pathlib import Path
from cmake_checker.verifier import Verifier
from cmake_checker.consolereporter import ConsoleReporter


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
                                  help='Path to the file or directory where the checks should be done')

    return arguments_parser.parse_args()


def main():
    arguments = parse_arguments()

    verify = Verifier()
    files_with_info = verify.check_path(arguments.PATH)
    reporter = ConsoleReporter(files_with_info)
    report = reporter.generate_report()
    print(report)
    sys.exit(0)


main()
