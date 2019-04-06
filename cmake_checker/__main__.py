import sys

from cmake_checker.components.file_finder import provide_files_for_verification
from cmake_checker.components.parse_arguments import parse_arguments
from cmake_checker.components.verifier import Verifier
from cmake_checker.components.reporter import Reporter


def compute_exit_code(violations: list, warn_only: bool) -> int:
    if warn_only is True:
        return 0
    if any(len(v) for f, v in violations):
        return -1
    return 0


def main():
    arguments = parse_arguments()
    verify = Verifier()

    files = provide_files_for_verification(arguments.PATH, arguments.whitelist)
    files_with_info = verify.check_path(files)
    reporter = Reporter.create(arguments.reporter, files_with_info)
    arguments.output_file.write(reporter.generate_report())

    sys.exit(compute_exit_code(files_with_info, arguments.warn_only))


main()
