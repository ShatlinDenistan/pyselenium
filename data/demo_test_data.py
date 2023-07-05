""" Provides test data to the tests"""
from utils.json_utils import read_json_file


def get_demo_test_data_positive():
    """Test data for positive scenarios"""
    return read_json_file("./data/demo_test_data.json")


def get_demo_test_data_negative():
    """Test data for negative scenarios"""
    return read_json_file("./data/demo_test_data_negative.json")
