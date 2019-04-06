from pathlib import Path
from junit_xml import TestSuite, TestCase


class LineReader(object):
    def __init__(self, file):
        self.current_line = ''
        self.current_line_number = 0
        self.file = file

    def get(self, line):
        while self.current_line_number != line:
            self.current_line_number = self.current_line_number + 1
            self.current_line = self.file.readline()

        return self.current_line


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
        self.files_with_info = files_with_info
        self.violations = 0

    def generate_report(self) -> str:
        output = ''
        for file, violations in self.files_with_info:
            output += self.__generate_file_output(file, violations)

        return output + '\n' + self.__create_summary()

    def __create_summary(self) -> str:
        files_number = len(self.files_with_info)
        return "Scanned %d file(s). Found %d issues.\n" % (files_number, self.violations)

    def __generate_file_output(self, file: Path, violations: list) -> str:
        output = ''
        if violations:
            with file.open() as cmake_file:
                line_reader = LineReader(cmake_file)
                output += "\n>>>" + str(file) + '<<<\n'
                output += self.__generate_file_violations(line_reader, violations)
        return output

    def __generate_file_violations(self, line_reader: LineReader, violations: list):
        output = ''
        for (violation_type, line_number) in violations:
            self.violations = self.violations + 1
            output += self.__generate_new_violation_prefix(line_number, violation_type)
            output += line_reader.get(line_number)
        return output

    @staticmethod
    def __generate_new_violation_prefix(line_number: int, violation_type: str):
        return "line: %4s %20s> " % (line_number, violation_type)


class JUnitReporter(Reporter):
    def __init__(self, files_with_info: list):
        self.files_with_info = files_with_info

    def generate_report(self) -> str:
        test_suites = self.__generate_test_suites()
        if not test_suites:
            test_suites = self.__generate_empty_test_suites()
        return TestSuite.to_xml_string(test_suites, prettyprint=True)

    def __generate_test_suites(self) -> list:
        test_suites = []
        for file_with_info in self.files_with_info:
            test_suites.append(self.__create_test_suite_for(file_with_info))
        return test_suites

    def __create_test_suite_for(self, file__with_info) -> TestSuite:
        test_case_list = self.__create_test_cases(file__with_info[0], file__with_info[1])
        return TestSuite(file__with_info[0], test_case_list)

    def __create_test_cases(self, file: Path, violations: list) -> list:
        test_cases = []
        with file.open() as cmake_file:
            line_reader = LineReader(cmake_file)

            for (violation, line_number) in violations:
                test_case = TestCase(name=violation, line=line_number)
                test_case.add_failure_info(message=self.__generate_failure_info(line_number, violation, line_reader))
                test_cases.append(test_case)
        return test_cases

    @staticmethod
    def __generate_failure_info(line_number: int, violation_type: str, line_reader: LineReader) -> str:
        return "line: %4s %20s> %s" % (line_number, violation_type, line_reader.get(line_number))

    @staticmethod
    def __generate_empty_test_suites() -> list:
        return [TestSuite('cmake-checker', [TestCase(name='No cmake files found')])]
