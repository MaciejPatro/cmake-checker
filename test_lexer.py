from unittest import TestCase
from lexer import Lexer


class TestLexer(TestCase):
    def __init__(self, *args, **kwargs):
        self.lexer = None
        super(TestLexer, self).__init__(*args, **kwargs)

    def setUp(self):
        self.lexer = Lexer()
        super(TestLexer, self).setUp()

    def test_empty_string_should_not_find_any_token(self):
        self.assertFalse(self.lexer.analyze(""))

    def test_correct_string_should_provide_empty_list(self):
        self.assertFalse(self.lexer.analyze("some_function()"))

    def test_should_find_file_glob_and_correctly_save_state_with_line_no(self):
        tokens_found = self.lexer.analyze("\n\n\nfile \t(  \tGLOB")

        self.assertEqual(1, len(tokens_found))

        file_glob_token = tokens_found[0]
        self.assertEqual('FILE_GLOB', file_glob_token.type)
        self.assertEqual(4, file_glob_token.lineno)

    def test_should_ignore_variable_with_glob(self):
        tokens_found = self.lexer.analyze("\n\n\nfile(  \t${GLOB")
        self.assertFalse(tokens_found)

    def test_should_find_add_compile_options_and_correctly_save_state_with_line_no(self):
        tokens_found = self.lexer.analyze("\nadd_compile_options\t(  \tGLOB")

        self.assertEqual(1, len(tokens_found))

        token = tokens_found[0]
        self.assertEqual('ADD_COMPILE_OPTIONS', token.type)
        self.assertEqual(2, token.lineno)

    def test_should_find_include_directories_but_ignore_target_version(self):
        tokens_found = self.lexer.analyze("\n   include_directories\t(  \tGLOB\n\ntarget_include_directories(dir)")

        self.assertEqual(1, len(tokens_found))

        token = tokens_found[0]
        self.assertEqual('INCLUDE_DIRECTORIES', token.type)
        self.assertEqual(2, token.lineno)

    def test_should_ignore_violations_in_line_comments_and_catch_in_next_lines(self):
        tokens_found = self.lexer.analyze("  # add_compile_options(\n   include_directories\t(")

        self.assertEqual(1, len(tokens_found))

        token = tokens_found[0]
        self.assertEqual('INCLUDE_DIRECTORIES', token.type)
        self.assertEqual(2, token.lineno)

    def test_cmake_check_disable_should_force_ignoring_content_until_enabled(self):
        tokens_found = self.lexer.analyze("add_compile_options( # cmake-check disable\n   include_directories\t( \n "
                                          "# cmake-check enable \n include_directories(")

        self.assertEqual(2, len(tokens_found))

        token = tokens_found[0]
        self.assertEqual('ADD_COMPILE_OPTIONS', token.type)
        self.assertEqual(1, token.lineno)

        token = tokens_found[1]
        self.assertEqual('INCLUDE_DIRECTORIES', token.type)
        self.assertEqual(4, token.lineno)

    def test_endif_should_not_contain_clauses_in_parenthesis(self):
        tokens_found = self.lexer.analyze("endif(sometext)\n\nelse()")

        self.assertEqual(1, len(tokens_found))

        token = tokens_found[0]
        self.assertEqual('CLOSING_COMMAND_WITH_CLAUSE', token.type)
        self.assertEqual(1, token.lineno)

    def test_should_raise_issue_when_set_or_unset_environment_variable_and_ignore_if_statements(self):
        tokens_found = self.lexer.analyze("\n\nset   \t(\tENV{ )  unset(ENV{ )\nif(ENV{")

        self.assertEqual(2, len(tokens_found))

        for token in tokens_found:
            self.assertEqual('MODIFY_ENV_VARIABLE', token.type)
            self.assertEqual(3, token.lineno)

    def test_should_raise_issue_when_unset_cache_is_done(self):
        tokens_found = self.lexer.analyze("unset(${SOME VARIABLE} # oh why () \n    CACHE")

        self.assertEqual(1, len(tokens_found))
        self.assertEqual('CACHE_IN_SET', tokens_found[0].type)

    def test_should_raise_violaton_for_target_sources_when_using_parent_dir(self):
        tokens_found = self.lexer.analyze("  \ttarget_sources( \n# ignored ../.. \n ../../dwoadnoew)\n ../..")

        self.assertEqual(1, len(tokens_found))
        self.assertEqual('PARENT_DIR_ACCESS', tokens_found[0].type)
        self.assertEqual(3, tokens_found[0].lineno)
