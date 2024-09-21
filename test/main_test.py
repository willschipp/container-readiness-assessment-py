import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from server.server import app, serve_static 

class TestStaticFileServing(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.server.os.path')
    @patch('server.server.send_from_directory')
    def test_serve_static(self, mock_send_from_directory, mock_os_path):
        # Mock os.path.dirname and os.path.join
        mock_os_path.dirname.return_value = '/mock/root'
        mock_os_path.join.return_value = '/mock/root/static'

        # Mock send_from_directory
        mock_send_from_directory.return_value = 'Mocked File Content'

        # Test the route
        response = self.app.get('/static/test.txt')

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Mocked File Content')

        # Assert that send_from_directory was called with correct arguments
        mock_send_from_directory.assert_called_once_with('/mock/root/static', 'test.txt')

    @patch('server.server.os.path')
    @patch('server.server.send_from_directory')
    def test_serve_static_subdirectory(self, mock_send_from_directory, mock_os_path):
        # Mock os.path.dirname and os.path.join
        mock_os_path.dirname.return_value = '/mock/root'
        mock_os_path.join.return_value = '/mock/root/static'

        # Mock send_from_directory
        mock_send_from_directory.return_value = 'Mocked Subdirectory File Content'

        # Test the route with a file in a subdirectory
        response = self.app.get('/static/css/styles.css')

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Mocked Subdirectory File Content')

        # Assert that send_from_directory was called with correct arguments
        mock_send_from_directory.assert_called_once_with('/mock/root/static', 'css/styles.css')

if __name__ == '__main__':
    unittest.main()