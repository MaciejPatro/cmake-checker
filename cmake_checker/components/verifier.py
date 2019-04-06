from pathlib import Path
from .lexer import Lexer


class Verifier(object):
    def __init__(self):
        self.lexer = Lexer()

    def check_path(self, files: list) -> list:
        files_with_issues = []
        for file in files:
            files_with_issues += [(file, self.__validate_file(file))]
        return files_with_issues

    def __validate_file(self, file: Path) -> list:
        with file.open() as cmake_file:
            return self.__find_issues(cmake_file.read())

    def __find_issues(self, data: str) -> list:
        return [(issue.type, issue.lineno) for issue in self.lexer.analyze(data)]
