import sys

from cmake_checker.parse_arguments import parse_arguments
from cmake_checker.verifier import Verifier
from cmake_checker.reporter import Reporter


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
