import unittest
from unittest.mock import Mock
import pandas as pd

from source.make_station_map import get_and_format_trip_data

class ScriptTests(unittest.TestCase):
    def test__get_and_format_trip_data__always__returns_correct(self):
        dummy_bike_trip_data_frame = pd.DataFrame(
            [[1,  ' 2018-06-30 23:59:55', '2018-07-01 00:38:10', 1, 2295, 3, ' Spaulding Ave & Armitage Ave', 340, ' Clark St & Wrightwood Ave', 'Subscriber', 'Male', 1989],
             [2, ' 2018-06-30 23:59:56', '2018-07-01 00:17:14', 2, 1038, 4, ' Spaulding Ave & Armitage Ave', 338, 'Calumet Ave & 18th St', 'Subscriber', 'Female', 1985],
             [3,    ' 2018-06-30 18:59:48', '2018-07-01 00:08:45', 3, 537, 5, ' Clark St & Wrightwood Ave', 506, ' Spaulding Ave & Armitage Ave', 'Subscriber', 'Male', 1980]],
            columns=['trip_id', 'start_time', 'end_time', 'bikeid', 'tripduration',
       'from_station_id', 'from_station_name', 'to_station_id',
       'to_station_name', 'usertype', 'gender', 'birthyear']
        ).astype(dtype={
            "trip_id": "int64",
            "start_time": "datetime64",
            "end_time": "datetime64",
            "bikeid": 'int64',
            "tripduration": 'int64',
            'from_station_id': 'int64',
            'from_station_name': 'object',
            'to_station_id': 'int64',
            'to_station_name': 'object',
            'usertype': 'object',
            'gender': 'object',
            'birthyear': 'object'
        })
        expected_data_frame = pd.DataFrame(
            [[1,  ' 2018-06-30 23:59:55', '2018-07-01 00:38:10', 1, 2295, 3, ' Spaulding Ave & Armitage Ave', 340, ' Clark St & Wrightwood Ave', 'Subscriber', 'Male', 1989, 23],
             [2, ' 2018-06-30 23:59:56', '2018-07-01 00:17:14', 2, 1038, 4, ' Spaulding Ave & Armitage Ave', 338, 'Calumet Ave & 18th St', 'Subscriber', 'Female', 1985, 23],
             [3,    ' 2018-06-30 18:59:48', '2018-07-01 00:08:45', 3, 537, 5, ' Clark St & Wrightwood Ave', 506, ' Spaulding Ave & Armitage Ave', 'Subscriber', 'Male', 1980, 18]],
            columns=['trip_id', 'start_time', 'end_time', 'bikeid', 'tripduration',
       'from_station_id', 'from_station_name', 'to_station_id',
       'to_station_name', 'usertype', 'gender', 'birthyear', 'hour']
        ).astype(dtype={
            "trip_id": "int64",
            "start_time": "datetime64",
            "end_time": "datetime64",
            "bikeid": 'int64',
            "tripduration": 'int64',
            'from_station_id': 'int64',
            'from_station_name': 'object',
            'to_station_id': 'int64',
            'to_station_name': 'object',
            'usertype': 'object',
            'gender': 'object',
            'birthyear': 'object',
            'hour': 'int64'
        })
        file_name = 'fake_file'
        read_csv_mock = Mock(return_value = dummy_bike_trip_data_frame)
        pd.read_csv = read_csv_mock

        actual_data_frame = get_and_format_trip_data(file_name)

        self.assertTrue(actual_data_frame.equals(expected_data_frame))
        read_csv_mock.assert_called_once_with(file_name, parse_dates=['start_time', 'end_time'])