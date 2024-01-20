import unittest
from unittest.mock import patch
from io import StringIO
from phase_4 import retrieve_data  


class TestRetrieveData(unittest.TestCase):

    def setUp(self):
        # Redirect stdout for testing user input
        self.patch_stdout = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.patch_stdout.start()

    def tearDown(self):
        self.patch_stdout.stop()

    @patch('requests.get')
    def test_retrieve_data_successful(self, mock_get):
        input_values = ['35.6895', '139.6917', 'Japan', 'Tokyo', 'Asia/Tokyo', '2022-01-01', '2022-01-01']
        with patch('builtins.input', side_effect=input_values):
            # Mock a successful API response
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                'daily': {
                    'time': ['2022-01-01'],
                    'temperature_2m_max': [20.0],
                    'temperature_2m_min': [10.0],
                    'temperature_2m_mean': [15.0],
                    'precipitation_hours': [3.0]
                }
            }

            retrieve_data()

      
    @patch('requests.get')
    def test_retrieve_data_invalid_input(self, mock_get):
        input_values = ['invalid', '139.6917', 'Japan', 'Tokyo', 'Asia/Tokyo', '2022-01-01', '2022-01-01']
        with patch('builtins.input', side_effect=input_values):
            # Mock an unsuccessful API response
            mock_get.return_value.status_code = 400
            retrieve_data()

        # Check if the error message is displayed
        self.assertIn('An error occurred:', self.mock_stdout.getvalue())


    # Add more test cases for edge cases, additional validations, etc.


if __name__ == '__main__':
    unittest.main()
