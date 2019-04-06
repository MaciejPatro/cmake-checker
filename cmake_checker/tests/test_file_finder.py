from unittest import TestCase
from pathlib import Path

from cmake_checker.components.file_finder import FileFinder


class TestFileFinder(TestCase):
    PATH = Path('cmake_checker/tests/integration_tests')

    def test_should_list_all_files_when_no_whitelist_provided(self):
        file_finder = FileFinder()
        all_found_files = file_finder.get_all_cmake_files(self.PATH)
        self.assertEqual(5, len(all_found_files))

    def test_should_whitelist_multiple_cases(self):
        whitelist = ['*.cmake', '**/empty_file/**']
        file_finder = FileFinder(whitelist)

        all_found_files = file_finder.get_all_cmake_files(self.PATH)

        self.assertEqual(3, len(all_found_files))
        self.assertTrue(all(not str(x).endswith('.cmake') for x in all_found_files))
        self.assertTrue(all('empty_file' not in str(x) for x in all_found_files))
