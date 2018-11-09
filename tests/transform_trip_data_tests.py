import unittest
import pandas as pd

from script import add_path_station_locations, identify_discrete_trips

class ScriptTests(unittest.TestCase):

    def test__add_path_station_locations__always__returns_correct(self):
        paths = pd.DataFrame(
            [[145,  0, 1],
             [1212, 0, 2],
             [1,    1, 2]],
            columns=["Trip Count", "from_station_id", "to_station_id"]
        ).astype(dtype={
            "Trip Count": "int64",
            "from_station_id": "int64",
            "to_station_id": "int64"})
        locations = pd.DataFrame(
            [[0, 0.5, 0.5],
             [1, 10, 100],
             [2, -2, 2]],
            columns=["station_id", "Latitude", "Longitude"]
        ).astype(dtype={
            "station_id": "int64",
            "Latitude": "float64",
            "Longitude": "float64"})
        expected_data_frame = pd.DataFrame(
            [[145,  0, 1, 0.5, 0.5, 10, 100],
             [1212, 0, 2, 0.5, 0.5, -2, 2],
             [1,    1, 2, 10,  100, -2, 2]],
            columns=[
                "Trip Count",
                "from_station_id",
                "to_station_id",
                "Start_Latitude",
                "Start_Longitude",
                "End_Latitude",
                "End_Longitude"]
        ).astype(dtype={
            "Trip Count": "int64",
            "from_station_id": "int64",
            "to_station_id": "int64",
            "Start_Latitude": "float64",
            "Start_Longitude": "float64",
            "End_Latitude": "float64",
            "End_Longitude": "float64"})

        actual_data_frame = add_path_station_locations(paths, locations)

        self.assertTrue(actual_data_frame.equals(expected_data_frame))
        paths["Trip Count"][0] = 6
        # This second assert shows that mutating `paths` doesn't affect `actual_data_frame`
        self.assertTrue(actual_data_frame.equals(expected_data_frame))

    def test__identify_discrete_trips__always__returns_correct(self):
        parse_dates = ['start_time', 'end_time']
        trips =  pd.read_csv('../resources/test_data', parse_dates=parse_dates)

        result = identify_discrete_trips(trips)

        sample_path = result['path_id'][0]
        sample_path_id_type = type(sample_path)

        sample_trip = result.iloc[0]
        sample_trip_path = sample_trip['path_id']
        sample_trip_from = sample_trip['from_station_id']
        sample_trip_to = sample_trip['to_station_id']

        self.assertTrue(result.columns.contains('path_id'))
        self.assertTrue(sample_path_id_type == (type((1, 2)))) #how to check if types are right?? has to be something better than this
        self.assertTrue(sample_trip_from == sample_trip_path[0])
        self.assertTrue(sample_trip_to == sample_trip_path[1])



