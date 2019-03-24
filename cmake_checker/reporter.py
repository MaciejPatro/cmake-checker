from pathlib import Path
from junit_xml import TestSuite, TestCase


class Reporter(object):
    @staticmethod
    def create(reporter_type: str, files_with_info: list):
        if reporter_type == 'console':
            return ConsoleReporter(files_with_info)
        elif reporter_type == 'junit':
            return JUnitReporter(files_with_info)
        return None


class ConsoleReporter(Reporter):
    def __init__(self, files_with_info: list):
        self.files_number = len(files_with_info)
        self.files_with_info = files_with_info

        self.current_violation_line = ""
        self.current_parsing_line = 0
        self.violations = 0

    def generate_report(self) -> str:
        output = ""
        for file, violations in self.files_with_info:
            output = output + self.__generate_file_violations(file, violations)

        output = output + '\n' + self.__create_summary()
        return output

    def __create_summary(self) -> str:
        if self.violations == 0:
            return "Scanned %d file(s). Found no issues.\n" % self.files_number
        else:
            return "Scanned %d file(s). Found %d issues.\n" % (self.files_number, self.violations)

    def __generate_file_violations(self, file: Path, violations: list) -> str:
        output = ""
        with file.open() as cmake_file:
            self.current_violation_line = ""
            self.current_parsing_line = 0

            if violations:
                output = output + "\n>>>" + str(file) + '<<<\n'

            for (violation_type, line_number) in violations:
                self.violations = self.violations + 1
                self.__read_line_with_given_number(cmake_file, line_number)
                output = output + self.__generate_new_violation(line_number, violation_type)
        return output

    def __read_line_with_given_number(self, file, line):
        while self.current_parsing_line != line:
            self.current_parsing_line = self.current_parsing_line + 1
            self.current_violation_line = file.readline()

    def __generate_new_violation(self, line_number: int, violation_type: str):
        return "line: %4s %20s> %s" % (line_number, violation_type, self.current_violation_line)


class JUnitReporter(Reporter):
    def __init__(self, files_with_info: list):
        self.files_with_info = files_with_info
        self.current_parsing_line = 0
        self.current_violation_line = ''

    def generate_report(self) -> str:
        test_suites = []

        for file_with_info in self.files_with_info:
            test_suites.append(self.__create_test_suite_for(file_with_info))

        if not test_suites:
            test_suites = self.__generate_empty_test_suites()

        return TestSuite.to_xml_string(test_suites, prettyprint=True)

    def __create_test_suite_for(self, file__with_info) -> TestSuite:
        test_case_list = self.__create_test_cases(file__with_info[0], file__with_info[1])
        return TestSuite(file__with_info[0], test_case_list)

    def __create_test_cases(self, file: Path, violations: list) -> list:
        test_cases = []

        with file.open() as cmake_file:
            self.current_parsing_line = 0

            for (violation_type, line_number) in violations:
                self.__read_line_with_given_number(cmake_file, line_number)
                test_case = TestCase(name=violation_type, line=line_number)
                violation = "line: %4s %20s> %s" % (line_number, violation_type, self.current_violation_line)
                test_case.add_failure_info(message=violation)
                test_cases.append(test_case)

        return test_cases

    def __read_line_with_given_number(self, file, line):
        while self.current_parsing_line != line:
            self.current_parsing_line = self.current_parsing_line + 1
            self.current_violation_line = file.readline()

    @staticmethod
    def __generate_empty_test_suites() -> list:
        return [TestSuite('cmake-checker', [TestCase(name='No cmake files found')])]
