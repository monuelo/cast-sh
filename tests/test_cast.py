import sys
import unittest

from flask import Flask

from cast.app import app, create_parser


class CastShTests(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get("/")
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


class CastShCLIOptionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = create_parser()
        cls.parser = parser

    def test_help(self):
        """
        User passes no args, should fail with SystemExit
        """
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--help"])

    def test_version(self):
        """
        User passes no args, should fail with SystemExit
        """
        args = self.parser.parse_args(["--version"])
        self.assertTrue(args.version)

    def test_bad_version(self):
        """
        User passes no args, should fail with SystemExit
        """
        with self.assertRaises(SystemExit):
            args = self.parser.parse_args(["--help"])
            self.assertFalse(args.version)
