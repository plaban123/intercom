from point import Point
from distance import GreatCircleDistance


class FindNearByPoints(object):

    def __init__(self, formula_cls=GreatCircleDistance, point_cls=Point):
        self.formula_cls = formula_cls
        self.point_cls = point_cls

    def find_nearby_points_within_distance(self, origin_latitude, origin_longitude, points_list, distance):
        origin_point = self.point_cls(lat_degrees=origin_latitude, long_degrees=origin_longitude)
        near_by_points = []

        for point_dict in points_list:
            point = self.point_cls(lat_degrees=float(point_dict['latitude']), long_degrees=float(point_dict['longitude']))
            point_distance = self.formula_cls.calculate_great_circle_distance(point, origin_point)

            if point_distance <= distance:
                near_by_points.append(point_dict)

        return near_by_points