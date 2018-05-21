from math import cos, sin, asin, sqrt

class GreatCircleDistance(object):

    @staticmethod
    def calculate_great_circle_distance(starting_point, end_point, radius=6371):
        '''Calculate great circle distance between two points using radians'''

        delta_long = end_point.long_radians - starting_point.long_radians
        delta_lat = end_point.lat_radians - starting_point.lat_radians

        A = sin(delta_lat/2) ** 2 + cos(starting_point.lat_radians) * cos(end_point.lat_radians) * sin(delta_long / 2) ** 2
        C = 2 * asin(sqrt(A))
        return C * radius