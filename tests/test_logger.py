import unittest
from random import randint

from cast.logger import Logging

import os


class CastShLoggingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        session_id = str(randint(1, 100000))
        logger = Logging(session_id)
        cls.session_id = session_id
        cls.logger = logger
        cls.logger.make_log_folder()

    def test_logger_properties(self):
        self.assertEqual(self.logger.folder, r"cast/log_data")
        self.assertEqual(
            self.logger.file_location, r"cast/log_data/log_" + self.session_id + r".log"
        )

    def test_log_folder_creation(self):
        self.assertTrue(os.path.exists(self.logger.folder))
        creation_status = self.logger.make_log_folder()
        self.assertEqual(creation_status, "Folder already exists")

    def test_log_file_creation(self):
        self.logger.write_log("test")
        self.assertTrue(os.path.exists(self.logger.file_location))

    def test_log_erase(self):
        self.logger.write_log("test")

        with open(self.logger.file_location, "r") as file:
            data = file.read().replace("\n", "")

        self.logger.write_log(b"\x7f".decode())

        with open(self.logger.file_location, "r") as file:
            erased_data = file.read().replace("\n", "")

        self.assertNotEqual(data, erased_data)
        self.assertEqual(erased_data, data[:-1])

    def test_log_time(self):
        self.logger.write_log("test")

        with open(self.logger.file_location, "r") as file:
            data = file.read().replace("\n", "")

        self.logger.write_log(b"\r".decode())

        with open(self.logger.file_location, "r") as file:
            erased_data = file.read().replace("\n", "")

        self.assertNotEqual(data, erased_data)
