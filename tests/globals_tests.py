import unittest
from settings import Settings
from util.globals import GlobalsUtils
from six import string_types
import itertools


class GlobalsTests(unittest.TestCase):
    """
    Tests in this class relate to the contents or existence of the globals.txt configuration file.
    """

    def setUp(self):
        self.globals_utils = GlobalsUtils(Settings.config_repo_path)

    def test_GIVEN_a_globals_file_exists_THEN_it_passes_a_syntax_check(self):

        if not self.globals_utils.file_exists():
            self.skipTest("Globals file did not exist.")

        for linenumber, line in enumerate(self.globals_utils.get_lines(), 1):
            self.assertIsInstance(line, string_types)
            self.assertTrue(self.globals_utils.check_syntax(line),
                            "Invalid syntax on line {linenumber}. Line contents was: {contents}"
                            .format(linenumber=linenumber, contents=line))

    def test_WHEN_checking_the_configs_directory_THEN_there_are_no_extra_files_called_globals(self):
        self.assertEqual(self.globals_utils.get_number_of_globals_files(), 1 if self.globals_utils.file_exists() else 0,
                         "Extra globals files ({}) files in repository.".format(self.globals_utils.GLOBALS_FILE))

    def test_WHEN_macros_are_defined_in_globals_for_a_motor_ioc_THEN_both_or_neither_of_com_setting_and_motor_control_number_are_defined(self):

        motor_ioc_prefixes = ["GALIL", "MCLENNAN", "LINMOT", "SM300"]
        max_suffix = 10
        motor_iocs = ["{}_{:02d}".format(p, i) for p, i in
                      itertools.product(motor_ioc_prefixes, range(1, max_suffix + 1))]

        for motor_ioc in motor_iocs:
            defined_macros = self.globals_utils.get_macros(motor_ioc)

            controller_number_defined = "MTRCTRL" in defined_macros
            comms_macro_defined = any(m in defined_macros for m in ["PORT", "GALILADDR"])

            self.assertTrue(controller_number_defined == comms_macro_defined)  # Both or neither
