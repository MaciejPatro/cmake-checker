from pathlib import Path
from cmake_checker.lexer import Lexer


class Verifier(object):
    def __init__(self):
        self.lexer = Lexer()

    def check_path(self, paths: list) -> list:
        files_with_issues = list()

        for path in paths:
            files_with_issues = files_with_issues + self.__check_path(path)

        return files_with_issues

    def __check_path(self, path: Path) -> list:
        if not path.is_dir():
            return [(path, self.__validate_file(path))]

        files_with_issues = list()
        files = self.__find_all_cmake_files(path)
        for file in files:
            files_with_issues.append((file, self.__validate_file(file)))
        return files_with_issues

    def __validate_file(self, file: Path) -> list:
        with file.open() as cmake_file:
            return self.__find_issues(cmake_file.read())

    def __find_issues(self, data: str) -> list:
        issues = []
        found_issues = self.lexer.analyze(data)

        for issue in found_issues:
            issues.append((issue.type, issue.lineno))

        return issues

    @staticmethod
    def __find_all_cmake_files(path: Path):
        files_list = sorted(path.glob('**/*.cmake'))
        files_list = files_list + sorted(path.glob('**/CMakeLists.txt'))
        return files_list
