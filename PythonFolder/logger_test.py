import unittest
from unittest.mock import patch
from PythonFolder.logger import Logger

class TestLogger(unittest.TestCase):
    @patch('logger.logging')
    def test_log_message(self, mock_logging):
        # Test logging for no error (code 201)
        Logger.log_message(201)
        mock_logging.info.assert_called_once_with("No error - operation successful.")

        # Reset mock
        mock_logging.reset_mock()

        # Test logging for bad parameter (code 400)
        Logger.log_message(400)
        mock_logging.error.assert_called_once_with("Bad parameter - a provided parameter is incorrect. ")

        # Reset mock
        mock_logging.reset_mock()

        # Test logging for No such image (code 404)
        Logger.log_message(404)
        mock_logging.error.assert_called_once_with("No such image - specified Docker image does not exist. ")

        # Reset mock
        mock_logging.reset_mock()

        # Test logging for Impossible to attach (code 406)
        Logger.log_message(406)
        mock_logging.error.assert_called_once_with("Impossible to attach - container not running. ")

        # Reset mock
        mock_logging.reset_mock()

        # Test logging for Conflict (code 409)
        Logger.log_message(409)
        mock_logging.error.assert_called_once_with("Conflict - conflicting state or request. ")

        # Reset mock
        mock_logging.reset_mock()

        # Test logging for Server error (code 500)
        Logger.log_message(500)
        mock_logging.error.assert_called_once_with("Server error - internal server error occurred. ")

        # Reset mock
        mock_logging.reset_mock()

        # Test logging for unknown error code
        Logger.log_message(999)
        mock_logging.warning.assert_called_once_with("Unknown error code: 999 - ")

        # Test with additional info
        mock_logging.reset_mock()
        Logger.log_message(404, extra_info="Attempt to pull missing image.")
        expected_message = "No such image - specified Docker image does not exist. Attempt to pull missing image."
        mock_logging.error.assert_called_once_with(expected_message)

    @patch('logger.logging')
    def test_info(self, mock_logging):
        # Test info logging
        Logger.info("Test informational message")
        mock_logging.info.assert_called_once_with("Test informational message")

    @patch('logger.logging')
    def test_error(self, mock_logging):
        # Test error logging
        Logger.error("Test error message")
        mock_logging.error.assert_called_once_with("Test error message")

if __name__ == '__main__':
    unittest.main()
