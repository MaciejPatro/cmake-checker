from unittest import TestCase
from pathlib import Path
import subprocess


class IntegrationTests(TestCase):
    PROGRAM = 'cmake_checker'
    INTEGRATION_TESTS_PATH = 'cmake_checker/tests/integration_tests/'

    def __init__(self, *args, **kwargs):
        super(IntegrationTests, self).__init__(*args, **kwargs)

    def __run_cmake_checker_for_file(self, *args) -> str:
        execute_command = ['python3', '-m', self.PROGRAM, '--warn-only', *args]
        output = subprocess.check_output(execute_command)

        return output.decode('utf-8')

    def path(self, path: str) -> str:
        return self.INTEGRATION_TESTS_PATH + path

    def assertNumberOfScannedFiles(self, number: int, data: str) -> None:
        self.assertTrue(("Scanned %d file(s)." % number) in data)

    def assertCheckerFoundNoIssues(self, data: str) -> None:
        self.assertCheckerFoundNumberOfIssues(0, data)

    def assertCheckerFoundNumberOfIssues(self, number: int, data: str) -> None:
        self.assertTrue(("Found %d issues." % number) in data)

    def setUp(self):
        super(IntegrationTests, self).setUp()

    def test_should_return_success_and_pass_when_checking_empty_file(self):
        try:
            output = self.__run_cmake_checker_for_file(self.path('empty_file/CMakeLists.txt'))

            self.assertNumberOfScannedFiles(1, output)
            self.assertCheckerFoundNoIssues(output)

        except subprocess.CalledProcessError:
            self.fail("Non zero result received for empty file!")

    def test_should_return_success_and_pass_when_checking_empty_directory(self):
        try:
            output = self.__run_cmake_checker_for_file(self.path('empty_dir'))

            self.assertNumberOfScannedFiles(0, output)
            self.assertCheckerFoundNoIssues(output)

        except subprocess.CalledProcessError:
            self.fail("Non zero result received for empty dir!")

    def test_should_return_non_zero_when_checking_non_existing_directory(self):
        self.assertRaises(subprocess.CalledProcessError, self.__run_cmake_checker_for_file, 'invalid_dir')

    def test_should_return_success_and_find_3_issues(self):
        output = self.__run_cmake_checker_for_file(self.path('dir_with_file_glob_issue/CMakeLists.txt'))

        self.assertNumberOfScannedFiles(1, output)
        self.assertCheckerFoundNumberOfIssues(3, output)

    def test_should_return_success_and_find_multiple_violations_in_line_1(self):
        number_of_violations = 3
        violation_string = "add_compile_options() CMAKE_CXX_FLAGS include_directories()"

        output = self.__run_cmake_checker_for_file(self.path('multiple_violations_in_single_line/CMakeLists.txt'))

        self.assertEqual(number_of_violations, output.count(violation_string))
        self.assertCheckerFoundNumberOfIssues(number_of_violations, output)

    def test_should_return_success_and_ignore_all_non_cmake_files_in_dir(self):
        output = self.__run_cmake_checker_for_file(self.path('non-cmake-files-dir/'))

        self.assertNumberOfScannedFiles(0, output)
        self.assertCheckerFoundNoIssues(output)

    def test_should_correctly_find_issues_in_multiple_files_inside_of_dir_recursively(self):
        output = self.__run_cmake_checker_for_file(self.path('cmake-files-dir/'))

        self.assertNumberOfScannedFiles(2, output)
        self.assertCheckerFoundNumberOfIssues(3, output)

    def test_should_accept_multiple_paths_or_files_as_arguments(self):
        output = self.__run_cmake_checker_for_file(
            self.path('cmake-files-dir/'),
            self.path('multiple_violations_in_single_line/')
        )

        self.assertNumberOfScannedFiles(3, output)
        self.assertCheckerFoundNumberOfIssues(6, output)

    def test_should_raise_exception_when_warn_only_is_disabled_and_violations_are_found(self):
        execute_command = ['python3', '-m', self.PROGRAM, self.INTEGRATION_TESTS_PATH]

        self.assertRaises(subprocess.CalledProcessError, subprocess.check_output, execute_command)

    def test_stdout_should_be_exactly_the_same_as_saved_file_output(self):
        filename = 'test.txt'
        command_line_output = self.__run_cmake_checker_for_file(self.INTEGRATION_TESTS_PATH)
        execute_command = ['python3', '-m', self.PROGRAM, '--warn-only', '-o', filename, self.INTEGRATION_TESTS_PATH]

        subprocess.check_output(execute_command)
        output_file = Path(filename)

        self.assertEqual(command_line_output, output_file.read_text())
        output_file.unlink()

    def test_junit_report_compare_with_golden_master_for_empty_directory(self):
        output = self.__run_cmake_checker_for_file(self.path('empty_dir'), '--reporter', 'junit')
        golden_master = Path(self.path('junit_goldenmaster/empty_dir.xml'))

        self.assertEqual(golden_master.read_text(), output)

    def test_junit_report_compare_with_golden_master_for_non_empty_dir(self):
        output = self.__run_cmake_checker_for_file(self.INTEGRATION_TESTS_PATH, '--reporter', 'junit')
        golden_master = Path(self.path('junit_goldenmaster/integration_dir.xml'))

        self.assertEqual(golden_master.read_text(), output)

    def test_should_whitelist_correctly_certain_files_when_whitelist_file_provided(self):
        output = self.__run_cmake_checker_for_file(
            self.path('cmake-files-dir/'),
            self.path('multiple_violations_in_single_line/'),
            '--whitelist',
            self.path('whitelist.txt')
        )

        self.assertNumberOfScannedFiles(2, output)
        self.assertCheckerFoundNumberOfIssues(3, output)
