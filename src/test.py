from distance import GreatCircleDistance
from point import Point
import unittest
from service import FindNearByPoints
from unittest import mock
from find_near_by_customers import FindNearbyCustomers

class TestPoint(unittest.TestCase):
    
    def test_set_radians(self):
        point = Point(lat_degrees=53.0033946, long_degrees=-6.3877505)
        point.set_radians()
        self.assertEqual(point.lat_degrees, 53.0033946)
        self.assertEqual(point.lat_radians, 0.9250837505037829)

class TestPointInvalidValues(unittest.TestCase):

    def test_point_creation_with_invalid_values(self):
        self.assertRaises(ValueError, Point, lat_degrees=53.0033946, long_radians=0.9250837505037829)

    def test_point_creation_with_invalid_lat_long(self):
        self.assertRaises(ValueError, Point, lat_degrees=92.3434334, long_degrees=-6.2877505)


class TestCalculateGreatCircleDistance(unittest.TestCase):

    def test_calculate_distance(self):
        pointA = Point(lat_degrees=53.0033946, long_degrees=-6.3877505)
        pointB = Point(lat_degrees=53.3381985, long_degrees=-6.2592576)
        self.assertAlmostEqual(GreatCircleDistance.calculate_great_circle_distance(pointA, pointB), 38.20092613347043)

    def test_calculate_distance_different_values(self):
        pointA = Point(lat_degrees=53.1489345, long_degrees=-6.8422408)
        pointB = Point(lat_degrees=53.3381985, long_degrees=-6.2592576)
        self.assertAlmostEqual(GreatCircleDistance.calculate_great_circle_distance(pointA, pointB), 44.13286096134965)

class TestFindNearByPoints(unittest.TestCase):

    @mock.patch("point.Point")
    @mock.patch("distance.GreatCircleDistance.calculate_great_circle_distance")
    def test_find_near_by_points(self, mock_calculate_great_circle_distance, mock_point_class):
        point_list = [
            {u'latitude': u'53.0033946', u'user_id': 39, u'name': u'Lisa Ahearn', u'longitude': u'-6.3877505'},
            {u'latitude': u'52.228056', u'user_id': 18, u'name': u'Bob Larkin', u'longitude': u'-7.915833'},
            {u'latitude': u'53.1302756', u'user_id': 5, u'name': u'Nora Dempsey', u'longitude': u'-6.2397222'},
            {u'latitude': u'53.521111', u'user_id': 20, u'name': u'Enid Enright', u'longitude': u'-9.831111'},
        ]

        return_list = [
            {u'latitude': u'53.0033946', u'user_id': 39, u'name': u'Lisa Ahearn', u'longitude': u'-6.3877505'},
            {u'latitude': u'53.1302756', u'user_id': 5, u'name': u'Nora Dempsey', u'longitude': u'-6.2397222'},
        ]


        origin_point = Point(lat_degrees=53.339428, long_degrees=-6.257664)
        points = [
            origin_point,
            Point(lat_degrees=53.0033946, long_degrees=-6.3877505),
            Point(lat_degrees=52.228056, long_degrees=-7.915833),
            Point(lat_degrees=53.1302756, long_degrees=-6.2397222),
            Point(lat_degrees=53.521111, long_degrees=-9.831111)
        ]

        mock_point_class.side_effect =  points
        mock_calculate_great_circle_distance.side_effect = [38.35801477480546, 166.4480926426452, 23.28732066309975, 237.5760150398592]

        find_nearby_points_service =  FindNearByPoints(point_cls=mock_point_class)
        near_by_points = find_nearby_points_service.find_nearby_points_within_distance(53.339428, -6.257664, point_list, 50)

        mock_calculate_great_circle_distance.assert_any_call(points[1], origin_point)
        mock_calculate_great_circle_distance.assert_any_call(points[2], origin_point)
        mock_calculate_great_circle_distance.assert_any_call(points[3], origin_point)
        mock_calculate_great_circle_distance.assert_any_call(points[4], origin_point)

        self.assertEqual(near_by_points, return_list)


class TestFindNearbyCustomers(unittest.TestCase):

    @mock.patch("builtins.sorted")
    def test_find_near_by_customers(self, mock_sorted):

        customers = [
            {u'latitude': u'53.0033946', u'user_id': 39, u'name': u'Lisa Ahearn', u'longitude': u'-6.3877505'},
            {u'latitude': u'52.228056', u'user_id': 18, u'name': u'Bob Larkin', u'longitude': u'-7.915833'},
            {u'latitude': u'53.1302756', u'user_id': 5, u'name': u'Nora Dempsey', u'longitude': u'-6.2397222'},
            {u'latitude': u'53.521111', u'user_id': 20, u'name': u'Enid Enright', u'longitude': u'-9.831111'},
        ]

        return_list = [
            {u'latitude': u'53.0033946', u'user_id': 39, u'name': u'Lisa Ahearn', u'longitude': u'-6.3877505'},
            {u'latitude': u'53.1302756', u'user_id': 5, u'name': u'Nora Dempsey', u'longitude': u'-6.2397222'},
        ]

        sorted_list =  [
            {u'latitude': u'53.1302756', u'user_id': 5, u'name': u'Nora Dempsey', u'longitude': u'-6.2397222'},
            {u'latitude': u'53.0033946', u'user_id': 39, u'name': u'Lisa Ahearn', u'longitude': u'-6.3877505'}
        ]

        mock_sorted.return_value = sorted_list

        near_by_points_service = FindNearByPoints()
        near_by_points_service.find_nearby_points_within_distance = mock.MagicMock(return_value = return_list)

        near_by_customers = FindNearbyCustomers.find_near_by_customers(53.339428, -6.257664, customers, 50, 'user_id', near_by_points_service)
        near_by_points_service.find_nearby_points_within_distance.assert_called_once_with(53.339428, -6.257664, customers, 50)

        mock_sorted.assert_called_once()
        self.assertEqual(near_by_customers, sorted_list)


    @mock.patch("builtins.open")
    def test_parse_file(self, mock_open):
        file_contains = """
            {u'latitude': u'53.0033946', u'user_id': 39, u'name': u'Lisa Ahearn', u'longitude': u'-6.3877505'},
            {u'latitude': u'52.228056', u'user_id': 18, u'name': u'Bob Larkin', u'longitude': u'-7.915833'},
            {u'latitude': u'53.1302756', u'user_id': 5, u'name': u'Nora Dempsey', u'longitude': u'-6.2397222'},
            {u'latitude': u'53.521111', u'user_id': 20, u'name': u'Enid Enright', u'longitude': u'-9.831111'},
        """

        mock_open.side_effect = [
            mock.mock_open(read_data=file_contains).return_value,
        ]

        return_list = FindNearbyCustomers.parse_file('customer.txt')
        mock_open.assert_called_once_with('customer.txt')



if __name__ == '__main__':
    unittest.main()
