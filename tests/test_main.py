import unittest
from unittest.mock import patch, mock_open
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ig_non_followers_checker')))

from main import load_credentials

class TestLoadCredentials(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"username": "test_user", "password": "test_pass"}')
    def test_load_credentials_valid(self, mock_file):
        filename = 'config.json'
        expected_result = {'username': 'test_user', 'password': 'test_pass'}
        result = load_credentials(filename)
        self.assertEqual(result, expected_result)

    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    def test_load_credentials_empty(self, mock_file):
        filename = 'empty_config.json'
        expected_result = {}
        result = load_credentials(filename)
        self.assertEqual(result, expected_result)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_credentials_nonexistent(self, mock_file):
        filename = 'nonexistent_config.json'
        self.assertRaises(FileNotFoundError, load_credentials, filename)

if __name__ == '__main__':
    unittest.main()
