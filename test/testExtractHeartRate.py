import unittest
from unittest.mock import MagicMock
from extractHeartRate import ExtractHeartRate
import numpy as np


class TestExtractHeartRate(unittest.TestCase):
    def setUp(self):
        self.green_channel_mock = MagicMock()
        self.extract_heart_rate = ExtractHeartRate(self.green_channel_mock)

    def test_calc_hr_process_no_face_detected(self):
        # Test when green_channel is None
        self.extract_heart_rate.green_channel = None
        padded_list = np.zeros(600)
        result = self.extract_heart_rate.calc_hr_process(padded_list, 30, 600, MagicMock(), 300)
        self.assertEqual(result, (0, 0, "Face did not detected"))

    def test_calc_hr_process_valid_case(self):
        # Test a valid case with non-empty sample data
        padded_list = np.random.rand(600)
        counter = 600
        result = self.extract_heart_rate.calc_hr_process(padded_list, 30, 600, MagicMock(), counter)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)
        self.assertIsNone(result[2])

    def test_max_filter(self):
        # Test the max_filter method
        start_max_index = 10
        start_max_value = 5.0
        fourier_abs_values = np.random.rand(600)
        list_size_without_padding = 600
        result = self.extract_heart_rate.max_filter(start_max_index, start_max_value, fourier_abs_values,
                                                    list_size_without_padding)
        self.assertIsInstance(result, int)

    def test_calculate_start_range(self):
        # Test the calculate_start_range method
        result = self.extract_heart_rate.calculate_start_range(30, 600)
        self.assertIsInstance(result, int)

    def test_calculate_end_range(self):
        # Test the calculate_end_range method
        result = self.extract_heart_rate.calculate_end_range(30, 600)
        self.assertIsInstance(result, int)

    def test_create_binary_vector(self):
        # Test the create_binary_vector method
        padded_list = np.random.rand(600)
        list_size_without_padding = 600
        result = self.extract_heart_rate.create_binary_vector(padded_list, list_size_without_padding)
        self.assertEqual(len(result), list_size_without_padding)

    def test_find_shift_widths(self):
        # Test the find_shift_widths method
        binary_vector = [0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0]
        result = self.extract_heart_rate.find_shift_widths(binary_vector)
        self.assertIsInstance(result, list)

    def test_trim_list(self):
        # Test the trim_list method
        input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        percentage_to_remove = 0.2
        result = self.extract_heart_rate.trim_list(input_list, percentage_to_remove)
        self.assertIsInstance(result, list)

    def test_clean_sd(self):
        # Test the clean_sd method
        x = np.random.rand(50)
        result = self.extract_heart_rate.clean_sd(x)
        self.assertIsInstance(result, np.ndarray)

    def test_remove_noise_and_pad(self):
        # Test the remove_noise_and_pad method
        padded_list = np.random.rand(600)
        std_list = np.random.rand(20)
        group_size = 30
        result = self.extract_heart_rate.remove_noise_and_pad(padded_list, std_list, group_size)
        self.assertIsInstance(result, list)

    def test_move_zeros_to_end(self):
        # Test the move_zeros_to_end method
        new_padded_list = [1, 0, 3, 0, 5, 0, 7, 8, 9, 10]
        result = self.extract_heart_rate.move_zeros_to_end(new_padded_list)
        self.assertIsInstance(result, list)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
