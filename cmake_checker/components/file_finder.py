from pathlib import Path


def provide_files_for_verification(paths: list, whitelist_content) -> list:
    file_finder = FileFinder(whitelist_content)

    file_list = []
    for path in paths:
        file_list += file_finder.get_all_cmake_files(path)
    return file_list


class FileFinder(object):
    def __init__(self, whitelist=None):
        if whitelist is None:
            self.ignore_patterns = []
        else:
            self.ignore_patterns = [line.rstrip('\n') for line in whitelist]

    def get_all_cmake_files(self, path: Path) -> list:
        if not path.is_dir():
            return [path]
        return self.__get_all_files_from_dir(path)

    def __get_all_files_from_dir(self, path: Path) -> list:
        all_cmake_files = sorted(path.glob('**/*.cmake')) + sorted(path.glob('**/CMakeLists.txt'))
        return [file for file in all_cmake_files if not self.__is_on_whitelist(file)]

    def __is_on_whitelist(self, file: Path) -> bool:
        return any(file.match(path_pattern) for path_pattern in self.ignore_patterns)
